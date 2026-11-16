from django import forms
from django.core.exceptions import ValidationError

from .models import Inspecao


class DataFiltroField(forms.DateField):
    def prepare_value(self, value):
        try:
            return self.to_python(value)
        except ValidationError:
            return value


class FiltrosInspecaoForm(forms.Form):
    estado = forms.ChoiceField(
        label="Situação", choices=[("", "Todas"), *Inspecao.Estado.choices], required=False,
    )
    estabelecimento = forms.TypedChoiceField(label="Estabelecimento", coerce=int, empty_value=None, required=False)
    fiscal = forms.TypedChoiceField(label="Fiscal da equipe", coerce=int, empty_value=None, required=False)
    inicio = DataFiltroField(
        label="Criada a partir de", required=False, input_formats=("%Y-%m-%d", "%d/%m/%Y"),
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )
    fim = DataFiltroField(
        label="Criada até", required=False, input_formats=("%Y-%m-%d", "%d/%m/%Y"),
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )

    def __init__(self, *args, opcoes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["estabelecimento"].choices = [("", "Todos"), *opcoes["estabelecimentos"]]
        self.fields["fiscal"].choices = [("", "Todos"), *opcoes["fiscais"]]

    def clean(self):
        dados = super().clean()
        inicio, fim = dados.get("inicio"), dados.get("fim")
        if inicio and fim and inicio > fim:
            self.add_error("fim", "A data final deve ser igual ou posterior à inicial.")
        return dados


class ConsultaInspecaoForm(FiltrosInspecaoForm):
    pagina = forms.IntegerField(
        min_value=1, required=False, widget=forms.HiddenInput,
        error_messages={"min_value": "Informe uma página maior ou igual a 1."},
    )
