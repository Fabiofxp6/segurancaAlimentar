from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from contas.models import Perfil, Usuario

from . import pontuacao
from .conclusao_services import _revisao
from .models import AcaoFiscalizacao, DecisaoCorrecao, HistoricoInspecao, Inspecao, PedidoCorrecao, ResultadoInspecao
from .resultados import RespostasConfirmadasIndisponiveis, atual, respostas_confirmadas
from .services import _acessiveis, _ator, _equipe_acao, acoes_supervisionadas
from .termo_services import retificar_se_necessario


class CorrecaoDesatualizada(Exception):
    pass


def _inspecao_da_equipe(ator, pk, *, bloquear=False):
    inspecoes = Inspecao.objects.filter(pk__in=_acessiveis(ator).values("pk"))
    if bloquear:
        inspecoes = inspecoes.select_for_update()
    return inspecoes.get(pk=pk, estado=Inspecao.Estado.CONCLUIDA)


def _pedidos(ator):
    equipe = _acessiveis(ator).values("pk")
    escopo = Q(base__inspecao_id__in=equipe)
    if ator.perfil == Perfil.FISCALIZACAO:
        escopo |= Q(base__inspecao__acao_id__in=acoes_supervisionadas(ator.pk))
    return PedidoCorrecao.objects.filter(escopo).select_related(
        "base__inspecao", "solicitante", "decisao__autor", "resultado_aplicado__aplicado_por",
    ).defer("base__respostas_utilizadas", "resultado_aplicado__respostas_utilizadas")


def _item(base, item_id):
    for item in base.versao_checklist.itens:
        if item["id"] == str(item_id):
            return item
    raise Inspecao.DoesNotExist


def _respostas(base):
    try:
        return respostas_confirmadas(base)
    except RespostasConfirmadasIndisponiveis as erro:
        raise CorrecaoDesatualizada(str(erro)) from erro


def _designacoes(pedido):
    return pedido.base.inspecao.acao.designacoes.filter(fim__isnull=True).exclude(fiscal_id=pedido.solicitante_id)


def _elegiveis(pedido, designacoes):
    return designacoes.filter(fiscal__in=_equipe_acao(pedido.base.inspecao.acao_id))


def _pode_aplicar(ator, pedido):
    return ator.perfil == Perfil.ADMINISTRADOR or (
        ator.pk == pedido.solicitante_id and _acessiveis(ator).filter(pk=pedido.base.inspecao_id).exists()
    )


def listar(ator_id, pagina):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    return Paginator(_pedidos(ator).order_by("-pk"), 25).get_page(pagina)


def consultar_inspecao(ator_id, pk, pagina):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _inspecao_da_equipe(ator, pk)
    base = atual(inspecao)
    revisoes = inspecao.resultados.defer("respostas_utilizadas").order_by("-revisao")
    pedidos = _pedidos(ator).filter(base__inspecao_id=pk).order_by("-pk")
    return {
        "inspecao": inspecao, "base": base, "itens": base.versao_checklist.itens,
        "revisoes": revisoes, "pagina": Paginator(pedidos, 25).get_page(pagina),
        "pode_solicitar": ator.perfil == Perfil.FISCALIZACAO,
    }


def consultar_item(ator_id, pk, item_id):
    ator = _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = _inspecao_da_equipe(ator, pk)
    base = atual(inspecao)
    return inspecao, base, _item(base, item_id), _respostas(base).get(str(item_id))


def consultar_pedido(ator_id, pk, pedido_id):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    pedido = _pedidos(ator).get(pk=pedido_id, base__inspecao_id=pk)
    inspecao = pedido.base.inspecao
    base_atual = atual(inspecao).pk == pedido.base_id
    pode_decidir = False
    if base_atual and not hasattr(pedido, "decisao") and ator.pk != pedido.solicitante_id:
        elegiveis = _elegiveis(pedido, _designacoes(pedido))
        pode_decidir = (
            not elegiveis.exists() if ator.perfil == Perfil.ADMINISTRADOR
            else elegiveis.filter(fiscal=ator).exists()
        )
    return {
        "inspecao": inspecao, "pedido": pedido, "item": _item(pedido.base, pedido.item_id),
        "base_atual": base_atual, "pode_decidir": pode_decidir,
        "pode_aplicar": base_atual and pedido.situacao == "Aprovada" and _pode_aplicar(ator, pedido),
        "equipe": _acessiveis(ator).filter(pk=pk).exists(),
    }


def verificar_acesso(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    if not _acessiveis(ator).filter(pk=pk, estado=Inspecao.Estado.CONCLUIDA).exists() and not _pedidos(ator).filter(
        base__inspecao_id=pk,
    ).exists():
        raise Inspecao.DoesNotExist


def _auditar(pedido, ator, ato, **dados):
    HistoricoInspecao.objects.create(
        inspecao_id=pedido.base.inspecao_id, autor=ator, ato=ato, dados={"pedido": pedido.pk, **dados},
    )


def _resposta_corrigida(antes, proposto):
    revisao = antes["revisao"] + 1 if antes else 1
    return {**proposto, "revisao": revisao}


@transaction.atomic
def solicitar(ator_id, pk, item_id, *, base_id, operacao_id, justificativa, opcao, observacao, descricao_irregularidade):
    ator = _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = _inspecao_da_equipe(ator, pk, bloquear=True)
    ator = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    if not _acessiveis(ator).filter(pk=pk).exists():
        raise Inspecao.DoesNotExist

    base = inspecao.resultados.get(pk=base_id)
    item = _item(base, item_id)
    justificativa = justificativa.strip()
    if (not justificativa or opcao not in item["opcoes"]
            or opcao.casefold() not in pontuacao.OPCOES_DEMONSTRACAO_1):
        raise ValidationError("Informe uma justificativa e escolha uma resposta válida para esse item.")
    proposto = {"opcao": opcao, "observacao": observacao, "descricao_irregularidade": descricao_irregularidade}
    existente = base.pedidos_correcao.filter(operacao_id=operacao_id).first()
    if existente:
        if (existente.solicitante_id == ator.pk and existente.item_id == item_id
                and existente.proposto == proposto and existente.justificativa == justificativa):
            return existente
        raise CorrecaoDesatualizada("Esta operação já foi usada com outros dados.")
    if atual(inspecao).pk != base.pk:
        raise CorrecaoDesatualizada("A revisão mudou. Confira os dados e abra um novo pedido.")

    respostas = _respostas(base)
    chave = str(item_id)
    antes = respostas.get(chave)
    if antes and all(antes[campo] == valor for campo, valor in proposto.items()):
        raise ValidationError("Informe pelo menos uma mudança.")
    respostas = {**respostas, chave: _resposta_corrigida(antes, proposto)}
    pontuacao.calcular(base.versao_checklist, respostas)
    pedido = PedidoCorrecao.objects.create(
        base=base, item_id=item_id, antes=antes, proposto=proposto, justificativa=justificativa,
        solicitante=ator, operacao_id=operacao_id,
    )
    _auditar(pedido, ator, HistoricoInspecao.Ato.CORRECAO_PEDIDA, base=base.revisao, item=chave)
    return pedido


def _bloquear_pedido(ator_id, pk, pedido_id):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    pedido = _pedidos(ator).get(pk=pedido_id, base__inspecao_id=pk)
    AcaoFiscalizacao.objects.select_for_update().get(pk=pedido.base.inspecao.acao_id)
    inspecao = Inspecao.objects.select_for_update().get(pk=pk, estado=Inspecao.Estado.CONCLUIDA)
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO, bloquear=True)
    return ator, inspecao, _pedidos(ator).get(pk=pedido_id, base__inspecao_id=pk)


def _autoridade(ator, pedido):
    if ator.pk == pedido.solicitante_id:
        raise PermissionDenied
    designacoes = _designacoes(pedido)
    elegiveis = _elegiveis(pedido, designacoes)
    if ator.perfil == Perfil.ADMINISTRADOR:
        candidatos = designacoes.values("fiscal_id")
        list(Usuario.objects.select_for_update().filter(pk__in=candidatos).order_by("pk").values_list("pk", flat=True))
        if elegiveis.exists():
            raise PermissionDenied
        return None
    designacao = elegiveis.filter(fiscal_id=ator.pk).first()
    if designacao is None:
        raise PermissionDenied
    return designacao


@transaction.atomic
def decidir(ator_id, pk, pedido_id, *, aprovada, motivo, operacao_id):
    ator, inspecao, pedido = _bloquear_pedido(ator_id, pk, pedido_id)
    motivo = motivo.strip()
    if not motivo:
        raise ValidationError("Informe o motivo da decisão.")
    existente = getattr(pedido, "decisao", None)
    if existente:
        if (existente.operacao_id == operacao_id and existente.autor_id == ator.pk
                and existente.aprovada == aprovada and existente.motivo == motivo):
            return existente
        raise CorrecaoDesatualizada("Já existe uma decisão para este pedido.")
    designacao = _autoridade(ator, pedido)
    if atual(inspecao).pk != pedido.base_id:
        raise CorrecaoDesatualizada("A revisão do pedido foi superada.")
    decisao = DecisaoCorrecao.objects.create(
        pedido=pedido, aprovada=aprovada, motivo=motivo, autor=ator, designacao=designacao, operacao_id=operacao_id,
    )
    _auditar(pedido, ator, HistoricoInspecao.Ato.CORRECAO_DECIDIDA,
             aprovada=aprovada, designacao=decisao.designacao_id)
    return decisao


@transaction.atomic
def aplicar(ator_id, pk, pedido_id, *, operacao_id):
    ator, inspecao, pedido = _bloquear_pedido(ator_id, pk, pedido_id)
    if not _pode_aplicar(ator, pedido):
        raise PermissionDenied
    existente = getattr(pedido, "resultado_aplicado", None)
    if existente:
        if existente.operacao_id == operacao_id and existente.aplicado_por_id == ator.pk:
            return existente
        raise CorrecaoDesatualizada("Esta correção já foi aplicada.")
    if pedido.situacao != "Aprovada":
        raise CorrecaoDesatualizada("Aplique somente um pedido aprovado.")

    base = atual(inspecao)
    if base.pk != pedido.base_id:
        raise CorrecaoDesatualizada("A revisão mudou. Registre um novo pedido na revisão atual.")
    respostas = {**_respostas(base), str(pedido.item_id): _resposta_corrigida(pedido.antes, pedido.proposto)}
    nota, classificacao = pontuacao.calcular(base.versao_checklist, respostas)
    resultado = ResultadoInspecao.objects.create(
        inspecao=inspecao, revisao=base.revisao + 1, correcao=pedido, aplicado_em=timezone.now(),
        aplicado_por=ator, versao_checklist=base.versao_checklist, regra_pontuacao=base.regra_pontuacao,
        pontuacao=nota, classificacao=classificacao, respostas_utilizadas=respostas,
        revisao_base=_revisao(inspecao, respostas), concluido_por_id=base.concluido_por_id,
        concluido_em=base.concluido_em, operacao_id=operacao_id,
    )
    _auditar(pedido, ator, HistoricoInspecao.Ato.CORRECAO_APLICADA,
             resultado_anterior=base.pk, resultado=resultado.pk, revisao=resultado.revisao)
    retificar_se_necessario(resultado, ator, operacao_id)
    return resultado
