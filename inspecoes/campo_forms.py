from django import forms
from django.core.exceptions import ValidationError

from .models import EvidenciaCampo


class RespostaCampoForm(forms.Form):
    opcao = forms.ChoiceField(label="Resposta", widget=forms.RadioSelect)
    observacao = forms.CharField(
        label="Observação", max_length=1000, required=False, widget=forms.Textarea(attrs={"rows": 3}),
    )
    ha_irregularidade = forms.BooleanField(label="Registrar irregularidade", required=False)
    descricao_irregularidade = forms.CharField(
        label="Descrição da irregularidade", max_length=1000, required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    revisao = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)

    def __init__(self, *args, opcoes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opcao"].choices = [(opcao, opcao) for opcao in opcoes]

    def clean(self):
        dados = super().clean()
        if dados.get("ha_irregularidade") and not dados.get("descricao_irregularidade"):
            self.add_error("descricao_irregularidade", "Descreva a irregularidade para salvar.")
        elif not dados.get("ha_irregularidade"):
            dados["descricao_irregularidade"] = ""
        return dados


class EvidenciaCampoForm(forms.Form):
    vinculo = forms.ChoiceField(label="Vincular a", choices=EvidenciaCampo.Vinculo.choices)
    arquivo = forms.FileField(
        label="Foto JPEG ou PNG", widget=forms.ClearableFileInput(attrs={"accept": "image/jpeg,image/png"}),
    )
    revisao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)

    def clean_arquivo(self):
        if len(self.files.getlist("arquivo")) != 1:
            raise ValidationError("Envie uma foto por vez.")
        return self.cleaned_data["arquivo"]
