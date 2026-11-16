from django.core.paginator import Paginator
from django.db.models import Case, F, Value, When

from contas.models import Perfil

from .models import DesignacaoSupervisor, DocumentoEstabelecimento, HistoricoInspecao, OperacaoCampo
from .services import _acessiveis, _ator


def _rotulos(campo, opcoes):
    return Case(
        *(When(**{campo: valor}, then=Value(rotulo)) for valor, rotulo in opcoes),
        default=Value("Registro"),
    )


def _eventos(consulta, *, data, autor, fonte, evento):
    return consulta.order_by().annotate(
        ocorreu_em=F(data), ator_nome=F(autor), fonte=Value(fonte), evento=evento,
    ).values("ocorreu_em", "ator_nome", "fonte", "evento", "pk")


def listar(ator_id, pk, pagina):
    ator = _ator(ator_id, Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    inspecao = _acessiveis(ator).get(pk=pk)
    historico = _eventos(
        HistoricoInspecao.objects.filter(inspecao=inspecao),
        data="registrado_em", autor="autor__username", fonte="Inspeção",
        evento=_rotulos("ato", HistoricoInspecao.Ato.choices),
    )
    designacoes = DesignacaoSupervisor.objects.filter(acao=inspecao.acao)
    inicio_designacao = _eventos(
        designacoes, data="inicio", autor="designado_por__username",
        fonte="Supervisão", evento=Value("Designação iniciada"),
    )
    fim_designacao = _eventos(
        designacoes.filter(fim__isnull=False), data="fim", autor="encerrado_por__username",
        fonte="Supervisão", evento=Value("Designação encerrada"),
    )
    campo = _eventos(
        OperacaoCampo.objects.filter(inspecao=inspecao), data="confirmado_em", autor="autor__username",
        fonte="Checklist em campo", evento=_rotulos("tipo", [
            (OperacaoCampo.Tipo.RESPOSTA, "Resposta confirmada"),
            (OperacaoCampo.Tipo.EVIDENCIA, "Evidência confirmada"),
        ]),
    )
    documentos = _eventos(
        DocumentoEstabelecimento.objects.filter(inspecao=inspecao),
        data="recebido_em", autor="autor__username", fonte="Estabelecimento",
        evento=Value("Documento recebido"),
    )
    trilha = historico.union(inicio_designacao, fim_designacao, campo, documentos, all=True).order_by(
        "-ocorreu_em", "fonte", "-pk", "evento",
    )
    return inspecao, Paginator(trilha, 25).get_page(pagina)
