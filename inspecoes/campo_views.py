from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from . import campo_services as services
from .campo_arquivos import validar_arquivo
from .campo_forms import EvidenciaCampoForm, RespostaCampoForm
from .envio_views import ContextoEnvioMixin, contexto_envio
from .models import EvidenciaCampo
from .views import InspecaoMixin


def _confirmacao(operacao, pk, item_id):
    dados = {
        "operacao_id": str(operacao.operacao_id), "confirmado_em": operacao.confirmado_em.isoformat(),
        **operacao.resultado,
    }
    if "evidencia_id" in dados:
        dados["url"] = reverse("inspecoes:campo_baixar", args=[pk, item_id, dados["evidencia_id"]])
    return JsonResponse(dados)


class CampoListaView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, itens = services.consultar_lista(request.user.pk, pk)
        return render(request, "campo/lista.html", {"inspecao": inspecao, "itens": itens, "pode_revisar": services.pode_gravar(inspecao)})


class CampoItemView(InspecaoMixin, View):
    def get(self, request, pk, item_id):
        inspecao, item, resposta, evidencias = services.consultar_pagina(request.user.pk, pk, item_id)
        gravada = {
            "opcao": resposta.opcao if resposta else "",
            "observacao": resposta.observacao if resposta else "",
            "ha_irregularidade": bool(resposta and resposta.descricao_irregularidade),
            "descricao_irregularidade": resposta.descricao_irregularidade if resposta else "",
            "revisao": resposta.revisao if resposta else 0,
        }
        return render(request, "campo/item.html", {
            "inspecao": inspecao, "item": item, "resposta": resposta, "contexto": contexto_envio(request),
            "pode_gravar": services.pode_gravar(inspecao),
            "form_resposta": RespostaCampoForm(opcoes=item["opcoes"], initial=gravada, auto_id="resposta_%s"),
            "form_arquivo": EvidenciaCampoForm(initial={"revisao": gravada["revisao"]}, auto_id="arquivo_%s"),
            "evidencias": evidencias,
        })


class ContextoCampoMixin(ContextoEnvioMixin, InspecaoMixin):
    pass


class CampoConexaoView(ContextoCampoMixin, View):
    def get(self, request, pk, item_id):
        services.consultar_item(request.user.pk, pk, item_id)
        return JsonResponse({"conectado": True})


class EnvioCampoMixin(ContextoCampoMixin):
    http_method_names = ["post", "options"]

    def post(self, request, pk, item_id):
        _, item, _ = services.consultar_item(request.user.pk, pk, item_id)
        form = self.formulario(request, item)
        if not form.is_valid():
            erros = [str(mensagem) for lista in form.errors.values() for mensagem in lista]
            return JsonResponse({"erro": " ".join(erros)}, status=400)
        try:
            operacao = self.salvar(request.user.pk, pk, item_id, **form.cleaned_data)
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        except services.CampoDesatualizado as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        return _confirmacao(operacao, pk, item_id)


class CampoResponderView(EnvioCampoMixin, View):
    def formulario(self, request, item):
        return RespostaCampoForm(request.POST, opcoes=item["opcoes"])

    def salvar(self, autor_id, pk, item_id, *, ha_irregularidade, **dados):
        return services.salvar_resposta(autor_id, pk, item_id, **dados)


class CampoAnexarView(EnvioCampoMixin, View):
    def formulario(self, request, item):
        return EvidenciaCampoForm(request.POST, request.FILES)

    def salvar(self, autor_id, pk, item_id, *, arquivo, **dados):
        metadados, conteudo = validar_arquivo(arquivo)
        return services.salvar_evidencia(autor_id, pk, item_id, **dados, metadados=metadados, conteudo=conteudo)


class CampoBaixarView(InspecaoMixin, View):
    def get(self, request, pk, item_id, evidencia_id):
        try:
            evidencia = services.baixar(request.user.pk, pk, item_id, evidencia_id)
        except EvidenciaCampo.DoesNotExist:
            raise Http404 from None
        resposta = FileResponse(
            BytesIO(evidencia.conteudo), as_attachment=True, filename=evidencia.nome,
            content_type=evidencia.mime,
        )
        resposta["X-Content-Type-Options"] = "nosniff"
        return resposta
