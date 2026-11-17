from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters

from . import services, vinculos
from .autorizacao import exigir_administrador
from .forms_gestao import UsuarioCriarForm, UsuarioEditarForm, UsuarioSenhaForm, VinculoForm
from .gestao import GestaoMixin
from .models import PERFIS_GERENCIAVEIS, Perfil, Usuario


class UsuariosView(GestaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "contas/lista_usuarios.html", {"pagina": pagina})


@method_decorator(sensitive_post_parameters("senha", "confirmar_senha"), name="dispatch")
class UsuarioCriarView(GestaoMixin, View):
    def get(self, request):
        exigir_administrador(request.user.pk)
        return self.formulario(request, UsuarioCriarForm())

    def post(self, request):
        exigir_administrador(request.user.pk)
        form = UsuarioCriarForm(request.POST)
        if form.is_valid():
            try:
                services.criar(request.user.pk, **form.cleaned_data)
            except ValidationError as error:
                form.add_error(None, error)
            else:
                return redirect("gestao_contas:lista")
        return self.formulario(request, form)

    def formulario(self, request, form):
        return render(request, "gestao/formulario.html", {
            "titulo": "Novo usuário", "form": form, "retorno": "gestao_contas:lista",
            "orientacao": "Você pode definir a senha agora ou depois. Para liberar o acesso, ative a conta após o cadastro.",
        })


class UsuarioEditarView(GestaoMixin, View):
    def get(self, request, pk):
        try:
            usuario = services.consultar(request.user.pk, pk)
        except Usuario.DoesNotExist:
            raise Http404 from None
        form = UsuarioEditarForm(initial={
            "nome": usuario.nome, "perfil": usuario.perfil,
            "situacao": "1" if usuario.is_active else "0", "versao": usuario.versao_gestao,
        })
        return self.formulario(request, usuario, form)

    def post(self, request, pk):
        try:
            usuario = services.consultar(request.user.pk, pk)
            form = UsuarioEditarForm(request.POST)
            if form.is_valid():
                services.editar(request.user.pk, pk, **form.cleaned_data)
                return redirect("gestao_contas:lista")
        except Usuario.DoesNotExist:
            raise Http404 from None
        except services.CadastroDesatualizado:
            return self.formulario(request, usuario, form, status=409)
        except ValidationError as error:
            form.add_error(None, error)
        return self.formulario(request, usuario, form)

    def formulario(self, request, usuario, form, *, status=200):
        return render(request, "gestao/formulario.html", {
            "titulo": "Editar usuário", "form": form, "retorno": "gestao_contas:lista",
            "identificador": usuario.username, "request_path": request.path, "conflito": status == 409,
            "conta_estabelecimento": usuario.pk if usuario.perfil == Perfil.ESTABELECIMENTO else None,
            "url_senha": (
                reverse("gestao_contas:senha", args=[usuario.pk]) if usuario.perfil in PERFIS_GERENCIAVEIS else ""
            ),
            "senha_configurada": usuario.has_usable_password(),
        }, status=status)


@method_decorator(sensitive_post_parameters("senha", "confirmar_senha"), name="dispatch")
class UsuarioSenhaView(GestaoMixin, View):
    def get(self, request, pk):
        return self.formulario(request, pk)

    def post(self, request, pk):
        return self.formulario(request, pk, dados=request.POST)

    def formulario(self, request, pk, dados=None):
        status = 200
        try:
            usuario = services.consultar_credencial(request.user.pk, pk)
            form = UsuarioSenhaForm(dados, initial={"versao": usuario.versao_gestao})
            if form.is_valid():
                services.redefinir_senha(request.user.pk, pk, **form.cleaned_data)
                return redirect("gestao_contas:editar", pk=pk)
        except Usuario.DoesNotExist:
            raise Http404 from None
        except services.CadastroDesatualizado:
            status = 409
        except ValidationError as erro:
            form.add_error(None, erro)

        configurada = usuario.has_usable_password()
        return render(request, "gestao/formulario.html", {
            "titulo": "Redefinir senha" if configurada else "Definir senha",
            "form": form, "retorno_url": reverse("gestao_contas:editar", args=[pk]),
            "identificador": usuario.username, "request_path": request.path, "conflito": status == 409,
            "orientacao": "Após salvar, a pessoa deve usar a nova senha para entrar na conta.",
            "rotulo_salvar": "Salvar senha",
        }, status=status)


class VinculoView(GestaoMixin, View):
    def get(self, request, pk):
        return self.formulario(request, pk)

    def post(self, request, pk):
        return self.formulario(request, pk, dados=request.POST)

    def formulario(self, request, pk, dados=None):
        try:
            usuario, atual, opcoes = vinculos.dados_gestao(request.user.pk, pk)
        except Usuario.DoesNotExist:
            raise Http404 from None
        if atual and not atual.estabelecimento.ativo:
            opcoes.append((atual.estabelecimento_id, f"{atual.estabelecimento.nome} (inativo)"))

        form = VinculoForm(dados, opcoes=opcoes, initial={
            "versao": usuario.versao_gestao,
            "estabelecimento_id": atual.estabelecimento_id if atual else "0",
        })
        status = 200
        if form.is_valid():
            try:
                vinculos.alterar(request.user.pk, pk, **form.cleaned_data)
            except Usuario.DoesNotExist:
                raise Http404 from None
            except vinculos.VinculoDesatualizado:
                status = 409
            except ValidationError as erro:
                form.add_error(None, erro)
            else:
                return redirect("gestao_contas:editar", pk=pk)
        return render(request, "gestao/formulario.html", {
            "titulo": "Vínculo com estabelecimento", "form": form,
            "retorno": "gestao_contas:lista", "identificador": usuario.username,
            "orientacao": "Para encerrar o vínculo atual, selecione Sem vínculo e salve.",
            "request_path": request.path, "conflito": status == 409,
        }, status=status)
