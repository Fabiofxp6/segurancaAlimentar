from posixpath import normpath
from urllib.parse import unquote, urljoin, urlsplit

from django.contrib.auth import login, logout
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters

from estabelecimentos.models import Estabelecimento

from .forms import EntradaForm
from .gestao import GestaoMixin
from .models import Perfil
from .vinculos import estabelecimentos_acessiveis


def _destino_seguro(request, value):
    destination = value.strip()
    allowed_hosts = {request.get_host()}
    require_https = request.is_secure()
    if "\\" in destination or not url_has_allowed_host_and_scheme(
        destination, allowed_hosts=allowed_hosts, require_https=require_https
    ):
        return ""

    destination = urljoin(request.path, destination)
    if not url_has_allowed_host_and_scheme(destination, allowed_hosts=allowed_hosts, require_https=require_https):
        return ""
    path = normpath(unquote(urlsplit(destination).path)).lstrip("/")
    blocked_paths = {reverse(name).strip("/") for name in ("contas:entrar", "contas:sair")}
    return "" if path in blocked_paths else destination


@method_decorator(sensitive_post_parameters(), name="dispatch")
class EntrarView(View):
    http_method_names = ["get", "post", "head", "options"]

    def get(self, request):
        destination = _destino_seguro(request, request.GET.get("next", ""))
        if request.user.is_authenticated and request.user.is_active:
            return redirect(destination or "contas:acesso")
        return render(request, "contas/entrar.html", {"form": EntradaForm(request), "next": destination})

    def post(self, request):
        destination = _destino_seguro(request, request.POST.get("next", ""))
        if request.user.is_authenticated and request.user.is_active:
            return redirect(destination or "contas:acesso")

        form = EntradaForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(destination or "contas:acesso")
        return render(request, "contas/entrar.html", {"form": form, "next": destination})


class SairView(View):
    http_method_names = ["post", "options"]

    def post(self, request):
        logout(request)
        return redirect("contas:entrar")


class AcessoView(View):
    http_method_names = ["get", "head", "options"]

    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_active:
            return redirect_to_login(reverse("contas:acesso"), reverse("contas:entrar"))
        unidade_id = None
        if request.user.perfil == Perfil.ESTABELECIMENTO:
            unidade_id = estabelecimentos_acessiveis(request.user.pk).values_list("pk", flat=True).first()
        return render(request, "contas/acesso.html", {
            "unidade_id": unidade_id,
            "usuario": request.user.get_username(),
            "administracao": request.user.perfil == Perfil.ADMINISTRADOR,
        })



class MeuEstabelecimentoView(GestaoMixin, View):
    def get(self, request, pk):
        try:
            estabelecimento = estabelecimentos_acessiveis(request.user.pk).values("nome").get(pk=pk)
        except Estabelecimento.DoesNotExist:
            raise Http404 from None
        return render(request, "contas/estabelecimento.html", {"estabelecimento": estabelecimento})
