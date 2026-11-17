from collections import Counter
from datetime import datetime, time

from django.core.paginator import Paginator
from django.db.models import Avg, Count, OuterRef, Q, Subquery
from django.db.models.functions import Trim
from django.utils import timezone

from checklists.models import VersaoChecklist
from contas.models import Perfil, Usuario
from estabelecimentos.models import Estabelecimento

from .models import Inspecao, RespostaCampo, ResultadoInspecao
from .services import _acessiveis, _ator, _opcoes


def _escopo(ator_id, painel=False):
    perfis = (Perfil.ADMINISTRADOR,) if painel else (Perfil.ADMINISTRADOR, Perfil.FISCALIZACAO)
    ator = _ator(ator_id, *perfis)
    return ator, _acessiveis(ator)


def opcoes(ator_id, *, painel=False):
    ator, escopo = _escopo(ator_id, painel)
    ids = escopo.values("pk")
    unidades = Estabelecimento.objects.filter(inspecao__in=ids).distinct()
    equipe = Usuario.objects.filter(
        Q(inspecoes_responsavel__in=ids) | Q(inspecoes_participante__in=ids),
    ).distinct()
    return ator.perfil, {"estabelecimentos": _opcoes(unidades, "nome"), "fiscais": _opcoes(equipe)}


def _filtrar(escopo, *, estado, estabelecimento, fiscal, inicio, fim):
    if estado:
        escopo = escopo.filter(estado=estado)
    if estabelecimento:
        escopo = escopo.filter(estabelecimento_id=estabelecimento)
    if fiscal:
        participacoes = Inspecao.objects.filter(participantes=fiscal).values("pk")
        escopo = escopo.filter(Q(responsavel_id=fiscal) | Q(pk__in=participacoes))
    if inicio:
        escopo = escopo.filter(criada_em__gte=timezone.make_aware(datetime.combine(inicio, time.min)))
    if fim:
        escopo = escopo.filter(criada_em__lte=timezone.make_aware(datetime.combine(fim, time.max)))
    return escopo


def listar(ator_id, *, pagina, busca="", recorte="", **filtros):
    _, escopo = _escopo(ator_id)
    consulta = _filtrar(escopo, **filtros)
    if recorte == "finalizadas":
        consulta = consulta.filter(estado__in=(Inspecao.Estado.CONCLUIDA, Inspecao.Estado.CANCELADA))
    if busca:
        termo = busca.removeprefix("#")
        if termo.isascii() and termo.isdecimal() and len(termo) <= 19:
            consulta = consulta.filter(pk=int(termo))
        else:
            consulta = consulta.filter(
                Q(identificacao_estabelecimento__nome__icontains=busca)
                | Q(identificacao_estabelecimento__isnull=True, estabelecimento__nome__icontains=busca),
            )
    consulta = consulta.select_related("estabelecimento", "responsavel").order_by("-pk")
    return Paginator(consulta, 25).get_page(pagina)


def _resultados_atuais(inspecoes):
    concluidas = inspecoes.filter(estado=Inspecao.Estado.CONCLUIDA).values("pk")
    ultima = ResultadoInspecao.objects.filter(inspecao_id=OuterRef("inspecao_id")).order_by("-revisao").values("pk")[:1]
    return ResultadoInspecao.objects.filter(inspecao_id__in=concluidas, pk=Subquery(ultima))


def _resultados_por_versao(resultados):
    return resultados.values(
        "versao_checklist_id", "versao_checklist__checklist_id", "versao_checklist__titulo",
        "versao_checklist__numero", "regra_pontuacao",
    ).annotate(
        total=Count("pk"),
        media=Avg("pontuacao"),
        satisfatorias=Count("pk", filter=Q(classificacao=ResultadoInspecao.Classificacao.SATISFATORIA)),
        regulares=Count("pk", filter=Q(classificacao=ResultadoInspecao.Classificacao.REGULAR)),
        insatisfatorias=Count("pk", filter=Q(classificacao=ResultadoInspecao.Classificacao.INSATISFATORIA)),
        sem_pontuacao=Count("pk", filter=Q(classificacao=ResultadoInspecao.Classificacao.SEM_PONTUACAO)),
    ).order_by("versao_checklist__titulo", "versao_checklist__numero", "versao_checklist_id", "regra_pontuacao")


def _irregularidades(resultados):
    originais = resultados.filter(revisao=1).values("inspecao_id")
    registradas = RespostaCampo.objects.filter(inspecao_id__in=originais).alias(
        descricao_preenchida=Trim("descricao_irregularidade"),
    ).exclude(descricao_preenchida="").values(
        "inspecao__versao_checklist_id", "item_id",
    ).annotate(total=Count("pk"))
    frequencias = Counter({
        (linha["inspecao__versao_checklist_id"], str(linha["item_id"])): linha["total"]
        for linha in registradas
    })
    corrigidas = resultados.filter(revisao__gt=1).values_list("versao_checklist_id", "respostas_utilizadas")
    for versao_id, respostas in corrigidas.iterator(chunk_size=200):
        frequencias.update(
            (versao_id, item_id) for item_id, dados in respostas.items()
            if dados.get("descricao_irregularidade", "").strip()
        )

    topo = sorted(frequencias.items(), key=lambda registro: (-registro[1], *registro[0]))[:10]
    versoes = VersaoChecklist.objects.filter(pk__in={versao_id for (versao_id, _), _ in topo}).only(
        "titulo", "numero", "itens", "checklist_id",
    ).in_bulk()
    enunciados = {
        (versao.pk, item.get("id")): item["enunciado"]
        for versao in versoes.values() for item in versao.itens
    }
    return [
        {"versao": versoes[chave[0]], "total": quantidade, "enunciado": enunciados[chave]}
        for chave, quantidade in topo if chave in enunciados
    ]


def indicadores(ator_id, **filtros):
    _, escopo = _escopo(ator_id, painel=True)
    consulta = _filtrar(escopo, **filtros)
    contagens = dict(consulta.values("estado").annotate(total=Count("pk")).values_list("estado", "total"))
    resultados = _resultados_atuais(consulta)
    return {
        "total_inspecoes": sum(contagens.values()),
        "situacoes": [(rotulo, contagens.get(estado, 0)) for estado, rotulo in Inspecao.Estado.choices],
        "resultados_por_versao": list(_resultados_por_versao(resultados)),
        "irregularidades": _irregularidades(resultados),
    }
