from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from django.conf import settings
from django.db import IntegrityError, OperationalError, connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from contas.models import Perfil, Usuario

from .models import Checklist, VersaoChecklist
from .services import criar, publicar, salvar_item


class ChecklistTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrador = Usuario.objects.create_user("admin-checklist", perfil=Perfil.ADMINISTRADOR)
        cls.fiscal = Usuario.objects.create_user("fiscal-checklist", perfil=Perfil.FISCALIZACAO)
        cls.cliente = Usuario.objects.create_user("cliente-checklist", perfil=Perfil.ESTABELECIMENTO)
        cls.tecnico = Usuario.objects.create_user("tecnico-checklist", is_superuser=True, is_staff=True)

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, raise_request_exception=False)
        self.client.force_login(self.administrador)
        self.novo = reverse("checklists:criar")
        self.client.get(self.novo)
        self.checklist = Checklist.objects.create(
            titulo="Checklist Fictício", regras="Orientação antiga", referencia="Manual fictício",
            criado_por=self.administrador,
        )
        self.detalhe = reverse("checklists:rascunho", args=[self.checklist.pk])
        self.item_novo = reverse("checklists:item_novo", args=[self.checklist.pk])
        self.publicar = reverse("checklists:publicar", args=[self.checklist.pk])

    def post(self, url, **dados):
        return self.client.post(url, {
            "csrfmiddlewaretoken": self.client.cookies[settings.CSRF_COOKIE_NAME].value, **dados,
        })

    def salvar_item(self, revisao=1, **alteracoes):
        dados = {
            "revisao": revisao, "enunciado": "Item fictício A", "ordem": 3, "peso": "1,250",
            "opcoes": "Satisfatório\n\nRevisar ", "obrigatorio": "on",
        }
        dados.update(alteracoes)
        return self.post(self.item_novo, **dados)

    def test_criar_checklist_e_recusar_titulo_em_branco(self):
        resposta = self.post(self.novo, titulo=" \t ")
        self.assertTrue(resposta.context["form"].has_error("titulo", "required"))
        self.assertEqual(Checklist.objects.count(), 1)
        resposta = self.post(
            self.novo, titulo="  Novo checklist  ", regras="  Regra  ", referencia="Origem fictícia",
            criado_por=self.tecnico.pk, itens='["vazamento"]',
        )
        cadastro = Checklist.objects.get(titulo="Novo checklist")
        self.assertRedirects(resposta, reverse("checklists:rascunho", args=[cadastro.pk]))
        self.assertEqual(cadastro.criado_por, self.administrador)
        self.assertEqual(cadastro.regras, "Regra")
        self.assertEqual(cadastro.itens, [])

    def test_itens_validos_e_ordem_opcoes_e_peso_invalidos(self):
        for alteracoes, campo in (
            ({"enunciado": "  "}, "enunciado"),
            ({"ordem": 0}, "ordem"),
            ({"opcoes": "\n \n"}, "opcoes"),
            ({"opcoes": "Sim\nsim"}, "opcoes"),
            ({"peso": "NaN"}, "peso"),
        ):
            with self.subTest(campo=campo):
                resposta = self.salvar_item(**alteracoes)
                self.assertEqual(resposta.status_code, 200)
                self.assertIn(campo, resposta.context["form"].errors)
        self.assertRedirects(self.salvar_item(), self.detalhe)
        resposta = self.salvar_item(revisao=2, enunciado="Outro item")
        self.assertContains(resposta, "Esta ordem já é usada por outro item.")
        self.assertRedirects(self.salvar_item(revisao=2, ordem=1, enunciado="Primeiro"), self.detalhe)
        self.checklist.refresh_from_db()
        primeiro, segundo = self.checklist.itens
        self.assertEqual(primeiro["ordem"], 1)
        self.assertEqual(segundo["peso"], "1.250")
        self.assertEqual(segundo["opcoes"], ["Satisfatório", "Revisar"])
        self.assertTrue(segundo["obrigatorio"])

    def test_rejeita_publicacao_vazia_sem_csrf_e_por_get(self):
        resposta = self.post(self.publicar, revisao=1)
        self.assertContains(resposta, "Inclua pelo menos um item")
        self.assertEqual(self.client.get(self.publicar).status_code, 405)
        self.assertEqual(self.client.post(self.publicar, {"revisao": 1}).status_code, 403)
        self.assertFalse(VersaoChecklist.objects.exists())

    def test_publicar_nova_versao_preserva_regras_itens_e_autoria_da_anterior(self):
        self.salvar_item()
        resposta = self.post(self.publicar, revisao=2, publicado_por=self.tecnico.pk, finalidade="oficial")
        v1 = self.checklist.versoes.get(numero=1)
        v1_url = reverse("checklists:versao", args=[self.checklist.pk, v1.pk])
        self.assertRedirects(resposta, v1_url)
        self.assertEqual(v1.publicado_por, self.administrador)
        self.assertIsNotNone(v1.publicado_em)
        self.assertEqual(v1.finalidade, VersaoChecklist.Finalidade.DEMONSTRACAO)

        self.assertRedirects(self.post(self.detalhe, revisao=2, titulo="Novo título", regras="Nova regra"), self.detalhe)
        item_url = reverse("checklists:item_editar", args=[self.checklist.pk, v1.itens[0]["id"]])
        self.assertRedirects(self.post(
            item_url, revisao=3, enunciado="Novo enunciado", ordem=3, peso="2,4",
            opcoes="Resposta nova\nOutra resposta", obrigatorio="",
        ), self.detalhe)
        self.assertRedirects(self.post(self.publicar, revisao=2), v1_url)
        resposta_v2 = self.post(self.publicar, revisao=4)
        v2 = self.checklist.versoes.get(numero=2)
        self.assertRedirects(resposta_v2, reverse("checklists:versao", args=[self.checklist.pk, v2.pk]))

        v1.refresh_from_db()
        self.assertEqual((v1.titulo, v1.regras, v1.referencia), (
            "Checklist Fictício", "Orientação antiga", "Manual fictício",
        ))
        self.assertEqual(v1.itens[0]["enunciado"], "Item fictício A")
        self.assertEqual(v1.itens[0]["peso"], "1.250")
        self.assertEqual(v1.itens[0]["id"], v2.itens[0]["id"])
        self.assertFalse(v2.itens[0]["obrigatorio"])
        self.assertContains(self.client.get(v1_url), "Orientação antiga")
        self.assertNotContains(self.client.get(v1_url), "Nova regra")
        self.assertContains(self.client.get(resposta_v2.url), "Novo enunciado")

    def test_rascunho_desatualizado_e_remocao_preservam_versao_publicada(self):
        self.salvar_item()
        self.assertEqual(self.salvar_item(revisao=1, ordem=4).status_code, 409)
        self.assertEqual(self.post(self.publicar, revisao=1).status_code, 409)
        self.post(self.publicar, revisao=2)
        v1 = self.checklist.versoes.get(numero=1)
        item_id = v1.itens[0]["id"]
        remover = reverse("checklists:item_remover", args=[self.checklist.pk, item_id])
        self.assertEqual(self.client.get(remover).status_code, 405)
        self.assertEqual(self.post(remover, revisao=1).status_code, 409)
        self.assertRedirects(self.post(remover, revisao=2), self.detalhe)
        self.checklist.refresh_from_db()
        self.assertEqual(self.checklist.itens, [])
        v1.refresh_from_db()
        self.assertEqual(v1.itens[0]["id"], item_id)

    def test_banco_recusa_edicao_exclusao_e_classificacao_oficial(self):
        self.salvar_item()
        self.post(self.publicar, revisao=2)
        v1 = self.checklist.versoes.get(numero=1)
        with self.assertRaisesRegex(IntegrityError, "imutável"), transaction.atomic():
            self.checklist.versoes.filter(pk=v1.pk).update(titulo="Tentativa")
        with self.assertRaisesRegex(IntegrityError, "imutável"), transaction.atomic():
            self.checklist.versoes.filter(pk=v1.pk).delete()
        with self.assertRaises(IntegrityError), transaction.atomic():
            VersaoChecklist.objects.create(
                checklist=self.checklist, numero=2, revisao_rascunho=3, titulo="Tentativa",
                itens=v1.itens, finalidade="oficial", publicado_por=self.administrador,
            )
        v1.refresh_from_db()
        self.assertEqual(v1.titulo, "Checklist Fictício")

    def test_acesso_a_dados_e_publicacao_exige_perfil_administrador(self):
        self.salvar_item()
        for usuario in (self.fiscal, self.cliente, self.tecnico):
            self.client.force_login(usuario)
            self.client.get(reverse("contas:acesso"))
            resposta = self.client.get(self.detalhe)
            self.assertNotContains(resposta, "Checklist Fictício", status_code=403)
            self.assertIn("no-store", resposta.headers["Cache-Control"])
            self.assertEqual(self.post(self.publicar, revisao=2).status_code, 403)
        self.assertFalse(VersaoChecklist.objects.exists())

    def test_publicacao_com_falha_de_banco_pode_ser_repetida_com_mesma_revisao(self):
        self.salvar_item()
        with patch("checklists.models.VersaoChecklist.save", side_effect=OperationalError("origem restrita")):
            resposta = self.post(self.publicar, revisao=2)
            self.assertContains(resposta, "Operação indisponível", status_code=503)
            self.assertNotContains(resposta, "origem restrita", status_code=503)
        self.assertFalse(self.checklist.versoes.exists())
        self.assertEqual(self.post(self.publicar, revisao=2).status_code, 302)
        self.assertEqual(self.checklist.versoes.get().numero, 1)


class PublicacaoConcorrenteTests(TransactionTestCase):
    def test_duas_publicacoes_da_mesma_revisao_retornam_o_mesmo_id(self):
        autor = Usuario.objects.create_user("publicador", perfil=Perfil.ADMINISTRADOR)
        outro = Usuario.objects.create_user("outro-publicador", perfil=Perfil.ADMINISTRADOR)
        checklist = criar(autor.pk, titulo="Demonstração", referencia="", regras="")
        salvar_item(
            autor.pk, checklist.pk, None, revisao=1, enunciado="Item", ordem=1, peso=None,
            obrigatorio=False, opcoes=["Sim", "Não"],
        )
        inicio = Barrier(2, timeout=8)

        def tentar(autor_id):
            try:
                inicio.wait()
                return publicar(autor_id, checklist.pk, revisao=2).pk
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            futuros = [pool.submit(tentar, pessoa.pk) for pessoa in (autor, outro)]
            ids = [futuro.result(timeout=10) for futuro in futuros]
        self.assertEqual(ids, [checklist.versoes.get().pk] * 2)
