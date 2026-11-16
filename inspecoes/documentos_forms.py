from django import forms


class DocumentoEstabelecimentoForm(forms.Form):
    descricao = forms.CharField(
        label="Descrição", required=False, max_length=1000, widget=forms.Textarea(attrs={"rows": 3}),
    )
    arquivo = forms.FileField(
        label="Documento PDF, JPEG ou PNG",
        widget=forms.ClearableFileInput(attrs={"accept": "application/pdf,image/jpeg,image/png"}),
    )
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)

    def clean_arquivo(self):
        if len(self.files.getlist("arquivo")) != 1:
            raise forms.ValidationError("Envie um documento por vez.")
        return self.cleaned_data["arquivo"]
