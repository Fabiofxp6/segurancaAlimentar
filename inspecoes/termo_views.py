from io import BytesIO

from django import forms
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from . import termo_services as services
from .envio_views import ContextoEnvioMixin, contexto_envio
from .models import TermoInspecao
from .views import InspecaoMixin


class OperacaoTermoForm(forms.Form):
    operacao_id = forms.UUIDField()


@method_decorator(never_cache, name="dispatch")
class TermoMixin(InspecaoMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except TermoInspecao.DoesNotExist:
            raise Http404 from None


def _pdf(termo):
    resposta = FileResponse(
        BytesIO(termo.conteudo), as_attachment=True, filename=f"{termo.codigo}.pdf",
        content_type="application/pdf",
    )
    resposta["X-Content-Type-Options"] = "nosniff"
    return resposta


class TermosEmitidosView(TermoMixin, View):
    def get(self, request):
        pagina = services.listar_emitidos(request.user.pk, request.GET.get("pagina"))
        return render(request, "termos/emitidos.html", {"pagina": pagina})


class TermoView(TermoMixin, View):
    def get(self, request, pk, termo_id=None):
        dados = services.consultar(request.user.pk, pk, termo_id=termo_id)
        return render(request, "termos/inspecao.html", {**dados, "contexto": contexto_envio(request)})


class TermoPdfView(TermoMixin, View):
    def get(self, request, pk, termo_id):
        return _pdf(services.baixar_interno(request.user.pk, pk, termo_id))


class TermoConexaoView(ContextoEnvioMixin, TermoMixin, View):
    def get(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        return JsonResponse({"conectado": True})


class OperacaoTermoMixin(ContextoEnvioMixin, TermoMixin):
    def post(self, request, pk, *args, **kwargs):
        form = OperacaoTermoForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"erro": "A solicitação é inválida. Reabra a página."}, status=400)
        try:
            instante = self.registrar(request.user.pk, pk, **kwargs, **form.cleaned_data)
        except services.FalhaGeracaoTermo:
            return JsonResponse({"erro": "Não foi possível gerar o PDF. Tente novamente."}, status=422)
        except services.TermoDesatualizado as erro:
            return JsonResponse({"erro": str(erro)}, status=409)

        return JsonResponse({
            "operacao_id": str(form.cleaned_data["operacao_id"]),
            "confirmado_em": instante.isoformat(),
            "url": reverse("inspecoes:termo", args=[pk]),
        })


class TermoEmitirView(OperacaoTermoMixin, View):
    def registrar(self, ator_id, pk, *, operacao_id):
        return services.emitir(ator_id, pk, operacao_id=operacao_id).emitido_em


class TermoLiberarView(OperacaoTermoMixin, View):
    def registrar(self, ator_id, pk, *, termo_id, operacao_id):
        return services.liberar(ator_id, pk, termo_id, operacao_id=operacao_id).liberado_em


class ResultadosLiberadosView(TermoMixin, View):
    def get(self, request):
        pagina = services.listar_liberados(request.user.pk, request.GET.get("pagina"))
        return render(request, "termos/resultados.html", {"pagina": pagina})


class ResultadoLiberadoView(TermoMixin, View):
    def get(self, request, termo_id):
        termo = services.consultar_liberado(request.user.pk, termo_id)
        return render(request, "termos/resultado.html", {"termo": termo, "resultado": termo.resultado})


class ResultadoPdfView(TermoMixin, View):
    def get(self, request, termo_id):
        return _pdf(services.consultar_liberado(request.user.pk, termo_id, baixar=True))
