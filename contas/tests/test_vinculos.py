from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from threading import Barrier
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, OperationalError, connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from contas.models import HistoricoUsuario, Perfil, Usuario
from contas.vinculos import VinculoDesatualizado, alterar
from estabelecimentos.models import Estabelecimento, VinculoEstabelecimento


class VinculoEstabelecimentoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user("admin-vinculo", perfil=Perfil.ADMINISTRADOR)
        cls.cliente = Usuario.objects.create_user(
            "cliente", perfil=Perfil.ESTABELECIMENTO, password="credencial fictícia de testes",
        )
        cls.fiscal = Usuario.objects.create_user("fiscal", perfil=Perfil.FISCALIZACAO)
        cls.unidade_a = Estabelecimento.objects.create(nome="Unidade Alfa", documento="sigiloso-001")
        cls.unidade_b = Estabelecimento.objects.create(nome="Unidade Beta")
        cls.inativa = Estabelecimento.objects.create(nome="Unidade Inativa", ativo=False)

    def setUp(self):
        self.admin_http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        self.admin_http.force_login(self.admin)
        self.gestao = reverse("gestao_contas:vinculo", args=[self.cliente.pk])
        self.detalhe = reverse("contas:estabelecimento", args=[self.unidade_a.pk])
        self.admin_http.get(self.gestao)
        self.navegador_cliente = Client(enforce_csrf_checks=True)
        self.navegador_cliente.force_login(self.cliente)

    def post(self, versao, unidade_id, http=None):
        http = http or self.admin_http
        return http.post(self.gestao, {
            "versao": versao, "estabelecimento_id": unidade_id,
            "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
        })

    def test_atribuicao_e_isolamento_de_unidades_na_sessao_atual(self):
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 404)
        chave = self.navegador_cliente.session.session_key
        self.assertEqual(self.post(1, self.unidade_a.pk).status_code, 302)
        self.assertEqual(self.post(1, self.unidade_a.pk).status_code, 302)
        vinculo = VinculoEstabelecimento.objects.get(usuario=self.cliente)
        self.assertEqual(vinculo.criado_por, self.admin)
        self.assertEqual(vinculo.estabelecimento, self.unidade_a)
        self.assertEqual(self.navegador_cliente.session.session_key, chave)
        resposta = self.navegador_cliente.get(self.detalhe)
        self.assertContains(resposta, "Unidade Alfa")
        self.assertNotContains(resposta, "sigiloso-001")
        self.assertIn("no-store", resposta.headers["Cache-Control"])
        outra = self.navegador_cliente.get(reverse("contas:estabelecimento", args=[self.unidade_b.pk]))
        inexistente = self.navegador_cliente.get(reverse("contas:estabelecimento", args=[99999]))
        self.assertNotContains(outra, "Unidade Beta", status_code=404)
        self.assertEqual(outra.content, inexistente.content)
        self.assertContains(self.navegador_cliente.get(reverse("contas:acesso")), "Meu estabelecimento")

    def test_retirada_faz_efeito_na_mesma_sessao_e_preserva_registro(self):
        self.post(1, self.unidade_a.pk)
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 200)
        chave = self.navegador_cliente.session.session_key
        self.assertEqual(self.post(2, 0).status_code, 302)
        self.assertEqual(self.post(2, 0).status_code, 302)
        self.assertEqual(self.navegador_cliente.session.session_key, chave)
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 404)
        self.assertNotContains(self.navegador_cliente.get(reverse("contas:acesso")), "Meu estabelecimento")
        vinculo = VinculoEstabelecimento.objects.get(usuario=self.cliente)
        self.assertEqual(vinculo.encerrado_por, self.admin)
        self.assertIsNotNone(vinculo.encerrado_em)

    def test_troca_encerra_anterior_e_recusa_formulario_antigo(self):
        self.post(1, self.unidade_a.pk)
        self.assertEqual(self.post(1, self.unidade_b.pk).status_code, 409)
        self.assertEqual(self.post(2, self.unidade_b.pk).status_code, 302)
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 404)
        atual = VinculoEstabelecimento.objects.get(usuario=self.cliente, encerrado_em__isnull=True)
        self.assertEqual(atual.estabelecimento, self.unidade_b)
        with self.assertRaises(IntegrityError), transaction.atomic():
            VinculoEstabelecimento.objects.create(
                usuario=self.cliente, estabelecimento=self.unidade_a, criado_por=self.admin,
            )
        self.assertEqual(VinculoEstabelecimento.objects.filter(usuario=self.cliente).count(), 2)

    def test_inativar_unidade_ou_trocar_perfil_nega_acesso(self):
        self.post(1, self.unidade_a.pk)
        Estabelecimento.objects.filter(pk=self.unidade_a.pk).update(ativo=False)
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 404)
        Estabelecimento.objects.filter(pk=self.unidade_a.pk).update(ativo=True)
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 200)

        resposta = self.admin_http.post(reverse("gestao_contas:editar", args=[self.cliente.pk]), {
            "versao": 2, "nome": "Pessoa de teste", "perfil": Perfil.FISCALIZACAO, "situacao": "1",
            "csrfmiddlewaretoken": self.admin_http.cookies[settings.CSRF_COOKIE_NAME].value,
        })
        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(self.navegador_cliente.get(self.detalhe).status_code, 404)
        self.assertEqual(VinculoEstabelecimento.objects.get(usuario=self.cliente).encerrado_por, self.admin)
        self.assertEqual(self.admin_http.get(self.gestao).status_code, 404)

    def test_gestao_de_vinculos_exige_admin_e_csrf(self):
        self.navegador_cliente.get(reverse("contas:acesso"))
        self.assertEqual(self.navegador_cliente.get(self.gestao).status_code, 403)
        self.assertEqual(self.post(1, self.unidade_a.pk, http=self.navegador_cliente).status_code, 403)
        self.assertEqual(self.admin_http.post(self.gestao, {"versao": 1, "estabelecimento_id": 1}).status_code, 403)
        self.assertFalse(VinculoEstabelecimento.objects.exists())

    def test_rejeita_unidade_inativa_e_termino_sem_selecao(self):
        self.assertEqual(self.post(1, self.inativa.pk).status_code, 200)
        self.assertFalse(VinculoEstabelecimento.objects.exists())
        self.post(1, self.unidade_a.pk)
        resposta = self.admin_http.post(self.gestao, {
            "versao": 2, "csrfmiddlewaretoken": self.admin_http.cookies[settings.CSRF_COOKIE_NAME].value,
        })
        self.assertTrue(resposta.context["form"].has_error("estabelecimento_id", "required"))
        self.assertTrue(VinculoEstabelecimento.objects.filter(encerrado_em__isnull=True).exists())

    def test_falha_na_troca_preserva_vinculo_anterior(self):
        self.post(1, self.unidade_a.pk)
        with patch("contas.vinculos.VinculoEstabelecimento.objects.create", side_effect=OperationalError):
            self.assertEqual(self.post(2, self.unidade_b.pk).status_code, 503)
        vinculo = VinculoEstabelecimento.objects.get(usuario=self.cliente)
        self.assertIsNone(vinculo.encerrado_em)
        self.assertEqual(vinculo.estabelecimento, self.unidade_a)


class VinculoConcorrenteTests(TransactionTestCase):
    def test_dois_administradores_partindo_da_mesma_versao_trocam_uma_vez(self):
        administradores = [
            Usuario.objects.create_user(f"admin-{numero}", perfil=Perfil.ADMINISTRADOR)
            for numero in (1, 2)
        ]
        cliente = Usuario.objects.create_user("cliente", perfil=Perfil.ESTABELECIMENTO)
        unidades = [Estabelecimento.objects.create(nome=f"Unidade {numero}") for numero in (1, 2)]
        inicio = Barrier(2, timeout=8)

        def conceder(autor_id, unidade_id):
            try:
                inicio.wait()
                alterar(autor_id, cliente.pk, versao=1, estabelecimento_id=unidade_id)
                return "gravado"
            except VinculoDesatualizado:
                return "conflito"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as pool:
            futuros = [pool.submit(conceder, admin.pk, unidade.pk) for admin, unidade in zip(administradores, unidades)]
            self.assertCountEqual([futuro.result(timeout=10) for futuro in futuros], ["gravado", "conflito"])

        self.assertEqual(VinculoEstabelecimento.objects.filter(usuario=cliente).count(), 1)
        cliente.refresh_from_db()
        self.assertEqual(cliente.versao_gestao, 2)


class ProvisionamentoAdministradorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.candidata = Usuario.objects.create_user("gestao-separada", password="credencial de teste")
        cls.inutilizavel = Usuario.objects.create_user("sem-credencial")
        cls.fiscal = Usuario.objects.create_user("fiscal", password="credencial de teste", perfil=Perfil.FISCALIZACAO)

    @patch("contas.management.commands.provisionar_administrador.getuser", return_value="operador-local")
    def test_concede_com_autoria_e_repeticao_segura(self, _getuser):
        for _ in range(2):
            call_command("provisionar_administrador", self.candidata.username, stdout=StringIO())
        self.candidata.refresh_from_db()
        self.assertEqual(self.candidata.perfil, Perfil.ADMINISTRADOR)
        self.assertFalse(self.candidata.is_superuser)
        self.assertFalse(self.candidata.is_staff)
        registro = HistoricoUsuario.objects.get(usuario=self.candidata)
        self.assertIsNone(registro.autor)
        self.assertEqual(registro.operador_tecnico, "operador-local")
        self.assertEqual(registro.alteracoes, {"perfil": {"anterior": "", "atual": Perfil.ADMINISTRADOR}})
        pagina = Client()
        pagina.force_login(self.candidata)
        self.assertEqual(pagina.get(reverse("gestao_contas:lista")).status_code, 200)

    def test_recusa_contas_operacionais_e_sem_credencial(self):
        for nome in (self.inutilizavel.username, self.fiscal.username, "inexistente"):
            with self.subTest(nome=nome), self.assertRaises(CommandError):
                call_command("provisionar_administrador", nome, stdout=StringIO())
        self.assertFalse(HistoricoUsuario.objects.exists())
