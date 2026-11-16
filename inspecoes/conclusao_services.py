import json
from hashlib import sha256

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from contas.models import Perfil

from . import pontuacao
from .cancelamento_services import tem_pedido_pendente
from .resultados import atual
from .models import HistoricoInspecao, Inspecao, ResultadoInspecao
from .services import _acessiveis, _ator


class ConclusaoDesatualizada(Exception):
    pass


def _inspecao(ator, pk, *, bloquear=False):
    consulta = Inspecao.objects.filter(pk__in=_acessiveis(ator).values("pk")).select_related("versao_checklist")
    if bloquear:
        consulta = consulta.select_for_update(of=("self",))
    return consulta.get(pk=pk)


def _respostas(inspecao):
    return {
        str(item_id): {"opcao": opcao, "revisao": revisao}
        for item_id, opcao, revisao in inspecao.respostas_campo.values_list("item_id", "opcao", "revisao")
    }


def _revisao(inspecao, respostas):
    dados = json.dumps([inspecao.versao_checklist_id, respostas], sort_keys=True, ensure_ascii=False)
    return sha256(dados.encode()).hexdigest()


def _faltantes(inspecao, respostas):
    return [
        item for item in inspecao.versao_checklist.itens
        if item.get("obrigatorio") and item["id"] not in respostas
    ]


def verificar_acesso(ator_id, pk):
    ator = _ator(ator_id, Perfil.FISCALIZACAO)
    _inspecao(ator, pk)


def consultar(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _inspecao(ator, pk)
    if inspecao.estado == Inspecao.Estado.CONCLUIDA:
        resultado = atual(inspecao)
        return {"inspecao": inspecao, "resultado": resultado}
    if ator.perfil != Perfil.FISCALIZACAO:
        raise PermissionDenied
    if inspecao.estado != Inspecao.Estado.EM_ANDAMENTO:
        return {"inspecao": inspecao, "indisponivel": True}

    respostas = _respostas(inspecao)
    bloqueada = tem_pedido_pendente(inspecao)
    faltantes = _faltantes(inspecao, respostas)
    return {
        "inspecao": inspecao, "faltantes": faltantes, "bloqueada": bloqueada,
        "respondidos": len(respostas), "pode_concluir": not (bloqueada or faltantes),
        "revisao_base": _revisao(inspecao, respostas), "itens": inspecao.versao_checklist.itens,
    }


@transaction.atomic
def concluir(ator_id, pk, *, operacao_id, revisao_base):
    ator = _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = _inspecao(ator, pk, bloquear=True)
    ator = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    if not _acessiveis(ator).filter(pk=pk).exists():
        raise Inspecao.DoesNotExist

    if inspecao.estado == Inspecao.Estado.CONCLUIDA:
        anterior = inspecao.resultados.get(revisao=1)
        if (
            anterior.operacao_id == operacao_id and anterior.concluido_por_id == ator.pk
            and anterior.revisao_base == revisao_base
        ):
            return anterior
    if inspecao.estado != Inspecao.Estado.EM_ANDAMENTO or tem_pedido_pendente(inspecao):
        raise ConclusaoDesatualizada("A inspeção não está disponível para conclusão. Confira a situação atual.")

    respostas = _respostas(inspecao)
    if _revisao(inspecao, respostas) != revisao_base:
        raise ConclusaoDesatualizada("As respostas mudaram. Reabra a revisão antes de concluir.")
    if _faltantes(inspecao, respostas):
        raise ConclusaoDesatualizada("Responda os itens obrigatórios antes de concluir.")

    versao = inspecao.versao_checklist
    try:
        nota, classificacao = pontuacao.calcular(versao, respostas)
    except ValidationError as erro:
        raise ConclusaoDesatualizada(" ".join(erro.messages)) from erro

    resultado = ResultadoInspecao.objects.create(
        inspecao=inspecao, versao_checklist=versao, regra_pontuacao=versao.regra_pontuacao,
        pontuacao=nota, classificacao=classificacao, respostas_utilizadas=respostas, revisao_base=revisao_base,
        concluido_por=ator, operacao_id=operacao_id,
    )
    inspecao.estado = Inspecao.Estado.CONCLUIDA
    inspecao.save(update_fields=["estado"])
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=ator, ato=HistoricoInspecao.Ato.CONCLUSAO, dados={
            "anterior": Inspecao.Estado.EM_ANDAMENTO, "atual": inspecao.estado, "resultado": resultado.pk,
            "versao": versao.pk, "regra": versao.regra_pontuacao, "classificacao": classificacao,
            "pontuacao": str(nota) if nota is not None else None,
        },
    )
    return resultado
