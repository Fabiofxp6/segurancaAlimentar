import logging

from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from django.utils import timezone

from contas.models import Perfil
from contas.vinculos import estabelecimentos_acessiveis

from . import termo_pdf
from .models import AcaoFiscalizacao, HistoricoInspecao, Inspecao, LiberacaoTermo, TermoInspecao
from .pontuacao import OPCOES_DEMONSTRACAO_1
from .resultados import RespostasConfirmadasIndisponiveis, atual, respostas_confirmadas
from .services import _acessiveis, _ator, acoes_supervisionadas, supervisor_ativo


logger = logging.getLogger(__name__)


class TermoDesatualizado(Exception):
    pass


class FalhaGeracaoTermo(Exception):
    pass


def _escopo_interno(ator):
    equipe = _acessiveis(ator)
    if ator.perfil == Perfil.ADMINISTRADOR:
        return equipe
    return Inspecao.objects.filter(
        Q(pk__in=equipe.values("pk"))
        | Q(acao_id__in=acoes_supervisionadas(ator.pk), resultados__termos__isnull=False),
    ).distinct()


def _inspecao(ator, pk, *, supervisao=False, bloquear=False):
    escopo = _escopo_interno(ator) if supervisao else _acessiveis(ator)
    consulta = Inspecao.objects.filter(pk__in=escopo.values("pk"))
    if bloquear:
        consulta = consulta.select_for_update()
    return consulta.get(pk=pk)


def _termos():
    return TermoInspecao.objects.select_related("resultado__inspecao", "liberacao").defer(
        "resultado__respostas_utilizadas",
    )


def _termo_da_inspecao(pk):
    return _termos().filter(resultado__inspecao_id=pk).order_by("-versao")


def listar_emitidos(ator_id, pagina):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    termos = _termos().filter(resultado__inspecao_id__in=_escopo_interno(ator).values("pk")).defer("conteudo")
    return Paginator(termos.order_by("-emitido_em", "-pk"), 25).get_page(pagina)


def consultar(ator_id, pk, *, termo_id=None):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _inspecao(ator, pk, supervisao=True)
    termos = _termo_da_inspecao(pk).defer("conteudo")
    recente = termos.first()
    termo = recente if termo_id is None else termos.get(pk=termo_id)
    equipe = _acessiveis(ator).filter(pk=pk).exists()
    pode_liberar = bool(termo and termo == recente and not hasattr(termo, "liberacao") and (
        ator.perfil == Perfil.ADMINISTRADOR or supervisor_ativo(inspecao.acao_id, ator.pk)
    ))
    return {
        "inspecao": inspecao, "termo": termo, "equipe": equipe, "pode_liberar": pode_liberar,
        "pode_emitir": termo is None and equipe and inspecao.estado == Inspecao.Estado.CONCLUIDA,
    }


def verificar_acesso(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    _inspecao(ator, pk, supervisao=True)


def baixar_interno(ator_id, pk, termo_id):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    return _termo_da_inspecao(pk).filter(resultado__inspecao_id__in=_escopo_interno(ator).values("pk")).get(pk=termo_id)


def _liberados(ator_id):
    _ator(ator_id, Perfil.ESTABELECIMENTO)
    unidades = estabelecimentos_acessiveis(ator_id)
    posterior = TermoInspecao.objects.filter(
        resultado__inspecao_id=OuterRef("resultado__inspecao_id"),
        versao__gt=OuterRef("versao"), liberacao__isnull=False,
    )
    return _termos().filter(
        resultado__inspecao__estabelecimento_id__in=unidades.values("pk"), liberacao__isnull=False,
    ).annotate(versao_anterior=Exists(posterior))


def listar_liberados(ator_id, pagina):
    termos = _liberados(ator_id).defer("conteudo").order_by("-liberacao__liberado_em", "-pk")
    return Paginator(termos, 25).get_page(pagina)


def consultar_liberado(ator_id, termo_id, *, baixar=False):
    termos = _liberados(ator_id)
    if not baixar:
        termos = termos.defer("conteudo")
    return termos.get(pk=termo_id)


def _itens_publicos(resultado):
    try:
        respostas = respostas_confirmadas(resultado)
    except RespostasConfirmadasIndisponiveis as erro:
        raise TermoDesatualizado(str(erro)) from erro

    itens = []
    for item in resultado.versao_checklist.itens:
        resposta = respostas.get(item["id"])
        if resposta is None:
            continue
        descricao = resposta["descricao_irregularidade"]
        nao_conforme = OPCOES_DEMONSTRACAO_1.get(resposta["opcao"].casefold()) == 0
        if nao_conforme or descricao:
            itens.append((item["ordem"], item["enunciado"], nao_conforme, descricao))
    return itens


@transaction.atomic
def emitir(ator_id, pk, *, operacao_id):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _inspecao(ator, pk, bloquear=True)
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO, bloquear=True)
    if not _acessiveis(ator).filter(pk=pk).exists():
        raise Inspecao.DoesNotExist
    if inspecao.estado != Inspecao.Estado.CONCLUIDA:
        raise TermoDesatualizado("Conclua a inspeção para emitir o termo.")

    termos = _termo_da_inspecao(pk).defer("conteudo")
    existente = termos.filter(anterior__isnull=True, operacao_id=operacao_id, emitido_por=ator).first()
    if existente:
        return existente
    if termos.exists():
        raise TermoDesatualizado("Já existe um termo emitido. Abra o documento disponível.")

    return _registrar_termo(atual(inspecao), ator, operacao_id, anterior=None)


def _registrar_termo(resultado, ator, operacao_id, *, anterior):
    inspecao = resultado.inspecao
    versao = anterior.versao + 1 if anterior else 1
    codigo = f"DEMO-{inspecao.pk}-V{versao:02d}"
    emitido_em = timezone.now()
    itens = _itens_publicos(resultado)
    try:
        conteudo = termo_pdf.gerar(
            resultado, codigo=codigo, versao=versao, emitido_em=emitido_em, itens=itens,
            anterior_codigo=anterior.codigo if anterior else None,
        )
    except Exception as erro:
        logger.warning("Falha na geração do termo de demonstração (%s).", type(erro).__name__)
        raise FalhaGeracaoTermo from None

    termo = TermoInspecao.objects.create(
        resultado=resultado, anterior=anterior, codigo=codigo, versao=versao, emitido_por=ator,
        emitido_em=emitido_em, operacao_id=operacao_id, conteudo=conteudo,
    )
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=ator, ato=HistoricoInspecao.Ato.TERMO_EMITIDO,
        dados={"termo": termo.pk, "versao": versao, "codigo": codigo, "resultado": resultado.pk,
               "anterior": termo.anterior_id},
    )
    return termo


def retificar_se_necessario(resultado, ator, operacao_id):
    anterior = _termo_da_inspecao(resultado.inspecao_id).defer("conteudo").first()
    if anterior is None:
        return None
    emitido = anterior.resultado
    if (
        resultado.pontuacao != emitido.pontuacao or resultado.classificacao != emitido.classificacao
        or _itens_publicos(resultado) != _itens_publicos(emitido)
    ):
        return _registrar_termo(resultado, ator, operacao_id, anterior=anterior)
    return None


@transaction.atomic
def liberar(ator_id, pk, termo_id, *, operacao_id):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    previa = _inspecao(ator, pk, supervisao=True)
    acao = AcaoFiscalizacao.objects.select_for_update().get(pk=previa.acao_id)
    inspecao = _inspecao(ator, pk, supervisao=True, bloquear=True)
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO, bloquear=True)
    designacao = None
    if ator.perfil == Perfil.FISCALIZACAO:
        if not supervisor_ativo(acao.pk, ator.pk):
            raise PermissionDenied
        designacao = acao.designacoes.get(fiscal_id=ator.pk, fim__isnull=True)
    if inspecao.estado != Inspecao.Estado.CONCLUIDA:
        raise TermoDesatualizado("A liberação exige uma inspeção concluída e um termo emitido.")

    termo = _termo_da_inspecao(pk).defer("conteudo").get(pk=termo_id)
    existente = getattr(termo, "liberacao", None)
    if existente:
        if existente.operacao_id == operacao_id and existente.liberado_por_id == ator.pk:
            return existente
        raise TermoDesatualizado("Este resultado já foi liberado. Confira sua situação.")

    if _termo_da_inspecao(pk).filter(versao__gt=termo.versao).exists():
        raise TermoDesatualizado("Há uma versão emitida mais recente. Abra o termo atual para liberar.")

    liberacao = LiberacaoTermo.objects.create(
        termo=termo, liberado_por=ator, designacao=designacao, operacao_id=operacao_id,
    )
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=ator, ato=HistoricoInspecao.Ato.TERMO_LIBERADO,
        dados={"termo": termo.pk, "versao": termo.versao, "liberacao": liberacao.pk, "designacao": liberacao.designacao_id},
    )
    return liberacao
