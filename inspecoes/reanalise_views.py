from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from . import reanalise_services as services
from .envio_views import ContextoEnvioMixin, contexto_envio
from .services import InspecaoDesatualizada
from .views import InspecaoMixin


class ParecerForm(forms.Form):
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)
    base_id = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    parecer = forms.CharField(label="Parecer", max_length=2000, widget=forms.Textarea(attrs={"rows": 4}))
    indica_correcao = forms.TypedChoiceField(
        label="Encaminhamento", choices=[("", "Selecione"), ("manter", "Manter resultado"), ("corrigir", "Indicar correção")],
        coerce=lambda valor: valor == "corrigir",
    )


@method_decorator(never_cache, name="dispatch")
class ReanalisesView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, pagina = services.listar(request.user.pk, pk, request.GET.get("pagina"))
        return render(request, "reanalises/lista.html", {"inspecao": inspecao, "pagina": pagina})


@method_decorator(never_cache, name="dispatch")
class ReanaliseView(InspecaoMixin, View):
    def get(self, request, pk, documento_id):
        dados = services.consultar(request.user.pk, pk, documento_id)
        form = ParecerForm(initial={"base_id": dados["base"].pk}) if dados["pode_registrar"] else None
        return render(request, "reanalises/documento.html", {
            **dados, "form": form, "contexto": contexto_envio(request) if form else "",
        })


class ReanaliseConexaoView(ContextoEnvioMixin, InspecaoMixin, View):
    def get(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        return JsonResponse({"conectado": True})


class RegistrarReanaliseView(ContextoEnvioMixin, InspecaoMixin, View):
    def post(self, request, pk, documento_id):
        services.verificar_acesso(request.user.pk, pk)
        form = ParecerForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"erro": " ".join(e for erros in form.errors.values() for e in erros)}, status=400)
        try:
            registro = services.registrar(request.user.pk, pk, documento_id, **form.cleaned_data)
        except InspecaoDesatualizada as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        return JsonResponse({
            "operacao_id": str(registro.operacao_id), "confirmado_em": registro.registrada_em.isoformat(),
            "url": reverse("inspecoes:reanalise_documento", args=[pk, documento_id]),
        })
