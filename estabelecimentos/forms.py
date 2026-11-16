from django import forms


class EstabelecimentoCriarForm(forms.Form):
    nome = forms.CharField(label="Nome")
    documento = forms.CharField(label="Documento", required=False)
    endereco = forms.CharField(label="Endereço", required=False)
    contato = forms.CharField(label="Contato", required=False)


class EstabelecimentoEditarForm(EstabelecimentoCriarForm):
    ativo = forms.TypedChoiceField(
        label="Situação",
        choices=[("1", "Ativo"), ("0", "Inativo")],
        coerce=lambda value: value == "1",
    )
    versao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
