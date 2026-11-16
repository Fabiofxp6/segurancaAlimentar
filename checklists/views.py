from decimal import Decimal

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from contas.autorizacao import exigir_administrador
from contas.gestao import GestaoMixin

from . import services
from .forms import ChecklistForm, ItemForm, RascunhoForm, RevisaoForm
from .models import Checklist, VersaoChecklist


class ChecklistMixin(GestaoMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except (Checklist.DoesNotExist, VersaoChecklist.DoesNotExist, services.ItemInexistente):
            raise Http404 from None


def _rascunho(request, checklist, versoes, *, form=None, erro="", status=200):
    if form is None:
        form = RascunhoForm(initial={
            "titulo": checklist.titulo, "referencia": checklist.referencia,
            "regras": checklist.regras, "revisao": checklist.revisao,
        })
    return render(request, "checklists/rascunho.html", {
        "checklist": checklist, "versoes": versoes, "form": form, "erro": erro,
    }, status=status)


class ChecklistsView(ChecklistMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "checklists/lista.html", {"pagina": pagina})


class ChecklistCriarView(ChecklistMixin, View):
    def get(self, request):
        exigir_administrador(request.user.pk)
        return self.formulario(request, ChecklistForm())

    def post(self, request):
        exigir_administrador(request.user.pk)
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = services.criar(request.user.pk, **form.cleaned_data)
            return redirect("checklists:rascunho", pk=checklist.pk)
        return self.formulario(request, form)

    def formulario(self, request, form):
        return render(request, "gestao/formulario.html", {
            "titulo": "Novo checklist", "form": form, "retorno": "checklists:lista",
        })


class RascunhoView(ChecklistMixin, View):
    def get(self, request, pk):
        return _rascunho(request, *services.consultar(request.user.pk, pk))

    def post(self, request, pk):
        checklist, versoes = services.consultar(request.user.pk, pk)
        form = RascunhoForm(request.POST)
        if form.is_valid():
            try:
                services.editar(request.user.pk, pk, **form.cleaned_data)
            except services.RascunhoDesatualizado:
                return _rascunho(request, checklist, versoes, form=form, status=409,
                                 erro="O rascunho mudou. Reabra a página antes de salvar.")
            return redirect("checklists:rascunho", pk=pk)
        return _rascunho(request, checklist, versoes, form=form)


class ItemView(ChecklistMixin, View):
    def get(self, request, pk, item_id=None):
        checklist, item = services.consultar_item(request.user.pk, pk, item_id)
        initial = {"revisao": checklist.revisao}
        if item:
            initial.update(item)
            initial["opcoes"] = "\n".join(item["opcoes"])
            if item["peso"] is not None:
                initial["peso"] = Decimal(item["peso"])
        return self.formulario(request, checklist, item, ItemForm(initial=initial))

    def post(self, request, pk, item_id=None):
        checklist, item = services.consultar_item(request.user.pk, pk, item_id)
        form = ItemForm(request.POST)
        if form.is_valid():
            try:
                services.salvar_item(request.user.pk, pk, item_id, **form.cleaned_data)
            except ValidationError as erro:
                form.add_error(None, erro)
            except services.RascunhoDesatualizado:
                return self.formulario(request, checklist, item, form, status=409)
            else:
                return redirect("checklists:rascunho", pk=pk)
        return self.formulario(request, checklist, item, form)

    def formulario(self, request, checklist, item, form, *, status=200):
        return render(request, "checklists/item.html", {
            "titulo": "Editar item" if item else "Novo item", "checklist": checklist, "item": item,
            "form": form, "conflito": status == 409, "request_path": request.path,
        }, status=status)


class ItemRemoverView(ChecklistMixin, View):
    http_method_names = ["post", "options"]

    def post(self, request, pk, item_id):
        checklist, versoes = services.consultar(request.user.pk, pk)
        form = RevisaoForm(request.POST)
        if form.is_valid():
            try:
                services.remover_item(request.user.pk, pk, item_id, **form.cleaned_data)
            except services.RascunhoDesatualizado:
                return _rascunho(request, checklist, versoes, status=409,
                                 erro="O rascunho mudou. Confira o item antes de removê-lo.")
            return redirect("checklists:rascunho", pk=pk)
        return _rascunho(request, checklist, versoes, status=400,
                         erro="Revisão inválida. Reabra o checklist e tente novamente.")


class ChecklistPublicarView(ChecklistMixin, View):
    http_method_names = ["post", "options"]

    def post(self, request, pk):
        checklist, versoes = services.consultar(request.user.pk, pk)
        form = RevisaoForm(request.POST)
        if not form.is_valid():
            return _rascunho(request, checklist, versoes, status=400,
                             erro="Revisão inválida. Reabra o checklist e tente novamente.")
        try:
            versao = services.publicar(request.user.pk, pk, **form.cleaned_data)
        except services.RascunhoDesatualizado:
            return _rascunho(request, checklist, versoes, status=409,
                             erro="O rascunho mudou. Confira os dados antes de publicar.")
        except ValidationError as erro:
            return _rascunho(request, checklist, versoes, erro=erro.messages[0])
        return redirect("checklists:versao", pk=pk, versao_pk=versao.pk)


class ChecklistVersaoView(ChecklistMixin, View):
    def get(self, request, pk, versao_pk):
        versao = services.consultar_versao(request.user.pk, pk, versao_pk)
        return render(request, "checklists/versao.html", {"versao": versao, "titulo": versao.titulo})
