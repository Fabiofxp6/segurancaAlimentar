from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from . import auditoria_services, cancelamento_services as services
from .cancelamento_forms import DecidirCancelamentoForm, SolicitarCancelamentoForm
from .envio_views import ContextoEnvioMixin, contexto_envio
from .models import PedidoCancelamento
from .views import InspecaoMixin


class PedidosCancelamentoView(InspecaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "cancelamento/lista.html", {"pagina": pagina})


class CancelamentoView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, pedidos, pode_solicitar, decisao = services.consultar(request.user.pk, pk)
        return render(request, "cancelamento/inspecao.html", {
            "inspecao": inspecao, "pedidos": pedidos, "pode_solicitar": pode_solicitar, "decisao": decisao,
            "form_solicitar": SolicitarCancelamentoForm(), "form_decidir": DecidirCancelamentoForm(),
            "contexto": contexto_envio(request),
        })


class CancelamentoConexaoView(ContextoEnvioMixin, InspecaoMixin, View):
    def get(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        return JsonResponse({"conectado": True})


class EnvioCancelamentoMixin(ContextoEnvioMixin, InspecaoMixin):
    http_method_names = ["post", "options"]

    def post(self, request, pk, *alvo):
        services.verificar_acesso(request.user.pk, pk)
        form = self.form_class(request.POST)
        if not form.is_valid():
            erros = [str(mensagem) for lista in form.errors.values() for mensagem in lista]
            return JsonResponse({"erro": " ".join(erros)}, status=400)
        try:
            pedido = self.gravar(request.user.pk, pk, *alvo, **form.cleaned_data)
        except PedidoCancelamento.DoesNotExist:
            raise Http404 from None
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        except services.CancelamentoDesatualizado as erro:
            return JsonResponse({"erro": str(erro)}, status=409)

        instante = pedido.decidida_em if alvo else pedido.solicitada_em
        return JsonResponse({
            "operacao_id": str(form.cleaned_data["operacao_id"]),
            "confirmado_em": instante.isoformat(),
            "url": reverse("inspecoes:cancelamento", args=[pk]),
        })


class SolicitarCancelamentoView(EnvioCancelamentoMixin, View):
    form_class = SolicitarCancelamentoForm
    gravar = staticmethod(services.solicitar)


class DecidirCancelamentoView(EnvioCancelamentoMixin, View):
    form_class = DecidirCancelamentoForm
    gravar = staticmethod(services.decidir)

    def post(self, request, pk, pedido_id):
        return super().post(request, pk, pedido_id)


class AuditoriaInspecaoView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, pagina = auditoria_services.listar(request.user.pk, pk, request.GET.get("pagina"))
        return render(request, "cancelamento/auditoria.html", {"inspecao": inspecao, "pagina": pagina})
