from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator


class EntradaForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Não foi possível entrar com os dados informados.",
        "inactive": "Não foi possível entrar com os dados informados.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self.fields["username"]
        username.label = "Usuário"
        username.validators.append(MaxLengthValidator(username.max_length))
        username.widget.attrs.pop("autofocus", None)
        username.widget.attrs["autocomplete"] = "username"

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not password.strip():
            raise ValidationError(self.fields["password"].error_messages["required"], code="required")
        return password
