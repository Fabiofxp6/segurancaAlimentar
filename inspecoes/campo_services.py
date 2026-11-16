import json
from hashlib import sha256

from django.core.exceptions import ValidationError
from django.db import transaction

from contas.models import Perfil

from .cancelamento_services import tem_pedido_pendente
from .models import EvidenciaCampo, Inspecao, OperacaoCampo, RespostaCampo
from .services import _ator


class CampoDesatualizado(Exception):
    pass


def _inspecao(autor_id, inspecao_id, *, bloquear=False):
    _ator(autor_id, Perfil.FISCALIZACAO)
    consulta = Inspecao.objects.select_related("versao_checklist").filter(
        pk=inspecao_id, estado__in=[Inspecao.Estado.EM_ANDAMENTO, Inspecao.Estado.CANCELADA, Inspecao.Estado.CONCLUIDA],
    )
    if bloquear:
        consulta = consulta.select_for_update(of=("self",))
    inspecao = consulta.get()
    if inspecao.responsavel_id != autor_id and not inspecao.participantes.filter(pk=autor_id).exists():
        raise Inspecao.DoesNotExist
    if bloquear:
        _ator(autor_id, Perfil.FISCALIZACAO, bloquear=True)
    return inspecao


def pode_gravar(inspecao):
    return inspecao.estado == Inspecao.Estado.EM_ANDAMENTO and not tem_pedido_pendente(inspecao)


def _exigir_gravacao(inspecao):
    if not pode_gravar(inspecao):
        raise CampoDesatualizado("Novos registros estão bloqueados nesta inspeção.")


def _item(inspecao, item_id):
    for item in inspecao.versao_checklist.itens:
        if item.get("id") == str(item_id):
            return item
    raise Inspecao.DoesNotExist


def _resposta(inspecao, item_id):
    return inspecao.respostas_campo.filter(item_id=item_id).first()


def consultar_lista(autor_id, inspecao_id):
    inspecao = _inspecao(autor_id, inspecao_id)
    respondidos = set(str(item_id) for item_id in inspecao.respostas_campo.values_list("item_id", flat=True))
    return inspecao, [
        {**item, "salva": item["id"] in respondidos}
        for item in inspecao.versao_checklist.itens if item.get("id")
    ]


def consultar_item(autor_id, inspecao_id, item_id):
    inspecao = _inspecao(autor_id, inspecao_id)
    return inspecao, _item(inspecao, item_id), _resposta(inspecao, item_id)


def consultar_pagina(autor_id, inspecao_id, item_id):
    inspecao, item, resposta = consultar_item(autor_id, inspecao_id, item_id)
    evidencias = resposta.evidencias.defer("conteudo").order_by("pk") if resposta else []
    return inspecao, item, resposta, evidencias


def baixar(autor_id, inspecao_id, item_id, evidencia_id):
    _, _, resposta = consultar_item(autor_id, inspecao_id, item_id)
    if resposta is None:
        raise EvidenciaCampo.DoesNotExist
    return resposta.evidencias.get(pk=evidencia_id)


def _operacao(inspecao, item_id, autor_id, operacao_id, tipo, dados):
    conteudo = json.dumps(dados, sort_keys=True, ensure_ascii=False).encode()
    impressao = sha256(conteudo).hexdigest()
    gravada = OperacaoCampo.objects.filter(inspecao=inspecao, operacao_id=operacao_id).first()
    if gravada and (
        gravada.impressao != impressao or gravada.item_id != item_id
        or gravada.autor_id != autor_id or gravada.tipo != tipo
    ):
        raise CampoDesatualizado("Este envio já foi usado com outros dados.")
    return gravada, {
        "inspecao": inspecao, "item_id": item_id, "autor_id": autor_id, "operacao_id": operacao_id,
        "tipo": tipo, "impressao": impressao, "dados": dados,
    }


@transaction.atomic
def salvar_resposta(autor_id, inspecao_id, item_id, *, operacao_id, revisao, opcao, observacao, descricao_irregularidade):
    inspecao = _inspecao(autor_id, inspecao_id, bloquear=True)
    item = _item(inspecao, item_id)
    if opcao not in item["opcoes"]:
        raise ValidationError("Escolha uma opção do checklist desta inspeção.")
    valores = {"opcao": opcao, "observacao": observacao, "descricao_irregularidade": descricao_irregularidade}
    anterior, operacao = _operacao(
        inspecao, item_id, autor_id, operacao_id, OperacaoCampo.Tipo.RESPOSTA, {**valores, "revisao": revisao},
    )
    if anterior:
        return anterior

    _exigir_gravacao(inspecao)
    resposta = _resposta(inspecao, item_id)
    if revisao != (resposta.revisao if resposta else 0):
        raise CampoDesatualizado("A resposta mudou em outra tela. Confira a versão atual antes de salvar.")
    nova_revisao = revisao + 1
    RespostaCampo.objects.update_or_create(
        inspecao=inspecao, item_id=item_id,
        defaults={**valores, "revisao": nova_revisao, "alterada_por_id": autor_id},
    )
    return OperacaoCampo.objects.create(**operacao, resultado={
        "revisao": nova_revisao, "ha_irregularidade": bool(descricao_irregularidade),
    })


@transaction.atomic
def salvar_evidencia(autor_id, inspecao_id, item_id, *, operacao_id, revisao, vinculo, metadados, conteudo):
    inspecao = _inspecao(autor_id, inspecao_id, bloquear=True)
    _item(inspecao, item_id)
    anterior, operacao = _operacao(
        inspecao, item_id, autor_id, operacao_id, OperacaoCampo.Tipo.EVIDENCIA,
        {**metadados, "vinculo": vinculo, "revisao": revisao},
    )
    if anterior:
        return anterior
    _exigir_gravacao(inspecao)
    resposta = _resposta(inspecao, item_id)
    if resposta is None or resposta.revisao != revisao:
        raise CampoDesatualizado("Confira a resposta confirmada antes de anexar a foto.")
    if vinculo == EvidenciaCampo.Vinculo.IRREGULARIDADE and not resposta.descricao_irregularidade:
        raise ValidationError("Salve a irregularidade antes de vinculá-la a uma foto.")
    evidencia = EvidenciaCampo.objects.create(
        resposta=resposta, vinculo=vinculo, autor_id=autor_id, conteudo=conteudo,
        nome=metadados["nome"], mime=metadados["mime"], tamanho=metadados["tamanho"],
        descricao_irregularidade=(
            resposta.descricao_irregularidade if vinculo == EvidenciaCampo.Vinculo.IRREGULARIDADE else ""
        ),
    )
    return OperacaoCampo.objects.create(**operacao, resultado={
        "evidencia_id": evidencia.pk, "nome": evidencia.nome, "vinculo": evidencia.get_vinculo_display(),
    })
