from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction

from contas.autorizacao import exigir_administrador

from .models import Checklist, VersaoChecklist


class RascunhoDesatualizado(Exception):
    pass


class ItemInexistente(Exception):
    pass


def _checklist(pk, *, bloquear=False):
    consulta = Checklist.objects.select_for_update() if bloquear else Checklist.objects
    return consulta.get(pk=pk)


def _conferir_revisao(checklist, revisao):
    if checklist.revisao != revisao:
        raise RascunhoDesatualizado


def _item(itens, item_id):
    item = next((item for item in itens if item["id"] == str(item_id)), None)
    if item is None:
        raise ItemInexistente
    return item


def listar(ator_id, pagina):
    exigir_administrador(ator_id)
    return Paginator(Checklist.objects.defer("itens", "regras").order_by("titulo", "pk"), 25).get_page(pagina)


def consultar(ator_id, pk):
    exigir_administrador(ator_id)
    checklist = _checklist(pk)
    versoes = list(checklist.versoes.values("pk", "numero", "publicado_em").order_by("-numero"))
    return checklist, versoes


def consultar_item(ator_id, pk, item_id):
    exigir_administrador(ator_id)
    checklist = _checklist(pk)
    item = _item(checklist.itens, item_id) if item_id else None
    return checklist, item


def consultar_versao(ator_id, pk, versao_pk):
    exigir_administrador(ator_id)
    return VersaoChecklist.objects.select_related("publicado_por").get(pk=versao_pk, checklist_id=pk)


@transaction.atomic
def criar(ator_id, *, titulo, referencia, regras):
    autor = exigir_administrador(ator_id, bloquear=True)
    return Checklist.objects.create(titulo=titulo, referencia=referencia, regras=regras, criado_por=autor)


@transaction.atomic
def editar(ator_id, pk, *, revisao, titulo, referencia, regras):
    exigir_administrador(ator_id, bloquear=True)
    checklist = _checklist(pk, bloquear=True)
    _conferir_revisao(checklist, revisao)
    if (checklist.titulo, checklist.referencia, checklist.regras) != (titulo, referencia, regras):
        checklist.titulo, checklist.referencia, checklist.regras = titulo, referencia, regras
        checklist.revisao += 1
        checklist.save(update_fields=["titulo", "referencia", "regras", "revisao"])


@transaction.atomic
def salvar_item(ator_id, pk, item_id, *, revisao, enunciado, ordem, peso, obrigatorio, opcoes):
    exigir_administrador(ator_id, bloquear=True)
    checklist = _checklist(pk, bloquear=True)
    _conferir_revisao(checklist, revisao)
    anterior = _item(checklist.itens, item_id) if item_id else None
    demais = [item for item in checklist.itens if item != anterior]
    if any(item["ordem"] == ordem for item in demais):
        raise ValidationError({"ordem": "Esta ordem já é usada por outro item."})

    novo = {
        "id": anterior["id"] if anterior else str(uuid4()),
        "enunciado": enunciado, "ordem": ordem, "peso": str(peso) if peso is not None else None,
        "obrigatorio": obrigatorio, "opcoes": opcoes,
    }
    if novo != anterior:
        checklist.itens = sorted([*demais, novo], key=lambda item: item["ordem"])
        checklist.revisao += 1
        checklist.save(update_fields=["itens", "revisao"])


@transaction.atomic
def remover_item(ator_id, pk, item_id, *, revisao):
    exigir_administrador(ator_id, bloquear=True)
    checklist = _checklist(pk, bloquear=True)
    _conferir_revisao(checklist, revisao)
    item = _item(checklist.itens, item_id)
    checklist.itens.remove(item)
    checklist.revisao += 1
    checklist.save(update_fields=["itens", "revisao"])


@transaction.atomic
def publicar(ator_id, pk, *, revisao):
    autor = exigir_administrador(ator_id, bloquear=True)
    checklist = _checklist(pk, bloquear=True)
    existente = checklist.versoes.filter(revisao_rascunho=revisao).first()
    if existente:
        return existente
    _conferir_revisao(checklist, revisao)
    if not checklist.itens:
        raise ValidationError("Inclua pelo menos um item antes de publicar.")
    ultimo_numero = checklist.versoes.order_by("-numero").values_list("numero", flat=True).first()
    return checklist.versoes.create(
        numero=(ultimo_numero or 0) + 1, revisao_rascunho=checklist.revisao,
        titulo=checklist.titulo, referencia=checklist.referencia, regras=checklist.regras,
        itens=checklist.itens, publicado_por=autor,
    )
