from django import forms


class OpcoesForm(forms.Form):
    def __init__(self, *args, opcoes, **kwargs):
        super().__init__(*args, **kwargs)
        for campo, escolhas in opcoes.items():
            field = self.fields[campo]
            vazio = []
            if isinstance(field, forms.TypedChoiceField):
                vazio = [("", "Nova ação" if campo == "acao_id" else "Selecione")]
            field.choices = [*vazio, *escolhas]


class AtribuirForm(OpcoesForm):
    estabelecimento_id = forms.TypedChoiceField(label="Estabelecimento", coerce=int)
    responsavel_id = forms.TypedChoiceField(label="Fiscal responsável", coerce=int)
    participantes_ids = forms.TypedMultipleChoiceField(
        label="Outros fiscais", coerce=int, required=False, widget=forms.CheckboxSelectMultiple,
    )
    acao_id = forms.TypedChoiceField(label="Ação", coerce=int, required=False, empty_value=None)
    operacao = forms.UUIDField(widget=forms.HiddenInput)


class InicioForm(OpcoesForm):
    checklist_id = forms.TypedChoiceField(label="Checklist", coerce=int)


class InicioDiretoForm(InicioForm):
    estabelecimento_id = forms.TypedChoiceField(label="Estabelecimento", coerce=int)
    operacao = forms.UUIDField(widget=forms.HiddenInput)
    field_order = ("estabelecimento_id", "checklist_id")


class EquipeForm(OpcoesForm):
    responsavel_id = forms.TypedChoiceField(label="Fiscal responsável", coerce=int)
    participantes_ids = forms.TypedMultipleChoiceField(
        label="Outros fiscais", coerce=int, required=False, widget=forms.CheckboxSelectMultiple,
    )
    revisao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)


class SupervisaoForm(OpcoesForm):
    fiscais_ids = forms.TypedMultipleChoiceField(
        label="Supervisores ativos da ação", coerce=int, required=False, widget=forms.CheckboxSelectMultiple,
    )
    revisao = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
