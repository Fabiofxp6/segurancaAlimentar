from django import forms
from django.contrib.auth.forms import UsernameField

from .models import PERFIS_GERENCIAVEIS, Usuario

campo_usuario = Usuario._meta.get_field("username")


class UsuarioCadastroForm(forms.Form):
    nome = forms.CharField(label="Nome")
    perfil = forms.ChoiceField(
        label="Perfil", choices=[(perfil, perfil.label) for perfil in PERFIS_GERENCIAVEIS],
    )


class UsuarioCriarForm(UsuarioCadastroForm):
    username = UsernameField(
        label="Nome de usuário",
        max_length=campo_usuario.max_length,
        validators=campo_usuario.validators,
    )
    field_order = ("nome", "username", "perfil")


class UsuarioEditarForm(UsuarioCadastroForm):
    situacao = forms.TypedChoiceField(
        label="Situação", choices=[("1", "Ativa"), ("0", "Inativa")],
        coerce=lambda value: value == "1",
    )
    versao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)


class VinculoForm(forms.Form):
    estabelecimento_id = forms.TypedChoiceField(
        label="Estabelecimento", coerce=lambda value: None if value == "0" else int(value),
    )
    versao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)

    def __init__(self, *args, opcoes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["estabelecimento_id"].choices = [("0", "Sem vínculo"), *opcoes]
