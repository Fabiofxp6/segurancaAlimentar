from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from contas.models import Perfil, Usuario

from .models import AcaoFiscalizacao, DesignacaoSupervisor, HistoricoInspecao, Inspecao, PedidoCancelamento
from .services import _acessiveis, _ator, _equipe_acao


class CancelamentoDesatualizado(Exception):
    pass


def tem_pedido_pendente(inspecao):
    return inspecao.pedidos_cancelamento.filter(situacao=PedidoCancelamento.Situacao.PENDENTE).exists()


def _acoes_supervisionadas(ator_id):
    inspecoes = Inspecao.objects.filter(Q(responsavel_id=ator_id) | Q(participantes=ator_id))
    return DesignacaoSupervisor.objects.filter(
        fiscal_id=ator_id, fim__isnull=True, acao_id__in=inspecoes.values("acao_id"),
    ).values("acao_id")


def _visiveis(ator):
    equipe = _acessiveis(ator)
    if ator.perfil == Perfil.ADMINISTRADOR:
        return equipe
    return Inspecao.objects.filter(
        Q(pk__in=equipe.values("pk"))
        | Q(acao_id__in=_acoes_supervisionadas(ator.pk), pedidos_cancelamento__isnull=False),
    ).distinct()


def _inspecao_visivel(ator, pk):
    return _visiveis(ator).select_related("estabelecimento").get(pk=pk)


def _equipe_da_inspecao(inspecao, ator_id):
    return inspecao.responsavel_id == ator_id or inspecao.participantes.filter(pk=ator_id).exists()


def _designacoes(acao_id, solicitante_id):
    return DesignacaoSupervisor.objects.filter(acao_id=acao_id, fim__isnull=True).exclude(fiscal_id=solicitante_id)


def _elegiveis(pedido):
    acao_id = pedido.inspecao.acao_id
    return _designacoes(acao_id, pedido.solicitante_id).filter(fiscal__in=_equipe_acao(acao_id))


def _pode_decidir(ator, pedido):
    if ator.pk == pedido.solicitante_id or pedido.situacao != PedidoCancelamento.Situacao.PENDENTE:
        return False
    elegiveis = _elegiveis(pedido)
    if ator.perfil == Perfil.ADMINISTRADOR:
        return not elegiveis.exists()
    return elegiveis.filter(fiscal=ator).exists()


def listar(ator_id, pagina):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    pedidos = PedidoCancelamento.objects.filter(inspecao_id__in=_visiveis(ator).values("pk")).select_related(
        "inspecao", "solicitante",
    ).order_by("-pk")
    return Paginator(pedidos, 25).get_page(pagina)


def consultar(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _inspecao_visivel(ator, pk)
    pedidos = inspecao.pedidos_cancelamento.select_related("solicitante", "decidido_por").order_by("-pk")
    pendente = next((pedido for pedido in pedidos if pedido.situacao == PedidoCancelamento.Situacao.PENDENTE), None)
    pode_solicitar = (
        ator.perfil == Perfil.FISCALIZACAO and inspecao.estado == Inspecao.Estado.EM_ANDAMENTO
        and pendente is None and _equipe_da_inspecao(inspecao, ator.pk)
    )
    return inspecao, pedidos, pode_solicitar, pendente if pendente and _pode_decidir(ator, pendente) else None


def verificar_acesso(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    _inspecao_visivel(ator, pk)


def _bloquear_inspecao(ator, pk):
    previa = _inspecao_visivel(ator, pk)
    AcaoFiscalizacao.objects.select_for_update().get(pk=previa.acao_id)
    return Inspecao.objects.select_for_update().get(pk=pk, acao_id=previa.acao_id)


def _auditar(pedido, ator, ato, **dados):
    HistoricoInspecao.objects.create(
        inspecao=pedido.inspecao, autor=ator, ato=ato, dados={"pedido": pedido.pk, **dados},
    )


@transaction.atomic
def solicitar(ator_id, pk, *, justificativa, operacao_id):
    ator = _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = _bloquear_inspecao(ator, pk)
    ator = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    if not _equipe_da_inspecao(inspecao, ator.pk):
        raise PermissionDenied

    justificativa = justificativa.strip()
    if not justificativa:
        raise ValidationError("Informe a justificativa.")
    anterior = inspecao.pedidos_cancelamento.filter(operacao_solicitacao=operacao_id).first()
    if anterior:
        if anterior.solicitante_id != ator.pk or anterior.justificativa != justificativa:
            raise CancelamentoDesatualizado("Esta operação já foi usada com outros dados.")
        return anterior
    if inspecao.estado != Inspecao.Estado.EM_ANDAMENTO or tem_pedido_pendente(inspecao):
        raise CancelamentoDesatualizado("A inspeção não está disponível para um novo pedido.")

    pedido = inspecao.pedidos_cancelamento.create(
        solicitante=ator, justificativa=justificativa, operacao_solicitacao=operacao_id,
    )
    _auditar(pedido, ator, HistoricoInspecao.Ato.PEDIDO_CANCELAR, alteracao="pendente")
    return pedido


def _autoridade(ator, pedido):
    if ator.pk == pedido.solicitante_id:
        raise PermissionDenied
    if ator.perfil == Perfil.ADMINISTRADOR:
        candidatos = _designacoes(pedido.inspecao.acao_id, pedido.solicitante_id).values("fiscal_id")
        list(Usuario.objects.select_for_update().filter(pk__in=candidatos).order_by("pk").values_list("pk", flat=True))
        if _elegiveis(pedido).exists():
            raise PermissionDenied
        return None
    designacao = _elegiveis(pedido).filter(fiscal=ator).first()
    if designacao is None:
        raise PermissionDenied
    return designacao


def _efetivar(pedido, ator):
    inspecao = pedido.inspecao
    estado_anterior = inspecao.estado
    agora = timezone.now()
    pedido.efetivada_em = agora
    pedido.situacao = PedidoCancelamento.Situacao.EFETIVADO
    pedido.save(update_fields=["efetivada_em", "situacao"])
    inspecao.estado = Inspecao.Estado.CANCELADA
    inspecao.cancelada_em = agora
    inspecao.save(update_fields=["estado", "cancelada_em"])
    _auditar(
        pedido, ator, HistoricoInspecao.Ato.CANCELAMENTO, anterior=estado_anterior,
        atual=inspecao.estado, execucao="automatica",
    )


@transaction.atomic
def decidir(ator_id, pk, pedido_id, *, decisao, motivo_decisao, operacao_id):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _bloquear_inspecao(ator, pk)
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO, bloquear=True)
    _inspecao_visivel(ator, pk)
    pedido = inspecao.pedidos_cancelamento.get(pk=pedido_id)

    motivo_decisao = motivo_decisao.strip()
    if decisao not in (PedidoCancelamento.Situacao.APROVADO, PedidoCancelamento.Situacao.REJEITADO) or not motivo_decisao:
        raise ValidationError("Informe uma decisão e seu motivo.")
    if pedido.operacao_decisao == operacao_id:
        situacao_original = PedidoCancelamento.Situacao.APROVADO if pedido.efetivada_em else pedido.situacao
        if pedido.decidido_por_id != ator.pk or situacao_original != decisao or pedido.motivo_decisao != motivo_decisao:
            raise CancelamentoDesatualizado("Esta operação já foi usada com outros dados.")
        return pedido
    if inspecao.estado != Inspecao.Estado.EM_ANDAMENTO or pedido.situacao != PedidoCancelamento.Situacao.PENDENTE:
        raise CancelamentoDesatualizado("O pedido não está mais disponível para decisão.")

    designacao = _autoridade(ator, pedido)
    pedido.decidido_por = ator
    pedido.decidida_em = timezone.now()
    pedido.operacao_decisao = operacao_id
    pedido.motivo_decisao = motivo_decisao
    pedido.situacao = decisao
    pedido.designacao = designacao
    pedido.save(update_fields=[
        "decidido_por", "decidida_em", "operacao_decisao", "motivo_decisao", "situacao", "designacao",
    ])
    _auditar(
        pedido, ator, HistoricoInspecao.Ato.DECISAO_CANCELAR, decisao=decisao,
        designacao=pedido.designacao_id, autoridade="supervisor" if designacao else "administrador",
    )
    if decisao == PedidoCancelamento.Situacao.APROVADO:
        _efetivar(pedido, ator)
    return pedido
