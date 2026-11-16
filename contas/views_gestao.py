from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from . import services, vinculos
from .autorizacao import exigir_administrador
from .forms_gestao import UsuarioCriarForm, UsuarioEditarForm, VinculoForm
from .gestao import GestaoMixin
from .models import Perfil, Usuario


class UsuariosView(GestaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "contas/lista_usuarios.html", {"pagina": pagina})


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
            "orientacao": "O cadastro será criado inativo, sem senha.",
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
