from io import BytesIO

from django.core.exceptions import ValidationError
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from . import documentos_services as services
from .documentos_arquivos import validar_documento
from .documentos_forms import DocumentoEstabelecimentoForm
from .envio_views import ContextoEnvioMixin, contexto_envio
from .models import DocumentoEstabelecimento
from .views import InspecaoMixin


class DocumentosListaView(InspecaoMixin, View):
    def get(self, request):
        pagina = services.listar(request.user.pk, request.GET.get("pagina"))
        return render(request, "documentos/lista.html", {"pagina": pagina, "cliente": True})


class DocumentosInspecaoView(InspecaoMixin, View):
    def get(self, request, pk):
        inspecao, documentos, cliente, pode_enviar, bloqueado = services.consultar_pagina(request.user.pk, pk)
        return render(request, "documentos/inspecao.html", {
            "inspecao": inspecao, "documentos": documentos, "cliente": cliente,
            "pode_enviar": pode_enviar, "contexto": contexto_envio(request) if pode_enviar else "",
            "form": DocumentoEstabelecimentoForm() if pode_enviar else None, "bloqueado": bloqueado,
        })


class DocumentosConexaoView(ContextoEnvioMixin, InspecaoMixin, View):
    def get(self, request, pk):
        services.verificar_envio(request.user.pk, pk)
        return JsonResponse({"conectado": True})


class DocumentosEnviarView(ContextoEnvioMixin, InspecaoMixin, View):
    http_method_names = ["post", "options"]

    def post(self, request, pk):
        services.verificar_envio(request.user.pk, pk)
        form = DocumentoEstabelecimentoForm(request.POST, request.FILES)
        if not form.is_valid():
            erros = [str(mensagem) for lista in form.errors.values() for mensagem in lista]
            return JsonResponse({"erro": " ".join(erros)}, status=400)
        try:
            metadados, conteudo = validar_documento(form.cleaned_data["arquivo"])
            documento = services.salvar(
                request.user.pk, pk, operacao_id=form.cleaned_data["operacao_id"],
                descricao=form.cleaned_data["descricao"], metadados=metadados, conteudo=conteudo,
            )
        except ValidationError as erro:
            return JsonResponse({"erro": " ".join(erro.messages)}, status=400)
        except services.DocumentoDesatualizado as erro:
            return JsonResponse({"erro": str(erro)}, status=409)
        return JsonResponse({
            "operacao_id": str(documento.operacao_id), "confirmado_em": documento.recebido_em.isoformat(),
            "nome": documento.nome, "autor": documento.autor.get_username(), "descricao": documento.descricao,
            "url": reverse("inspecoes:documentos_baixar", args=[pk, documento.pk]),
        })


class DocumentosBaixarView(InspecaoMixin, View):
    def get(self, request, pk, documento_id):
        try:
            documento = services.baixar(request.user.pk, pk, documento_id)
        except DocumentoEstabelecimento.DoesNotExist:
            raise Http404 from None
        resposta = FileResponse(
            BytesIO(documento.conteudo), as_attachment=True, filename=documento.nome, content_type=documento.mime,
        )
        resposta["X-Content-Type-Options"] = "nosniff"
        return resposta
