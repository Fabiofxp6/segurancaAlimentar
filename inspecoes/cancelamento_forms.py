from django import forms


class OperacaoCancelamentoForm(forms.Form):
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)


class SolicitarCancelamentoForm(OperacaoCancelamentoForm):
    justificativa = forms.CharField(
        label="Justificativa do cancelamento", max_length=2000,
        widget=forms.Textarea(attrs={"rows": 4}),
    )


class DecidirCancelamentoForm(OperacaoCancelamentoForm):
    decisao = forms.ChoiceField(label="Decisão", choices=[
        ("", "Selecione"), ("aprovado", "Aprovar"), ("rejeitado", "Rejeitar"),
    ])
    motivo_decisao = forms.CharField(
        label="Motivo da decisão", max_length=2000, widget=forms.Textarea(attrs={"rows": 4}),
    )
