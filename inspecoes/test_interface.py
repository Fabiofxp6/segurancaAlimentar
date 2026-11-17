from uuid import UUID, uuid4

from django.conf import settings
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from contas.models import Perfil, Usuario

from . import campo_services
from .campo_arquivos import validar_arquivo
from .models import HistoricoInspecao, ObservacaoInspecao
from .services import atribuir
from .test_campo import foto
from .test_conclusao import preparar_conclusao, responder
from .test_termos import confirmar_resultado


class InterfaceCampoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.inspecao, _, cls.itens = preparar_conclusao()
        cls.fora = Usuario.objects.create_user("fiscal-fora-da-interface", perfil=Perfil.FISCALIZACAO)
        cls.outra = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=cls.inspecao.estabelecimento_id, acao_id=None,
            responsavel_id=cls.fora.pk, participantes_ids=[],
        )

    def sessao(self, usuario):
        navegador = Client(enforce_csrf_checks=True)
        navegador.force_login(usuario)
        return navegador

    def abrir_pagina(self, navegador, nome, *args):
        return navegador.get(reverse(f"inspecoes:{nome}", args=[self.inspecao.pk, *args]))

    def test_observacao_geral_confirmada_e_preservada_no_historico(self):
        navegador = self.sessao(self.fiscal)
        pagina = self.abrir_pagina(navegador, "observacoes")
        url = reverse("inspecoes:observacao_salvar", args=[self.inspecao.pk])
        dados = {
            "operacao_id": str(uuid4()), "texto": "Registro fictício de campo",
            "csrfmiddlewaretoken": navegador.cookies[settings.CSRF_COOKIE_NAME].value,
        }
        cabecalhos = {"X-Contexto-Campo": pagina.context["contexto"]}
        recibo = navegador.post(url, dados, headers=cabecalhos)
        self.assertEqual(recibo.status_code, 200)
        self.assertEqual(navegador.post(url, dados, headers=cabecalhos).json(), recibo.json())
        self.assertEqual(navegador.post(url, {**dados, "texto": "Outro texto"}, headers=cabecalhos).status_code, 409)
        self.assertContains(self.abrir_pagina(navegador, "observacoes"), dados["texto"])
        self.assertEqual(self.abrir_pagina(self.sessao(self.cliente), "observacoes").status_code, 403)
        self.assertEqual(self.abrir_pagina(self.sessao(self.fora), "observacoes").status_code, 404)
        registro = ObservacaoInspecao.objects.get(inspecao=self.inspecao)
        evento = self.inspecao.historico.get(ato=HistoricoInspecao.Ato.OBSERVACAO)
        self.assertEqual(evento.dados, {"observacao": registro.pk})
        with transaction.atomic(), self.assertRaises(IntegrityError):
            ObservacaoInspecao.objects.filter(pk=registro.pk).update(texto="Substituição")
        confirmar_resultado(self.fiscal, self.inspecao, self.itens)
        self.assertEqual(navegador.post(url, dados, headers=cabecalhos).json(), recibo.json())
        novo = {**dados, "operacao_id": str(uuid4())}
        self.assertEqual(navegador.post(url, novo, headers=cabecalhos).status_code, 409)

    def test_galeria_mostra_foto_apenas_a_equipe(self):
        item = self.itens[0]
        responder(self.fiscal, self.inspecao, item, "Sim")
        metadados, conteudo = validar_arquivo(foto())
        operacao = campo_services.salvar_evidencia(
            self.fiscal.pk, self.inspecao.pk, UUID(item["id"]), operacao_id=uuid4(),
            revisao=1, vinculo="item", metadados=metadados, conteudo=conteudo,
        )
        evidencia_id = operacao.resultado["evidencia_id"]
        fiscal = self.sessao(self.fiscal)
        self.assertContains(self.abrir_pagina(fiscal, "galeria"), metadados["nome"])
        imagem = self.abrir_pagina(fiscal, "campo_visualizar", item["id"], evidencia_id)
        self.assertEqual(imagem.status_code, 200)
        self.assertEqual(imagem["Content-Type"], "image/png")
        self.assertTrue(imagem["Content-Disposition"].startswith("inline;"))
        self.assertIn("no-store", imagem["Cache-Control"])
        self.assertEqual(b"".join(imagem.streaming_content), conteudo)
        cliente = self.sessao(self.cliente)
        self.assertEqual(self.abrir_pagina(cliente, "campo_visualizar", item["id"], evidencia_id).status_code, 403)
        self.assertEqual(self.abrir_pagina(self.sessao(self.fora), "galeria").status_code, 404)

    def test_busca_e_abas_de_inspecao_respeitam_o_escopo(self):
        fiscal = self.sessao(self.fiscal)
        url = reverse("inspecoes:lista")
        pagina = fiscal.get(url, {"busca": f"#{self.inspecao.pk}"})
        self.assertContains(pagina, "1 inspeção encontrada")
        self.assertContains(fiscal.get(url, {"busca": str(self.outra.pk)}), "0 inspeções encontradas")
        self.assertContains(fiscal.get(url, {"busca": "Unidade Norte"}), "1 inspeção encontrada")
        self.assertContains(fiscal.get(url, {"recorte": "finalizadas"}), "0 inspeções encontradas")
        confirmar_resultado(self.fiscal, self.inspecao, self.itens)
        self.assertContains(fiscal.get(url, {"recorte": "finalizadas"}), "1 inspeção encontrada")
