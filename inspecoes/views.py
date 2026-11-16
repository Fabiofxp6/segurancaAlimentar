from uuid import uuid4

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from contas.gestao import GestaoMixin
from contas.models import Perfil

from .cancelamento_services import tem_pedido_pendente

from . import consulta_services, services
from .consulta_forms import ConsultaInspecaoForm, FiltrosInspecaoForm
from .forms import AtribuirForm, EquipeForm, InicioDiretoForm, InicioForm, SupervisaoForm
from .models import AcaoFiscalizacao, Inspecao


class InspecaoMixin(GestaoMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except (AcaoFiscalizacao.DoesNotExist, Inspecao.DoesNotExist):
            raise Http404 from None

    def formulario(self, request, form, titulo, *, status=200):
        return render(request, "inspecoes/formulario.html", {
            "titulo": titulo, "form": form, "request_path": request.path,
            "conflito": status == 409,
        }, status=status)


@method_decorator(never_cache, name="dispatch")
class InspecoesView(InspecaoMixin, View):
    def get(self, request):
        perfil, opcoes = consulta_services.opcoes(request.user.pk)
        form = ConsultaInspecaoForm(request.GET, opcoes=opcoes)
        pagina = consulta_services.listar(request.user.pk, **form.cleaned_data) if form.is_valid() else None
        return render(request, "inspecoes/lista.html", {
            "pagina": pagina, "admin": perfil == Perfil.ADMINISTRADOR, "form": form,
            "parametros": request.GET,
        }, status=400 if form.errors else 200)


@method_decorator(never_cache, name="dispatch")
class IndicadoresView(InspecaoMixin, View):
    def get(self, request):
        _, opcoes = consulta_services.opcoes(request.user.pk, painel=True)
        form = FiltrosInspecaoForm(request.GET, opcoes=opcoes)
        dados = consulta_services.indicadores(request.user.pk, **form.cleaned_data) if form.is_valid() else {}
        return render(request, "inspecoes/indicadores.html", {
            "form": form, **dados,
        }, status=400 if form.errors else 200)


class InspecaoView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, perfil, pode_iniciar, designacoes, supervisor = services.consultar(request.user.pk, pk)
        return render(request, "inspecoes/detalhe.html", {
            "inspecao": inspecao, "admin": perfil == Perfil.ADMINISTRADOR, "pode_iniciar": pode_iniciar,
            "designacoes": designacoes, "supervisor": supervisor,
            "pode_ver_documentos": perfil == Perfil.FISCALIZACAO,
            "pode_consultar_campo": perfil == Perfil.FISCALIZACAO
            and inspecao.estado in (Inspecao.Estado.EM_ANDAMENTO, Inspecao.Estado.CANCELADA, Inspecao.Estado.CONCLUIDA),
            "pode_preencher": inspecao.estado == Inspecao.Estado.EM_ANDAMENTO and not tem_pedido_pendente(inspecao),
            "cancelada": inspecao.estado == Inspecao.Estado.CANCELADA,
            "tem_resultado": inspecao.estado == Inspecao.Estado.CONCLUIDA,
            "pode_revisar": perfil == Perfil.FISCALIZACAO and inspecao.estado == Inspecao.Estado.EM_ANDAMENTO,
        })


class CriacaoMixin(InspecaoMixin):
    def get(self, request):
        return self.edicao(request)

    def post(self, request):
        return self.edicao(request, request.POST)

    def edicao(self, request, dados=None):
        dados_opcoes = services.opcoes_criacao(request.user.pk, self.perfil)
        if self.perfil == Perfil.ADMINISTRADOR:
            fiscais = dados_opcoes["fiscais"]
            opcoes = {
                "estabelecimento_id": dados_opcoes["estabelecimentos"], "acao_id": dados_opcoes["acoes"],
                "responsavel_id": fiscais, "participantes_ids": fiscais,
            }
        else:
            opcoes = {
                "estabelecimento_id": dados_opcoes["estabelecimentos"], "checklist_id": dados_opcoes["checklists"],
            }
        form = self.form_class(dados, opcoes=opcoes, initial={"operacao": uuid4()})
        if form.is_valid():
            try:
                inspecao = self.operacao(request.user.pk, **form.cleaned_data)
            except ValidationError as erro:
                form.add_error(None, erro)
            except services.InspecaoDesatualizada:
                return self.formulario(request, form, self.titulo, status=409)
            else:
                return redirect("inspecoes:detalhe", pk=inspecao.pk)
        return self.formulario(request, form, self.titulo)


class AtribuirView(CriacaoMixin, View):
    perfil = Perfil.ADMINISTRADOR
    form_class = AtribuirForm
    operacao = staticmethod(services.atribuir)
    titulo = "Atribuir inspeção"


class InicioDiretoView(CriacaoMixin, View):
    perfil = Perfil.FISCALIZACAO
    form_class = InicioDiretoForm
    operacao = staticmethod(services.iniciar_diretamente)
    titulo = "Iniciar nova inspeção"


class InicioView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, checklists = services.opcoes_inicio(request.user.pk, pk)
        if inspecao.estado != Inspecao.Estado.ATRIBUIDA:
            return redirect("inspecoes:detalhe", pk=pk)
        return self.formulario(request, InicioForm(opcoes={"checklist_id": checklists}), "Iniciar inspeção")

    def post(self, request, pk):
        _, checklists = services.opcoes_inicio(request.user.pk, pk)
        form = InicioForm(request.POST, opcoes={"checklist_id": checklists})
        if form.is_valid():
            try:
                services.iniciar_atribuida(request.user.pk, pk, **form.cleaned_data)
            except ValidationError as erro:
                form.add_error(None, erro)
            except services.InspecaoDesatualizada:
                return self.formulario(request, form, "Iniciar inspeção", status=409)
            else:
                return redirect("inspecoes:detalhe", pk=pk)
        return self.formulario(request, form, "Iniciar inspeção")


class EquipeView(InspecaoMixin, View):
    def get(self, request, pk):
        return self.edicao(request, pk)

    def post(self, request, pk):
        return self.edicao(request, pk, request.POST)

    def edicao(self, request, pk, dados=None):
        inspecao, fiscais = services.opcoes_equipe(request.user.pk, pk)
        form = EquipeForm(dados, opcoes={"responsavel_id": fiscais, "participantes_ids": fiscais}, initial={
            "responsavel_id": inspecao.responsavel_id, "revisao": inspecao.revisao,
            "participantes_ids": [p.pk for p in inspecao.participantes.all()],
        })
        if form.is_valid():
            try:
                services.alterar_equipe(request.user.pk, pk, **form.cleaned_data)
            except ValidationError as erro:
                form.add_error(None, erro)
            except services.InspecaoDesatualizada:
                return self.formulario(request, form, "Alterar equipe", status=409)
            else:
                return redirect("inspecoes:detalhe", pk=pk)
        return self.formulario(request, form, "Alterar equipe")


class SupervisaoView(InspecaoMixin, View):
    def get(self, request, pk):
        return self.edicao(request, pk)

    def post(self, request, pk):
        return self.edicao(request, pk, request.POST)

    def edicao(self, request, pk, dados=None):
        acao, equipe, historico = services.consultar_supervisao(request.user.pk, pk)
        ids = {fiscal_id for fiscal_id, _ in equipe}
        form = SupervisaoForm(dados, opcoes={"fiscais_ids": equipe}, initial={
            "revisao": acao.revisao_supervisao,
            "fiscais_ids": [d.fiscal_id for d in historico if d.fim is None and d.fiscal_id in ids],
        })
        status = 200
        if form.is_valid():
            try:
                services.alterar_supervisao(request.user.pk, pk, **form.cleaned_data)
            except ValidationError as erro:
                form.add_error(None, erro)
            except services.InspecaoDesatualizada:
                status = 409
            else:
                return redirect("inspecoes:supervisao", pk=pk)
        return render(request, "inspecoes/supervisao.html", {
            "titulo": f"Supervisão da ação #{pk}", "form": form, "historico": historico, "elegiveis": ids,
            "request_path": request.path, "conflito": status == 409,
        }, status=status)
