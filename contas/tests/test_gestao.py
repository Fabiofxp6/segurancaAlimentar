from unittest.mock import patch

from django.conf import settings
from django.db import OperationalError
from django.test import Client, TestCase
from django.urls import reverse

from contas.models import HistoricoUsuario, Perfil, Usuario


class GestaoUsuariosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user("admin-teste", perfil=Perfil.ADMINISTRADOR)
        cls.fiscal = Usuario.objects.create_user(
            "fiscal-teste", password="senha fictícia dos testes", perfil=Perfil.FISCALIZACAO,
            nome="Fiscal Fictício",
        )
        cls.tecnico = Usuario.objects.create_user("tecnico-teste", is_superuser=True, is_staff=True)

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, raise_request_exception=False)
        self.client.force_login(self.admin)
        self.lista = reverse("gestao_contas:lista")
        self.novo = reverse("gestao_contas:criar")
        self.editar = reverse("gestao_contas:editar", args=[self.fiscal.pk])
        self.assertEqual(self.client.get(self.novo).status_code, 200)

    def post(self, route, data):
        return self.client.post(route, {
            **data, "csrfmiddlewaretoken": self.client.cookies[settings.CSRF_COOKIE_NAME].value,
        })

    def test_cadastra_sem_senha_e_historico_registra_somente_dados_cadastrais(self):
        dados = {
            "nome": "Mercado de teste", "username": "mercado-teste", "perfil": Perfil.ESTABELECIMENTO,
            "password": "texto forjado", "is_staff": "true", "is_superuser": "true",
            "is_active": "true", "autor": self.fiscal.pk,
        }
        self.assertRedirects(self.post(self.novo, dados), self.lista)
        conta = Usuario.objects.get(username="mercado-teste")
        self.assertFalse(conta.has_usable_password())
        self.assertFalse(conta.is_staff)
        self.assertFalse(conta.is_superuser)
        self.assertFalse(conta.is_active)
        self.assertEqual(conta.perfil, Perfil.ESTABELECIMENTO)
        evento = HistoricoUsuario.objects.get(usuario=conta)
        self.assertEqual(evento.autor_id, self.admin.pk)
        self.assertNotIn("password", evento.alteracoes)
        self.assertNotIn("is_superuser", evento.alteracoes)
        resposta = self.client.get(self.lista)
        self.assertContains(resposta, "Mercado de teste")
        self.assertNotContains(resposta, self.fiscal.password)
        self.assertNotContains(resposta, self.tecnico.username)

        editar = reverse("gestao_contas:editar", args=[conta.pk])
        resposta = self.post(editar, {
            "nome": conta.nome, "perfil": conta.perfil, "situacao": "1", "versao": 1,
        })
        self.assertContains(resposta, "A conta precisa de uma credencial antes de ser ativada.")
        conta.refresh_from_db()
        self.assertFalse(conta.is_active)
        self.assertEqual(HistoricoUsuario.objects.filter(usuario=conta).count(), 1)

    def test_rejeita_duplicidade_nome_vazio_perfis_nao_concediveis_e_csrf(self):
        self.assertEqual(self.client.post(self.novo, {"nome": "Tentativa"}).status_code, 403)
        dados = {"nome": "Nome", "username": "nome-unico", "perfil": Perfil.FISCALIZACAO}
        for alteracao, campo in (
            ({"nome": "   "}, "nome"),
            ({"username": self.fiscal.username}, "username"),
            ({"perfil": "supervisor"}, "perfil"),
            ({"perfil": Perfil.ADMINISTRADOR}, "perfil"),
        ):
            with self.subTest(alteracao=alteracao):
                resposta = self.post(self.novo, {**dados, **alteracao})
                self.assertEqual(resposta.status_code, 200)
                self.assertIn(campo, resposta.context["form"].errors)
        self.assertEqual(Usuario.objects.count(), 3)
        self.assertFalse(HistoricoUsuario.objects.exists())

    def test_admin_nao_edita_outro_admin_nem_conta_tecnica_por_url(self):
        outro_admin = Usuario.objects.create_user("outro-admin", perfil=Perfil.ADMINISTRADOR)
        for alvo in (self.admin, outro_admin, self.tecnico):
            url = reverse("gestao_contas:editar", args=[alvo.pk])
            self.assertEqual(self.client.get(url).status_code, 404)
            resposta = self.post(url, {
                "nome": "Alterado", "perfil": Perfil.FISCALIZACAO, "situacao": "0", "versao": 1,
            })
            self.assertEqual(resposta.status_code, 404)
        self.assertFalse(HistoricoUsuario.objects.exists())

    def test_post_direto_de_fiscal_negado_com_csrf_valido(self):
        self.client.force_login(self.fiscal)
        self.client.get(reverse("contas:acesso"))
        self.assertEqual(self.client.get(self.lista).status_code, 403)
        self.assertEqual(self.client.get(self.editar).status_code, 403)
        resposta = self.post(self.novo, {"nome": "Tentativa", "username": "outro", "perfil": Perfil.FISCALIZACAO})
        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(Usuario.objects.filter(username="outro").exists())

    def test_inativacao_bloqueia_requisicao_seguinte_e_preserva_autoria(self):
        outro_cliente = Client()
        outro_cliente.force_login(self.fiscal)
        acesso = reverse("contas:acesso")
        self.assertEqual(outro_cliente.get(acesso).status_code, 200)

        atualizar = {"nome": "Fiscal Atualizado", "perfil": Perfil.FISCALIZACAO, "situacao": "0", "versao": 1}
        self.assertRedirects(self.post(self.editar, atualizar), self.lista)
        self.assertContains(
            self.post(self.editar, atualizar), "Reabra o cadastro", status_code=409,
        )
        resposta = outro_cliente.get(acesso)
        self.assertEqual(resposta.status_code, 302)
        self.assertIn(reverse("contas:entrar"), resposta.url)
        evento = HistoricoUsuario.objects.get(usuario=self.fiscal)
        self.assertEqual(evento.autor_id, self.admin.pk)
        self.assertEqual(evento.alteracoes["is_active"], {"anterior": True, "atual": False})
        self.assertEqual(evento.versao, 2)

    def test_falha_no_historico_reverte_nova_conta(self):
        with patch("contas.services.HistoricoUsuario.objects.create", side_effect=OperationalError("restrito")):
            resposta = self.post(self.novo, {
                "nome": "Falha", "username": "falha-historico", "perfil": Perfil.FISCALIZACAO,
            })
        self.assertContains(resposta, "Operação indisponível", status_code=503)
        self.assertNotContains(resposta, "restrito", status_code=503)
        self.assertFalse(Usuario.objects.filter(username="falha-historico").exists())


    def test_define_senha_no_cadastro_e_ativa_pela_edicao(self):
        senha = "  credencial inicial fictícia  "
        dados = {
            "nome": "Nova pessoa fiscal", "username": "fiscal-com-credencial", "perfil": Perfil.FISCALIZACAO,
            "senha": senha, "confirmar_senha": senha,
        }
        self.assertRedirects(self.post(self.novo, dados), self.lista)
        conta = Usuario.objects.get(username=dados["username"])
        self.assertFalse(conta.is_active)
        self.assertTrue(conta.check_password(senha))
        self.assertFalse(conta.check_password(senha.strip()))
        self.assertNotEqual(conta.password, senha)

        editar = reverse("gestao_contas:editar", args=[conta.pk])
        pagina = self.client.get(editar)
        self.assertContains(pagina, "Senha configurada")
        self.assertNotContains(pagina, conta.password)
        self.assertNotContains(pagina, senha)
        evento = HistoricoUsuario.objects.get(usuario=conta)
        self.assertEqual(evento.alteracoes["credencial"], {"acao": "definida"})
        self.assertNotIn(senha, str(evento.alteracoes))
        self.assertNotIn(conta.password, str(evento.alteracoes))

        titular = Client()
        dados_login = {"username": conta.username, "password": senha}
        self.assertFalse(titular.login(**dados_login))
        self.assertRedirects(self.post(editar, {
            "nome": conta.nome, "perfil": conta.perfil, "situacao": "1", "versao": conta.versao_gestao,
        }), self.lista)
        self.assertTrue(titular.login(**dados_login))

    def test_redefine_senha_encerra_sessao_anterior_e_rejeita_versao_reutilizada(self):
        titular = Client()
        titular.force_login(self.fiscal)
        acesso = reverse("contas:acesso")
        rota_senha = reverse("gestao_contas:senha", args=[self.fiscal.pk])
        nova = "credencial redefinida de teste"
        self.assertEqual(titular.get(acesso).status_code, 200)

        pagina = self.client.get(rota_senha)
        self.assertContains(pagina, "Confirmar nova senha")
        self.assertNotContains(pagina, self.fiscal.password)
        self.assertIn("no-store", pagina["Cache-Control"])
        antigo = self.fiscal.password
        dados = {"senha": nova, "confirmar_senha": nova, "versao": self.fiscal.versao_gestao}
        self.assertRedirects(self.post(rota_senha, dados), self.editar)
        self.fiscal.refresh_from_db()
        self.assertNotEqual(self.fiscal.password, antigo)
        self.assertTrue(self.fiscal.check_password(nova))
        self.assertFalse(self.fiscal.check_password("senha fictícia dos testes"))
        self.assertEqual(titular.get(acesso).status_code, 302)
        self.assertEqual(self.client.get(self.editar).status_code, 200)
        self.assertTrue(titular.login(username=self.fiscal.username, password=nova))

        evento = HistoricoUsuario.objects.get(usuario=self.fiscal)
        self.assertEqual(evento.autor_id, self.admin.pk)
        self.assertEqual(evento.alteracoes, {"credencial": {"acao": "redefinida"}})
        self.assertContains(self.post(rota_senha, dados), "Reabra o cadastro", status_code=409)
        self.assertEqual(HistoricoUsuario.objects.filter(usuario=self.fiscal).count(), 1)

    def test_redefinicao_invalida_nao_devolve_os_campos_e_nao_muda_senha(self):
        rota_senha = reverse("gestao_contas:senha", args=[self.fiscal.pk])
        senha = "entrada sigilosa fictícia"
        valores = [
            (senha, "outra senha fictícia", "As senhas precisam ser iguais."),
            ("   ", "   ", "Informe uma senha que contenha caracteres além de espaços."),
        ]
        for primeira, segunda, mensagem in valores:
            resposta = self.post(rota_senha, {
                "senha": primeira, "confirmar_senha": segunda, "versao": 1,
            })
            self.assertContains(resposta, mensagem)
            self.assertNotContains(resposta, senha)
            self.assertNotContains(resposta, "outra senha fictícia")
        self.fiscal.refresh_from_db()
        self.assertTrue(self.fiscal.check_password("senha fictícia dos testes"))
        self.assertFalse(HistoricoUsuario.objects.exists())

    def test_redefinicao_exige_administrador_escopo_e_csrf(self):
        comum_sem_perfil = Usuario.objects.create_user("candidato-sem-perfil")
        rota_senha = reverse("gestao_contas:senha", args=[self.fiscal.pk])
        dados = {"senha": "senha teste", "confirmar_senha": "senha teste", "versao": 1}
        self.assertEqual(self.client.post(rota_senha, dados).status_code, 403)
        for alvo in (self.admin, self.tecnico, comum_sem_perfil):
            rota = reverse("gestao_contas:senha", args=[alvo.pk])
            self.assertEqual(self.client.get(rota).status_code, 404)
            self.assertEqual(self.post(rota, dados).status_code, 404)
        self.client.force_login(self.fiscal)
        self.client.get(reverse("contas:acesso"))
        self.assertEqual(self.client.get(rota_senha).status_code, 403)
        self.assertEqual(self.post(rota_senha, dados).status_code, 403)
        self.assertFalse(HistoricoUsuario.objects.exists())

    def test_falha_na_auditoria_de_senha_reverte_a_redefinicao(self):
        rota_senha = reverse("gestao_contas:senha", args=[self.fiscal.pk])
        senha = "credencial fictícia que não deve aparecer"
        with patch("contas.services.HistoricoUsuario.objects.create", side_effect=OperationalError("restrito")):
            resposta = self.post(rota_senha, {"senha": senha, "confirmar_senha": senha, "versao": 1})
        self.assertContains(resposta, "Operação indisponível", status_code=503)
        self.assertNotContains(resposta, senha, status_code=503)
        self.fiscal.refresh_from_db()
        self.assertTrue(self.fiscal.check_password("senha fictícia dos testes"))
        self.assertEqual(self.fiscal.versao_gestao, 1)
