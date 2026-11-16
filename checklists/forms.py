from django import forms


class ChecklistForm(forms.Form):
    titulo = forms.CharField(label="Título")
    referencia = forms.CharField(label="Referência", required=False)
    regras = forms.CharField(label="Regras e orientações", required=False, widget=forms.Textarea(attrs={"rows": 4}))


class RevisaoForm(forms.Form):
    revisao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)


class RascunhoForm(ChecklistForm, RevisaoForm):
    pass


class ItemForm(RevisaoForm):
    enunciado = forms.CharField(label="Enunciado")
    ordem = forms.IntegerField(label="Ordem", min_value=1, max_value=2_147_483_647)
    peso = forms.DecimalField(
        label="Peso", required=False, max_digits=18, decimal_places=8, localize=True,
    )
    obrigatorio = forms.BooleanField(label="Resposta obrigatória", required=False)
    opcoes = forms.CharField(
        label="Opções de resposta", help_text="Uma opção por linha.",
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    def clean_opcoes(self):
        opcoes = [linha.strip() for linha in self.cleaned_data["opcoes"].splitlines() if linha.strip()]
        if len({opcao.casefold() for opcao in opcoes}) != len(opcoes):
            raise forms.ValidationError("Informe cada opção de resposta uma única vez.")
        return opcoes
