from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from . import adiamento_services as services
from .envio_views import ContextoEnvioMixin, contexto_envio
from .models import PedidoAdiamento
from .services import InspecaoDesatualizada
from .views import InspecaoMixin


class SolicitarAdiamentoForm(forms.Form):
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)
    data_proposta = forms.DateTimeField(
        label="Nova data e hora (Maceió)", widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    justificativa = forms.CharField(
        label="Justificativa", max_length=2000, widget=forms.Textarea(attrs={"rows": 3}),
    )


class DecidirAdiamentoForm(forms.Form):
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)
    decisao = forms.ChoiceField(
        label="Decisão",
        choices=[("", "Selecione uma decisão"), (PedidoAdiamento.Situacao.APROVADO, "Aprovar"),
                 (PedidoAdiamento.Situacao.REJEITADO, "Rejeitar")],
    )
    motivo = forms.CharField(label="Motivo da decisão", max_length=2000, widget=forms.Textarea(attrs={"rows": 3}))


@method_decorator(never_cache, name="dispatch")
class AdiamentosView(InspecaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "adiamentos/lista.html", {"pagina": pagina})


@method_decorator(never_cache, name="dispatch")
class AdiamentoView(InspecaoMixin, View):
    def get(self, request, pk):
        dados = services.consultar(request.user.pk, pk)
        return render(request, "adiamentos/inspecao.html", {
            **dados, "contexto": contexto_envio(request),
            "solicitar": SolicitarAdiamentoForm() if dados["pode_solicitar"] else None,
            "decidir": DecidirAdiamentoForm() if dados["decidivel"] else None,
        })


class AdiamentoConexaoView(ContextoEnvioMixin, InspecaoMixin, View):
    def get(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        return JsonResponse({"conectado": True})


class OperacaoAdiamentoMixin(ContextoEnvioMixin, InspecaoMixin):
    def post(self, request, pk, **identificadores):
        services.verificar_acesso(request.user.pk, pk)
        form = self.form_class(request.POST)
        with timezone.override("America/Maceio"):
            valido = form.is_valid()
        if not valido:
            return JsonResponse({"erro": " ".join(e for erros in form.errors.values() for e in erros)}, status=400)
        try:
            pedido = self.registrar(request.user.pk, pk, **identificadores, **form.cleaned_data)
        except InspecaoDesatualizada as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        instante = pedido.decidida_em if identificadores else pedido.solicitada_em
        return JsonResponse({
            "operacao_id": str(form.cleaned_data["operacao_id"]), "confirmado_em": instante.isoformat(),
            "url": reverse("inspecoes:adiamento", args=[pk]),
        })


class SolicitarAdiamentoView(OperacaoAdiamentoMixin, View):
    form_class = SolicitarAdiamentoForm
    registrar = staticmethod(services.solicitar)


class DecidirAdiamentoView(OperacaoAdiamentoMixin, View):
    form_class = DecidirAdiamentoForm
    registrar = staticmethod(services.decidir)
