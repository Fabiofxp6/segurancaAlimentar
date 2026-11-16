from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from . import conclusao_services as services
from .envio_views import ContextoEnvioMixin, contexto_envio
from .views import InspecaoMixin


class ConclusaoForm(forms.Form):
    operacao_id = forms.UUIDField()
    revisao_base = forms.RegexField(r"\A[0-9a-f]{64}\Z", max_length=64)


class ConclusaoView(InspecaoMixin, View):
    def get(self, request, pk):
        dados = services.consultar(request.user.pk, pk)
        return render(request, "conclusao/inspecao.html", {**dados, "contexto": contexto_envio(request)})


class ConcluirView(ContextoEnvioMixin, InspecaoMixin, View):
    def post(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        form = ConclusaoForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"erro": "O pedido de conclusão é inválido. Reabra a revisão."}, status=400)
        try:
            resultado = services.concluir(request.user.pk, pk, **form.cleaned_data)
        except services.ConclusaoDesatualizada as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        return JsonResponse({
            "operacao_id": str(resultado.operacao_id), "confirmado_em": resultado.concluido_em.isoformat(),
            "url": reverse("inspecoes:conclusao", args=[pk]),
        })


class ConclusaoConexaoView(ContextoEnvioMixin, InspecaoMixin, View):
    def get(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        return JsonResponse({"conectado": True})
