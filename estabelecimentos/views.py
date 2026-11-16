from django.forms.models import model_to_dict
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from contas.autorizacao import exigir_administrador
from contas.gestao import GestaoMixin

from . import services
from .forms import EstabelecimentoCriarForm, EstabelecimentoEditarForm
from .models import Estabelecimento


class EstabelecimentosView(GestaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "estabelecimentos/lista.html", {"pagina": pagina})


class EstabelecimentoCriarView(GestaoMixin, View):
    def get(self, request):
        exigir_administrador(request.user.pk)
        return self.formulario(request, EstabelecimentoCriarForm())

    def post(self, request):
        exigir_administrador(request.user.pk)
        form = EstabelecimentoCriarForm(request.POST)
        if form.is_valid():
            services.criar(request.user.pk, **form.cleaned_data)
            return redirect("estabelecimentos:lista")
        return self.formulario(request, form)

    def formulario(self, request, form):
        return render(request, "gestao/formulario.html", {
            "titulo": "Novo estabelecimento", "form": form, "retorno": "estabelecimentos:lista",
        })


class EstabelecimentoEditarView(GestaoMixin, View):
    def get(self, request, pk):
        try:
            cadastro = services.consultar(request.user.pk, pk)
        except Estabelecimento.DoesNotExist:
            raise Http404 from None
        initial = model_to_dict(cadastro, fields=(*services.CAMPOS_CADASTRAIS, "versao"))
        initial["ativo"] = "1" if cadastro.ativo else "0"
        return self.formulario(request, EstabelecimentoEditarForm(initial=initial))

    def post(self, request, pk):
        try:
            services.consultar(request.user.pk, pk)
            form = EstabelecimentoEditarForm(request.POST)
            if form.is_valid():
                services.editar(request.user.pk, pk, **form.cleaned_data)
                return redirect("estabelecimentos:lista")
        except Estabelecimento.DoesNotExist:
            raise Http404 from None
        except services.CadastroDesatualizado:
            return self.formulario(request, form, status=409)
        return self.formulario(request, form)

    def formulario(self, request, form, *, status=200):
        return render(request, "gestao/formulario.html", {
            "titulo": "Editar estabelecimento", "form": form,
            "retorno": "estabelecimentos:lista", "conflito": status == 409,
            "request_path": request.path,
        }, status=status)
