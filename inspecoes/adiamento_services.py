from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from contas.models import Perfil

from .models import AcaoFiscalizacao, HistoricoInspecao, Inspecao, PedidoAdiamento
from .services import (
    InspecaoDesatualizada, _acessiveis, _ator, acoes_supervisionadas, autoridade_decisao, supervisores_elegiveis,
)


def _visiveis(ator):
    equipe = _acessiveis(ator)
    if ator.perfil == Perfil.ADMINISTRADOR:
        return equipe
    return Inspecao.objects.filter(
        Q(pk__in=equipe.values("pk"))
        | Q(acao_id__in=acoes_supervisionadas(ator.pk), pedidos_adiamento__isnull=False),
    ).distinct()


def listar(ator_id, pagina):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    pedidos = PedidoAdiamento.objects.filter(inspecao_id__in=_visiveis(ator).values("pk"))
    return Paginator(pedidos.order_by("-pk"), 25).get_page(pagina)


def verificar_acesso(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    return ator, _visiveis(ator).get(pk=pk)


def consultar(ator_id, pk):
    ator, inspecao = verificar_acesso(ator_id, pk)
    pedidos = inspecao.pedidos_adiamento.select_related("solicitante", "decidido_por").order_by("-pk")
    pendente = pedidos.filter(situacao=PedidoAdiamento.Situacao.PENDENTE).first()
    pode_decidir = False
    if pendente and ator.pk != pendente.solicitante_id:
        elegiveis = supervisores_elegiveis(inspecao.acao_id, pendente.solicitante_id)
        pode_decidir = (
            not elegiveis.exists() if ator.perfil == Perfil.ADMINISTRADOR
            else elegiveis.filter(fiscal=ator).exists()
        )
    return {
        "inspecao": inspecao, "pedidos": pedidos, "decidivel": pendente if pode_decidir else None,
        "pode_solicitar": (
            ator.perfil == Perfil.FISCALIZACAO and pendente is None
            and inspecao.estado == Inspecao.Estado.ATRIBUIDA and _acessiveis(ator).filter(pk=pk).exists()
        ),
    }


@transaction.atomic
def solicitar(ator_id, pk, *, data_proposta, justificativa, operacao_id):
    _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = Inspecao.objects.select_for_update().get(pk=pk)
    fiscal = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    if not _acessiveis(fiscal).filter(pk=pk).exists():
        raise Inspecao.DoesNotExist
    justificativa = justificativa.strip()
    if not justificativa:
        raise ValidationError("Informe a justificativa.")
    anterior = inspecao.pedidos_adiamento.filter(operacao_id=operacao_id).first()
    if anterior:
        if (anterior.solicitante_id, anterior.data_proposta, anterior.justificativa) != (
            fiscal.pk, data_proposta, justificativa,
        ):
            raise InspecaoDesatualizada("Esta operação já foi usada com outros dados.")
        return anterior
    if inspecao.estado != Inspecao.Estado.ATRIBUIDA or inspecao.pedidos_adiamento.filter(
        situacao=PedidoAdiamento.Situacao.PENDENTE,
    ).exists():
        raise InspecaoDesatualizada("A inspeção não está disponível para um novo pedido de adiamento.")
    if data_proposta <= timezone.now() or (inspecao.agendada_em and data_proposta <= inspecao.agendada_em):
        raise ValidationError("Informe uma data futura e posterior à data já agendada, se houver.")
    pedido = inspecao.pedidos_adiamento.create(
        solicitante=fiscal, justificativa=justificativa, data_proposta=data_proposta, operacao_id=operacao_id,
    )
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=fiscal, ato=HistoricoInspecao.Ato.ADIAMENTO_PEDIDO,
        dados={"pedido": pedido.pk, "data_proposta": data_proposta.isoformat()},
    )
    return pedido


@transaction.atomic
def decidir(ator_id, pk, pedido_id, *, decisao, motivo, operacao_id):
    _, previa = verificar_acesso(ator_id, pk)
    AcaoFiscalizacao.objects.select_for_update().get(pk=previa.acao_id)
    inspecao = Inspecao.objects.select_for_update().get(pk=pk)
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO, bloquear=True)
    if not _visiveis(ator).filter(pk=pk).exists():
        raise Inspecao.DoesNotExist
    pedido = inspecao.pedidos_adiamento.filter(pk=pedido_id).first()
    if pedido is None:
        raise Inspecao.DoesNotExist
    if ator.pk == pedido.solicitante_id:
        raise PermissionDenied
    motivo = motivo.strip()
    if not motivo or decisao not in (PedidoAdiamento.Situacao.APROVADO, PedidoAdiamento.Situacao.REJEITADO):
        raise ValidationError("Informe a decisão e seu motivo.")
    if pedido.operacao_decisao == operacao_id:
        if (pedido.decidido_por_id, pedido.situacao, pedido.motivo_decisao) != (ator.pk, decisao, motivo):
            raise InspecaoDesatualizada("Esta operação já foi usada com outros dados.")
        return pedido
    if inspecao.estado != Inspecao.Estado.ATRIBUIDA or pedido.situacao != PedidoAdiamento.Situacao.PENDENTE:
        raise InspecaoDesatualizada("O pedido não está mais disponível para decisão.")
    designacao = autoridade_decisao(ator, inspecao, pedido.solicitante_id)
    agora = timezone.now()
    dados = {"pedido": pedido.pk, "decisao": decisao, "designacao": designacao.pk if designacao else None}
    if decisao == PedidoAdiamento.Situacao.APROVADO:
        if pedido.data_proposta <= agora:
            raise ValidationError("A data proposta passou. Rejeite o pedido para permitir nova solicitação.")
        anterior = inspecao.agendada_em
        dados.update(data_anterior=anterior.isoformat() if anterior else None, data_nova=pedido.data_proposta.isoformat())
        inspecao.agendada_em = pedido.data_proposta
        inspecao.save(update_fields=["agendada_em"])
    pedido.situacao = decisao
    pedido.decidido_por = ator
    pedido.decidida_em = agora
    pedido.motivo_decisao = motivo
    pedido.operacao_decisao = operacao_id
    pedido.designacao = designacao
    pedido.save(update_fields=[
        "situacao", "decidido_por", "decidida_em", "motivo_decisao", "operacao_decisao", "designacao",
    ])
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=ator, ato=HistoricoInspecao.Ato.ADIAMENTO_DECISAO, dados=dados,
    )
    return pedido
