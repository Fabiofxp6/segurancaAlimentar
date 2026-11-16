from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction

from contas.models import Perfil

from .models import HistoricoInspecao, Inspecao, ReanaliseDocumento
from .resultados import atual
from .services import InspecaoDesatualizada, _acessiveis, _ator


def _inspecao(ator, pk, *, bloquear=False):
    consulta = Inspecao.objects.filter(pk__in=_acessiveis(ator).values("pk"), estado=Inspecao.Estado.CONCLUIDA)
    if bloquear:
        consulta = consulta.select_for_update()
    return consulta.get(pk=pk)


def _documentos(inspecao):
    return inspecao.documentos_estabelecimento.filter(complemento=True).select_related(
        "reanalise__autor", "reanalise__base",
    ).defer("conteudo", "reanalise__base__respostas_utilizadas")


def verificar_acesso(ator_id, pk):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    return ator, _inspecao(ator, pk)


def listar(ator_id, pk, pagina):
    _, inspecao = verificar_acesso(ator_id, pk)
    docs = _documentos(inspecao).order_by("-pk")
    return inspecao, Paginator(docs, 25).get_page(pagina)


def consultar(ator_id, pk, documento_id):
    ator, inspecao = verificar_acesso(ator_id, pk)
    documento = _documentos(inspecao).filter(pk=documento_id).first()
    if documento is None:
        raise Inspecao.DoesNotExist
    reanalise = getattr(documento, "reanalise", None)
    base = atual(inspecao)
    fiscal = ator.perfil == Perfil.FISCALIZACAO
    itens = base.versao_checklist.itens if (
        fiscal and reanalise and reanalise.indica_correcao and reanalise.base_id == base.pk
    ) else []
    return {
        "inspecao": inspecao, "documento": documento, "reanalise": reanalise, "base": base,
        "itens": itens, "pode_registrar": fiscal and reanalise is None, "fiscal": fiscal,
    }


@transaction.atomic
def registrar(ator_id, pk, documento_id, *, base_id, parecer, indica_correcao, operacao_id):
    ator = _ator(ator_id, Perfil.FISCALIZACAO)
    inspecao = _inspecao(ator, pk, bloquear=True)
    ator = _ator(ator_id, Perfil.FISCALIZACAO, bloquear=True)
    if not _acessiveis(ator).filter(pk=pk).exists():
        raise Inspecao.DoesNotExist
    documento = _documentos(inspecao).filter(pk=documento_id).first()
    if documento is None:
        raise Inspecao.DoesNotExist
    parecer = parecer.strip()
    if not parecer:
        raise ValidationError("Informe o parecer.")
    anterior = getattr(documento, "reanalise", None)
    if anterior is not None:
        if (anterior.autor_id, anterior.base_id, anterior.parecer, anterior.indica_correcao, anterior.operacao_id) == (
            ator.pk, base_id, parecer, indica_correcao, operacao_id,
        ):
            return anterior
        raise InspecaoDesatualizada("Já existe um parecer registrado para este documento.")
    base = atual(inspecao)
    if base.pk != base_id:
        raise InspecaoDesatualizada("A revisão mudou. Reabra o documento e confira o resultado.")
    reanalise = ReanaliseDocumento.objects.create(
        documento=documento, base=base, autor=ator, indica_correcao=indica_correcao,
        parecer=parecer, operacao_id=operacao_id,
    )
    HistoricoInspecao.objects.create(
        inspecao=inspecao, autor=ator, ato=HistoricoInspecao.Ato.REANALISE,
        dados={"documento": documento.pk, "reanalise": reanalise.pk, "base": base.revisao, "indica_correcao": indica_correcao},
    )
    return reanalise


def referencia_correcao(inspecao, base, reanalise_id):
    reanalise = ReanaliseDocumento.objects.filter(
        pk=reanalise_id, base=base, documento__inspecao=inspecao, indica_correcao=True,
    ).first()
    if reanalise is None:
        raise Inspecao.DoesNotExist
    return reanalise
