from django.core.paginator import Paginator
from django.db import transaction

from contas.autorizacao import exigir_administrador

from .models import Estabelecimento, HistoricoEstabelecimento


CAMPOS_CADASTRAIS = ("nome", "documento", "endereco", "contato", "ativo")


class CadastroDesatualizado(Exception):
    pass


def listar(ator_id, pagina):
    exigir_administrador(ator_id)
    cadastros = Estabelecimento.objects.order_by("nome", "pk")
    return Paginator(cadastros, 25).get_page(pagina)


def consultar(ator_id, estabelecimento_id):
    exigir_administrador(ator_id)
    return Estabelecimento.objects.get(pk=estabelecimento_id)


@transaction.atomic
def criar(ator_id, *, nome, documento, endereco, contato):
    autor = exigir_administrador(ator_id, bloquear=True)
    cadastro = Estabelecimento.objects.create(
        nome=nome, documento=documento, endereco=endereco, contato=contato,
    )
    HistoricoEstabelecimento.objects.create(
        estabelecimento=cadastro,
        autor=autor,
        versao=cadastro.versao,
        alteracoes={campo: {"atual": getattr(cadastro, campo)} for campo in CAMPOS_CADASTRAIS},
    )
    return cadastro


@transaction.atomic
def editar(ator_id, estabelecimento_id, *, versao, nome, documento, endereco, contato, ativo):
    autor = exigir_administrador(ator_id, bloquear=True)
    cadastro = Estabelecimento.objects.select_for_update().get(pk=estabelecimento_id)
    if versao != cadastro.versao:
        raise CadastroDesatualizado

    valores = {
        "nome": nome, "documento": documento, "endereco": endereco, "contato": contato, "ativo": ativo,
    }
    alteracoes = {
        campo: {"anterior": getattr(cadastro, campo), "atual": valor}
        for campo, valor in valores.items()
        if valor != getattr(cadastro, campo)
    }
    if alteracoes:
        for campo in alteracoes:
            setattr(cadastro, campo, valores[campo])
        cadastro.versao += 1
        cadastro.save(update_fields=[*alteracoes, "versao"])
        HistoricoEstabelecimento.objects.create(
            estabelecimento=cadastro, autor=autor, versao=cadastro.versao, alteracoes=alteracoes,
        )
    return cadastro
