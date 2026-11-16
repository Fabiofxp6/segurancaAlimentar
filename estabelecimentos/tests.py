from unittest.mock import patch

from django.conf import settings
from django.db import IntegrityError, OperationalError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from contas.models import Perfil, Usuario

from .models import Estabelecimento, HistoricoEstabelecimento


class CadastroEstabelecimentosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrador = Usuario.objects.create_user("admin-teste", perfil=Perfil.ADMINISTRADOR)
        cls.fiscal = Usuario.objects.create_user("fiscal-teste", perfil=Perfil.FISCALIZACAO)
        cls.cliente = Usuario.objects.create_user("cliente-teste", perfil=Perfil.ESTABELECIMENTO)
        cls.tecnico = Usuario.objects.create_user("tecnico-teste", is_staff=True, is_superuser=True)
        cls.inativo = Usuario.objects.create_user(
            "inativo-teste", perfil=Perfil.ADMINISTRADOR, is_active=False,
        )
        cls.existente = Estabelecimento.objects.create(nome="Café Fictício", documento="0001-7")

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, raise_request_exception=False)
        self.lista = reverse("estabelecimentos:lista")
        self.novo = reverse("estabelecimentos:criar")
        self.editar = reverse("estabelecimentos:editar", args=[self.existente.pk])

    def post(self, route, data):
        return self.client.post(route, {
            **data, "csrfmiddlewaretoken": self.client.cookies[settings.CSRF_COOKIE_NAME].value,
        })

    def formulario(self):
        self.client.force_login(self.administrador)
        self.assertEqual(self.client.get(self.novo).status_code, 200)

    def test_estabelecimento_cadastrado_com_documento_textual_e_historico(self):
        self.formulario()
        response = self.post(self.novo, {
            "nome": "  Mercado Fictício  ", "documento": " 000.7-5 ", "ativo": "0",
            "autor": self.fiscal.pk, "versao": 99,
        })
        self.assertRedirects(response, self.lista)
        self.assertContains(self.client.get(self.lista), "Mercado Fictício")

        cadastro = Estabelecimento.objects.get(nome="Mercado Fictício")
        self.assertEqual(cadastro.documento, "000.7-5")
        self.assertTrue(cadastro.ativo)
        self.assertEqual(cadastro.versao, 1)
        evento = HistoricoEstabelecimento.objects.get(estabelecimento=cadastro)
        self.assertEqual(evento.autor, self.administrador)
        self.assertEqual(evento.alteracoes["documento"], {"atual": "000.7-5"})

    def test_rejeita_nome_vazio_espacos_e_csrf_invalido(self):
        self.formulario()
        self.assertEqual(self.client.post(self.novo, {"nome": "Sem token"}).status_code, 403)
        for data in ({}, {"nome": ""}, {"nome": " \t "}):
            response = self.post(self.novo, data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].has_error("nome", "required"))
        self.assertEqual(Estabelecimento.objects.count(), 1)
        self.assertFalse(HistoricoEstabelecimento.objects.exists())

    def test_edicao_inativacao_e_conflito_preservam_chave_e_historico(self):
        self.formulario()
        self.assertContains(self.client.get(self.editar), "0001-7")
        anterior = self.existente.pk
        dados = {"nome": "Café Editado", "documento": "0003-2", "ativo": "0", "versao": 1}
        self.assertRedirects(self.post(self.editar, dados), self.lista)
        self.assertContains(self.post(self.editar, {**dados, "nome": "Desatualizado"}), "Reabra o cadastro", status_code=409)
        self.assertRedirects(self.post(self.editar, {**dados, "versao": 2}), self.lista)

        self.existente.refresh_from_db()
        self.assertEqual(self.existente.pk, anterior)
        self.assertEqual(self.existente.nome, "Café Editado")
        self.assertEqual(self.existente.versao, 2)
        self.assertFalse(self.existente.ativo)
        historico = HistoricoEstabelecimento.objects.get(estabelecimento=self.existente)
        self.assertEqual(historico.alteracoes["ativo"], {"anterior": True, "atual": False})
        self.assertEqual(historico.alteracoes["documento"], {"anterior": "0001-7", "atual": "0003-2"})

    def test_fiscal_cliente_e_tecnico_sem_perfil_negados_inclusive_por_post(self):
        for usuario in (self.fiscal, self.cliente, self.tecnico):
            with self.subTest(usuario=usuario.username):
                self.client.force_login(usuario)
                self.client.get(reverse("contas:acesso"))
                for url in (self.lista, self.novo, self.editar, f"{self.lista}999999/"):
                    resposta = self.client.get(url)
                    self.assertNotContains(resposta, self.existente.nome, status_code=403)
                    self.assertIn("no-store", resposta.headers["Cache-Control"])
                for url in (self.novo, self.editar):
                    response = self.post(url, {"nome": "Fraude", "perfil": Perfil.ADMINISTRADOR})
                    self.assertEqual(response.status_code, 403)
        self.assertEqual(Estabelecimento.objects.count(), 1)
        self.assertFalse(HistoricoEstabelecimento.objects.exists())

    def test_login_exigido_de_anonimo_e_de_conta_inativa(self):
        entrar = reverse("contas:entrar")
        self.assertRedirects(self.client.get(self.lista), f"{entrar}?next={self.lista}", fetch_redirect_response=False)
        self.client.force_login(self.inativo)
        self.assertRedirects(self.client.get(self.editar), f"{entrar}?next={self.editar}", fetch_redirect_response=False)

    def test_perda_do_perfil_e_revalidada_na_mesma_sessao(self):
        self.formulario()
        session_key = self.client.session.session_key
        Usuario.objects.filter(pk=self.administrador.pk).update(perfil=Perfil.FISCALIZACAO)
        self.assertEqual(self.client.session.session_key, session_key)
        self.assertEqual(self.client.get(self.editar).status_code, 403)
        self.assertEqual(self.post(self.novo, {"nome": "Negado"}).status_code, 403)
        self.assertFalse(Estabelecimento.objects.filter(nome="Negado").exists())

    def test_falha_ao_registrar_historico_reverte_criacao_e_edicao(self):
        self.formulario()
        with patch(
            "estabelecimentos.services.HistoricoEstabelecimento.objects.create",
            side_effect=OperationalError("detalhe não público"),
        ):
            for url, data in (
                (self.novo, {"nome": "Não confirmado"}),
                (self.editar, {"nome": "Não confirmado", "ativo": "0", "versao": 1}),
            ):
                resposta = self.post(url, data)
                self.assertContains(resposta, "Operação indisponível", status_code=503)
                self.assertNotContains(resposta, "detalhe não público", status_code=503)
        self.assertEqual(Estabelecimento.objects.count(), 1)
        self.existente.refresh_from_db()
        self.assertTrue(self.existente.ativo)
        self.assertEqual(self.existente.versao, 1)
        self.assertFalse(HistoricoEstabelecimento.objects.exists())

    def test_perfil_supervisor_recusado_pelo_banco(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Usuario.objects.filter(pk=self.fiscal.pk).update(perfil="supervisor")
        self.fiscal.refresh_from_db()
        self.assertEqual(self.fiscal.perfil, Perfil.FISCALIZACAO)
