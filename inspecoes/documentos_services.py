from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

from contas.models import Perfil
from contas.vinculos import estabelecimentos_acessiveis
from estabelecimentos.models import Estabelecimento

from .cancelamento_services import tem_pedido_pendente
from .models import DocumentoEstabelecimento, Inspecao
from .services import _acessiveis, _ator


JANELA_ENVIO = (Inspecao.Estado.ATRIBUIDA, Inspecao.Estado.EM_ANDAMENTO)


class DocumentoDesatualizado(Exception):
    pass


def _inspecoes_unidade(ator_id):
    unidades = estabelecimentos_acessiveis(ator_id).values("pk")
    return Inspecao.objects.filter(estabelecimento_id__in=unidades)


def _visiveis_unidade(ator_id):
    return _inspecoes_unidade(ator_id).filter(
        Q(estado__in=JANELA_ENVIO) | Q(documentos_estabelecimento__isnull=False),
    ).distinct()


def listar(ator_id, pagina):
    _ator(ator_id, Perfil.ESTABELECIMENTO)
    inspecoes = _visiveis_unidade(ator_id).select_related("estabelecimento").order_by("-pk")
    return Paginator(inspecoes, 25).get_page(pagina)


def _consultar_inspecao(ator_id, pk):
    ator = _ator(ator_id, Perfil.ESTABELECIMENTO, Perfil.FISCALIZACAO)
    consulta = _visiveis_unidade(ator_id) if ator.perfil == Perfil.ESTABELECIMENTO else _acessiveis(ator)
    inspecao = consulta.select_related("estabelecimento").get(pk=pk)
    return ator, inspecao


def consultar_pagina(ator_id, pk):
    ator, inspecao = _consultar_inspecao(ator_id, pk)
    documentos = inspecao.documentos_estabelecimento.defer("conteudo").select_related("autor").order_by("-pk")
    cliente = ator.perfil == Perfil.ESTABELECIMENTO
    janela = cliente and inspecao.estado in JANELA_ENVIO
    bloqueado = janela and tem_pedido_pendente(inspecao)
    return inspecao, documentos, cliente, janela and not bloqueado, bloqueado


def verificar_envio(ator_id, pk):
    _ator(ator_id, Perfil.ESTABELECIMENTO)
    _visiveis_unidade(ator_id).get(pk=pk)


def baixar(ator_id, pk, documento_id):
    _, inspecao = _consultar_inspecao(ator_id, pk)
    return inspecao.documentos_estabelecimento.get(pk=documento_id)


@transaction.atomic
def salvar(ator_id, pk, *, operacao_id, descricao, metadados, conteudo):
    _ator(ator_id, Perfil.ESTABELECIMENTO)
    inspecao = _inspecoes_unidade(ator_id).select_for_update().get(pk=pk)
    autor = _ator(ator_id, Perfil.ESTABELECIMENTO, bloquear=True)
    if not Estabelecimento.objects.select_for_update().filter(pk=inspecao.estabelecimento_id, ativo=True).exists():
        raise Inspecao.DoesNotExist
    if not estabelecimentos_acessiveis(ator_id).filter(pk=inspecao.estabelecimento_id).exists():
        raise Inspecao.DoesNotExist

    anterior = inspecao.documentos_estabelecimento.defer("conteudo").filter(operacao_id=operacao_id).first()
    if anterior:
        if (
            anterior.autor_id != autor.pk or anterior.descricao != descricao
            or anterior.sha256 != metadados["sha256"] or anterior.nome != metadados["nome"]
        ):
            raise DocumentoDesatualizado("Este envio já foi usado com outros dados.")
        return anterior
    if inspecao.estado not in JANELA_ENVIO:
        raise ValidationError("O prazo de envio de documentos desta inspeção terminou.")
    if tem_pedido_pendente(inspecao):
        raise DocumentoDesatualizado("O envio de documentos está temporariamente bloqueado.")
    return DocumentoEstabelecimento.objects.create(
        inspecao=inspecao, autor=autor, operacao_id=operacao_id, descricao=descricao, conteudo=conteudo,
        **metadados,
    )
