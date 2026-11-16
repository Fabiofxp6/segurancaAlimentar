from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario
from estabelecimentos.models import Estabelecimento

from .models import AcaoFiscalizacao, DesignacaoSupervisor, HistoricoInspecao, Inspecao, PedidoAdiamento


class InspecaoDesatualizada(Exception):
    pass


def _ator(ator_id, *perfis, bloquear=False):
    if not settings.INSPECOES_DEMONSTRACAO:
        raise PermissionDenied
    consulta = Usuario.objects.filter(pk=ator_id, perfil__in=perfis, is_active=True)
    if bloquear:
        consulta = consulta.select_for_update()
    try:
        return consulta.get()
    except Usuario.DoesNotExist:
        raise PermissionDenied from None


def _fiscais_ativos():
    return Usuario.objects.filter(is_active=True, perfil=Perfil.FISCALIZACAO)


def _membros_acao(acao_id):
    return Usuario.objects.filter(
        Q(inspecoes_responsavel__acao_id=acao_id) | Q(inspecoes_participante__acao_id=acao_id),
    ).distinct()


def _equipe_acao(acao_id):
    return _membros_acao(acao_id).filter(is_active=True, perfil=Perfil.FISCALIZACAO)


def _acessiveis(ator):
    consulta = Inspecao.objects.all()
    if ator.perfil == Perfil.FISCALIZACAO:
        consulta = consulta.filter(Q(responsavel=ator) | Q(participantes=ator)).distinct()
    return consulta


def _opcoes(consulta, campo="username"):
    return list(consulta.order_by(campo, "pk").values_list("pk", campo))


def _opcoes_checklist():
    publicadas = VersaoChecklist.objects.filter(
        finalidade=VersaoChecklist.Finalidade.DEMONSTRACAO,
    ).order_by("checklist_id", "-numero").distinct("checklist_id")
    opcoes = [
        (checklist_id, f"{titulo} · Versão {numero}")
        for checklist_id, titulo, numero in publicadas.values_list("checklist_id", "titulo", "numero")
    ]
    return sorted(opcoes, key=lambda opcao: (opcao[1].casefold(), opcao[0]))

def opcoes_criacao(ator_id, perfil):
    _ator(ator_id, perfil)
    opcoes = {"estabelecimentos": _opcoes(Estabelecimento.objects.filter(ativo=True), "nome")}
    if perfil == Perfil.ADMINISTRADOR:
        opcoes["fiscais"] = _opcoes(_fiscais_ativos())
        opcoes["acoes"] = [(pk, f"Ação #{pk}") for pk in AcaoFiscalizacao.objects.order_by("-pk").values_list("pk", flat=True)]
    else:
        opcoes["checklists"] = _opcoes_checklist()
    return opcoes


def bloqueio_inicio(inspecao):
    if inspecao.pedidos_adiamento.filter(situacao=PedidoAdiamento.Situacao.PENDENTE).exists():
        return "Aguarde a decisão do pedido de adiamento."
    if inspecao.agendada_em and inspecao.agendada_em > timezone.now():
        return "A inspeção poderá ser iniciada a partir da data agendada."
    return ""


def consultar(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _acessiveis(ator).select_related(
        "acao", "estabelecimento", "versao_checklist", "responsavel",
    ).prefetch_related("participantes", "historico__autor").get(pk=pk)
    pode_iniciar = (
        ator.perfil == Perfil.FISCALIZACAO and ator.pk == inspecao.responsavel_id
        and inspecao.estado == Inspecao.Estado.ATRIBUIDA
    )
    designacoes = inspecao.acao.designacoes.filter(
        fim__isnull=True, fiscal__in=_equipe_acao(inspecao.acao_id),
    ).select_related("fiscal").order_by("fiscal__username")
    supervisor = supervisor_ativo(inspecao.acao_id, ator.pk)
    return inspecao, ator.perfil, pode_iniciar, designacoes, supervisor


def opcoes_inicio(ator_id, pk):
    _ator(ator_id, Perfil.FISCALIZACAO)
    consulta = Inspecao.objects.filter(responsavel_id=ator_id)
    inspecao = consulta.get(pk=pk)
    return inspecao, _opcoes_checklist()


def opcoes_equipe(ator_id, pk):
    _ator(ator_id, Perfil.ADMINISTRADOR)
    inspecao = Inspecao.objects.prefetch_related("participantes").get(pk=pk)
    return inspecao, _opcoes(_fiscais_ativos())


def acoes_supervisionadas(ator_id):
    inspecoes = Inspecao.objects.filter(Q(responsavel_id=ator_id) | Q(participantes=ator_id))
    return DesignacaoSupervisor.objects.filter(
        fiscal_id=ator_id, fim__isnull=True, acao_id__in=inspecoes.values("acao_id"),
    ).values("acao_id")


def supervisor_ativo(acao_id, fiscal_id):
    return settings.INSPECOES_DEMONSTRACAO and DesignacaoSupervisor.objects.filter(
        acao_id=acao_id, fiscal_id=fiscal_id, fim__isnull=True, fiscal__in=_equipe_acao(acao_id),
    ).exists()


def _outras_designacoes(acao_id, solicitante_id):
    return DesignacaoSupervisor.objects.filter(acao_id=acao_id, fim__isnull=True).exclude(fiscal_id=solicitante_id)


def supervisores_elegiveis(acao_id, solicitante_id):
    return _outras_designacoes(acao_id, solicitante_id).filter(fiscal__in=_equipe_acao(acao_id))


def autoridade_decisao(ator, inspecao, solicitante_id):
    if ator.pk == solicitante_id:
        raise PermissionDenied
    acao_id = inspecao.acao_id
    elegiveis = supervisores_elegiveis(acao_id, solicitante_id)
    if ator.perfil == Perfil.ADMINISTRADOR:
        candidatos = _outras_designacoes(acao_id, solicitante_id).values("fiscal_id")
        list(Usuario.objects.select_for_update().filter(pk__in=candidatos).order_by("pk").values_list("pk", flat=True))
        if elegiveis.exists():
            raise PermissionDenied
        return None
    designacao = elegiveis.filter(fiscal=ator).first()
    if designacao is None:
        raise PermissionDenied
    return designacao


def _estabelecimento(estabelecimento_id):
    try:
        return Estabelecimento.objects.select_for_update().get(pk=estabelecimento_id, ativo=True)
    except Estabelecimento.DoesNotExist:
        raise ValidationError("Selecione um estabelecimento ativo.") from None


def _validar_fiscais(ids):
    selecionados = list(_fiscais_ativos().select_for_update().filter(pk__in=ids).order_by("pk"))
    if {fiscal.pk for fiscal in selecionados} != set(ids):
        raise ValidationError("A equipe deve conter somente fiscais ativos.")


def _versao(checklist_id):
    try:
        checklist = Checklist.objects.select_for_update().get(pk=checklist_id)
    except Checklist.DoesNotExist:
        raise ValidationError("Selecione um checklist publicado de demonstração.") from None
    versao = checklist.versoes.filter(
        finalidade=VersaoChecklist.Finalidade.DEMONSTRACAO,
    ).order_by("-numero").first()
    if versao is None:
        raise ValidationError("Selecione um checklist publicado de demonstração.")
    return versao


def _repeticao(ator, operacao, solicitacao):
    anterior = Inspecao.objects.filter(criada_por=ator, operacao_criacao=operacao).first()
    if anterior:
        registro = anterior.historico.order_by("pk").first()
        if registro is None or registro.dados.get("solicitacao") != solicitacao:
            raise InspecaoDesatualizada
    return anterior


def _equipe(responsavel_id, participantes_ids):
    return {"responsavel": responsavel_id, "participantes": sorted(set(participantes_ids) - {responsavel_id})}


@transaction.atomic
def atribuir(ator_id, *, operacao, estabelecimento_id, acao_id, responsavel_id, participantes_ids):
    _ator(ator_id, Perfil.ADMINISTRADOR)
    acao = AcaoFiscalizacao.objects.select_for_update().get(pk=acao_id) if acao_id else None
    autor = _ator(ator_id, Perfil.ADMINISTRADOR, bloquear=True)
    equipe = _equipe(responsavel_id, participantes_ids)
    solicitacao = {"origem": "administrativa", "estabelecimento": estabelecimento_id, "acao": acao_id, **equipe}
    anterior = _repeticao(autor, operacao, solicitacao)
    if anterior:
        return anterior
    _validar_fiscais([equipe["responsavel"], *equipe["participantes"]])
    estabelecimento = _estabelecimento(estabelecimento_id)
    if acao is None:
        acao = AcaoFiscalizacao.objects.create(criada_por=autor)
    inspecao = Inspecao.objects.create(
        acao=acao, estabelecimento=estabelecimento, responsavel_id=responsavel_id,
        origem=Inspecao.Origem.ADMINISTRATIVA, estado=Inspecao.Estado.ATRIBUIDA,
        criada_por=autor, operacao_criacao=operacao,
    )
    inspecao.participantes.set(equipe["participantes"])
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=autor, ato=HistoricoInspecao.Ato.ATRIBUICAO, dados={"solicitacao": solicitacao},
    )
    return inspecao


def _dados_inicio(ator, estabelecimento, versao):
    return {
        "estado": Inspecao.Estado.EM_ANDAMENTO, "iniciada_por": ator, "iniciada_em": timezone.now(),
        "versao_checklist": versao,
        "identificacao_estabelecimento": {"nome": estabelecimento.nome, "documento": estabelecimento.documento},
    }


@transaction.atomic
def iniciar_diretamente(ator_id, *, operacao, estabelecimento_id, checklist_id):
    fiscal = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    solicitacao = {"origem": "fiscal", "estabelecimento": estabelecimento_id, "checklist": checklist_id}
    anterior = _repeticao(fiscal, operacao, solicitacao)
    if anterior:
        return anterior
    estabelecimento = _estabelecimento(estabelecimento_id)
    versao = _versao(checklist_id)
    acao = AcaoFiscalizacao.objects.create(criada_por=fiscal)
    inspecao = Inspecao.objects.create(
        acao=acao, estabelecimento=estabelecimento, responsavel=fiscal, origem=Inspecao.Origem.FISCAL,
        criada_por=fiscal, operacao_criacao=operacao, **_dados_inicio(fiscal, estabelecimento, versao),
    )
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=fiscal, ato=HistoricoInspecao.Ato.INICIO,
        dados={"solicitacao": solicitacao, "versao": versao.pk},
    )
    return inspecao


@transaction.atomic
def iniciar_atribuida(ator_id, pk, *, checklist_id):
    _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = Inspecao.objects.select_for_update().get(pk=pk, responsavel_id=ator_id)
    fiscal = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    if inspecao.estado == Inspecao.Estado.EM_ANDAMENTO:
        if inspecao.iniciada_por_id == fiscal.pk and inspecao.versao_checklist.checklist_id == checklist_id:
            return
        raise InspecaoDesatualizada
    if inspecao.estado != Inspecao.Estado.ATRIBUIDA:
        raise InspecaoDesatualizada
    if motivo := bloqueio_inicio(inspecao):
        raise ValidationError(motivo)
    estabelecimento = _estabelecimento(inspecao.estabelecimento_id)
    versao = _versao(checklist_id)
    dados = _dados_inicio(fiscal, estabelecimento, versao)
    for campo, valor in dados.items():
        setattr(inspecao, campo, valor)
    inspecao.save(update_fields=list(dados))
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=fiscal, ato=HistoricoInspecao.Ato.INICIO, dados={"versao": versao.pk},
    )


def _encerrar(consulta, autor):
    return consulta.update(fim=timezone.now(), encerrado_por=autor)


@transaction.atomic
def alterar_equipe(ator_id, pk, *, revisao, responsavel_id, participantes_ids):
    _ator(ator_id, Perfil.ADMINISTRADOR)
    referencia = Inspecao.objects.only("acao_id").get(pk=pk)
    acao = AcaoFiscalizacao.objects.select_for_update().get(pk=referencia.acao_id)
    inspecao = Inspecao.objects.select_for_update().get(pk=pk)
    autor = _ator(ator_id, Perfil.ADMINISTRADOR, bloquear=True)
    if inspecao.estado == Inspecao.Estado.CANCELADA or inspecao.revisao != revisao:
        raise InspecaoDesatualizada
    anterior = _equipe(inspecao.responsavel_id, inspecao.participantes.values_list("pk", flat=True))
    atual = _equipe(responsavel_id, participantes_ids)
    if anterior == atual:
        return
    _validar_fiscais([atual["responsavel"], *atual["participantes"]])
    inspecao.responsavel_id = responsavel_id
    inspecao.revisao += 1
    inspecao.save(update_fields=["responsavel", "revisao"])
    inspecao.participantes.set(atual["participantes"])
    removidos = acao.designacoes.filter(fim__isnull=True).exclude(fiscal__in=_membros_acao(acao.pk))
    if _encerrar(removidos, autor):
        acao.revisao_supervisao += 1
        acao.save(update_fields=["revisao_supervisao"])
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=autor, ato=HistoricoInspecao.Ato.EQUIPE,
        dados={"anterior": anterior, "atual": atual},
    )


def consultar_supervisao(ator_id, pk):
    _ator(ator_id, Perfil.ADMINISTRADOR)
    acao = AcaoFiscalizacao.objects.get(pk=pk)
    historico = acao.designacoes.select_related("fiscal", "designado_por", "encerrado_por").order_by("-pk")
    return acao, _opcoes(_equipe_acao(pk)), historico


@transaction.atomic
def alterar_supervisao(ator_id, pk, *, revisao, fiscais_ids):
    _ator(ator_id, Perfil.ADMINISTRADOR)
    acao = AcaoFiscalizacao.objects.select_for_update().get(pk=pk)
    autor = _ator(ator_id, Perfil.ADMINISTRADOR, bloquear=True)
    atuais = acao.designacoes.filter(fim__isnull=True)
    existentes = set(atuais.values_list("fiscal_id", flat=True))
    escolhidos = set(fiscais_ids)
    if escolhidos == existentes:
        return
    if acao.revisao_supervisao != revisao:
        raise InspecaoDesatualizada
    _validar_fiscais(escolhidos)
    equipe = set(_equipe_acao(pk).filter(pk__in=escolhidos).values_list("pk", flat=True))
    if equipe != escolhidos:
        raise ValidationError("Selecione apenas fiscais ativos da equipe desta ação.")
    _encerrar(atuais.exclude(fiscal_id__in=escolhidos), autor)
    for fiscal_id in sorted(escolhidos - existentes):
        acao.designacoes.create(fiscal_id=fiscal_id, designado_por=autor, inicio=timezone.now())
    acao.revisao_supervisao += 1
    acao.save(update_fields=["revisao_supervisao"])
