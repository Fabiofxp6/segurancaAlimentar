from django import forms
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from . import correcao_services as services
from .envio_views import ContextoEnvioMixin, contexto_envio
from .models import PedidoCorrecao, ResultadoInspecao
from .termo_services import FalhaGeracaoTermo, TermoDesatualizado
from .views import InspecaoMixin


class OperacaoCorrecaoForm(forms.Form):
    operacao_id = forms.UUIDField(widget=forms.HiddenInput)


class SolicitarCorrecaoForm(OperacaoCorrecaoForm):
    base_id = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    justificativa = forms.CharField(label="Justificativa", max_length=2000, widget=forms.Textarea(attrs={"rows": 3}))
    opcao = forms.ChoiceField(label="Resposta proposta")
    observacao = forms.CharField(
        label="Observação", required=False, max_length=1000, widget=forms.Textarea(attrs={"rows": 3}),
    )
    descricao_irregularidade = forms.CharField(
        label="Descrição da irregularidade", required=False, max_length=1000,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, opcoes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opcao"].choices = [("", "Selecione uma resposta"), *((opcao, opcao) for opcao in opcoes)]


class DecisaoCorrecaoForm(OperacaoCorrecaoForm):
    aprovada = forms.TypedChoiceField(
        label="Decisão", choices=[("", "Selecione uma decisão"), ("aprovar", "Aprovar"), ("rejeitar", "Rejeitar")],
        coerce=lambda valor: valor == "aprovar",
    )
    motivo = forms.CharField(label="Motivo da decisão", max_length=2000, widget=forms.Textarea(attrs={"rows": 3}))


@method_decorator(never_cache, name="dispatch")
class CorrecaoMixin(InspecaoMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except (PedidoCorrecao.DoesNotExist, ResultadoInspecao.DoesNotExist):
            raise Http404 from None


class PedidosCorrecaoView(CorrecaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "correcoes/lista.html", {"pagina": pagina})


class RevisoesInspecaoView(CorrecaoMixin, View):
    def get(self, request, pk):
        dados = services.consultar_inspecao(request.user.pk, pk, request.GET.get("pagina"))
        return render(request, "correcoes/revisoes.html", dados)


class PedidoCorrecaoView(CorrecaoMixin, View):
    def get(self, request, pk, pedido_id):
        dados = services.consultar_pedido(request.user.pk, pk, pedido_id)
        return render(request, "correcoes/pedido.html", {
            **dados, "contexto": contexto_envio(request), "form_decidir": DecisaoCorrecaoForm(),
        })


class CorrecaoConexaoView(ContextoEnvioMixin, CorrecaoMixin, View):
    def get(self, request, pk):
        services.verificar_acesso(request.user.pk, pk)
        return JsonResponse({"conectado": True})


def _confirmacao(pk, pedido_id, chave, instante):
    return JsonResponse({
        "operacao_id": str(chave), "confirmado_em": instante.isoformat(),
        "url": reverse("inspecoes:correcao", args=[pk, pedido_id]),
    })


def _erros_formulario(form):
    return JsonResponse({"erro": " ".join(str(e) for lista in form.errors.values() for e in lista)}, status=400)


class PrepararCorrecaoView(CorrecaoMixin, View):
    def get(self, request, pk, item_id):
        inspecao, base, item, antes = services.consultar_item(request.user.pk, pk, item_id)
        form = SolicitarCorrecaoForm(opcoes=item["opcoes"], initial={"base_id": base.pk, **(antes or {})})
        return render(request, "correcoes/solicitar.html", {
            "inspecao": inspecao, "base": base, "item": item, "antes": antes,
            "contexto": contexto_envio(request), "form": form,
        })


class SolicitarCorrecaoView(ContextoEnvioMixin, CorrecaoMixin, View):
    def post(self, request, pk, item_id):
        try:
            _, _, item, _ = services.consultar_item(request.user.pk, pk, item_id)
            form = SolicitarCorrecaoForm(request.POST, opcoes=item["opcoes"])
            if not form.is_valid():
                return _erros_formulario(form)
            pedido = services.solicitar(request.user.pk, pk, item_id, **form.cleaned_data)
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        except services.CorrecaoDesatualizada as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        return _confirmacao(pk, pedido.pk, pedido.operacao_id, pedido.solicitada_em)


class OperacaoPedidoMixin(ContextoEnvioMixin, CorrecaoMixin):
    def post(self, request, pk, pedido_id):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return _erros_formulario(form)
        try:
            instante = self.registrar(request.user.pk, pk, pedido_id, **form.cleaned_data)
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        except (services.CorrecaoDesatualizada, TermoDesatualizado) as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        except FalhaGeracaoTermo:
            return JsonResponse({"erro": "Falha na geração do retificador. Tente aplicar novamente."}, status=422)
        return _confirmacao(pk, pedido_id, form.cleaned_data["operacao_id"], instante)


class DecidirCorrecaoView(OperacaoPedidoMixin, View):
    form_class = DecisaoCorrecaoForm

    def registrar(self, ator, pk, pedido_id, **dados):
        return services.decidir(ator, pk, pedido_id, **dados).decidida_em


class AplicarCorrecaoView(OperacaoPedidoMixin, View):
    form_class = OperacaoCorrecaoForm

    def registrar(self, ator, pk, pedido_id, **dados):
        return services.aplicar(ator, pk, pedido_id, **dados).aplicado_em
