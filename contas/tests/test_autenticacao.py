from io import StringIO
import logging
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.db import OperationalError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone


class AutenticacaoTests(TestCase):
    senha = "  segredo fictício de teste  "
    mensagem_recusa = "Não foi possível entrar com os dados informados."

    @classmethod
    def setUpTestData(cls):
        model = get_user_model()
        cls.usuario = model.objects.create_user(username="fiscal-teste", password=cls.senha)
        cls.inativo = model.objects.create_user(username="inativo-teste", password=cls.senha, is_active=False)

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True, raise_request_exception=False)
        self.entrar = reverse("contas:entrar")
        self.acesso = reverse("contas:acesso")
        self.sair = reverse("contas:sair")

    def token(self, *, secure=False):
        return self.client.cookies[settings.CSRF_COOKIE_NAME].value

    def login(self, *, secure=False, **overrides):
        self.client.get(self.entrar, secure=secure)
        data = {"username": self.usuario.username, "password": self.senha, "csrfmiddlewaretoken": self.token()}
        headers = {"HTTP_REFERER": f"https://testserver{self.entrar}"} if secure else {}
        return self.client.post(self.entrar, data | overrides, secure=secure, **headers)

    def assert_retorno_seguro(self, response, destination):
        self.assertRedirects(response, destination, fetch_redirect_response=False)
        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_formulario_e_protecao_do_acesso_anonimo(self):
        response = self.client.get(self.entrar)
        for markup in ('for="id_username"', 'for="id_password"', 'name="csrfmiddlewaretoken"', 'autocomplete="username"', 'autocomplete="current-password"'):
            self.assertContains(response, markup)
        self.assertIn("no-store", response.headers["Cache-Control"])
        response = self.client.get(self.acesso)
        self.assert_retorno_seguro(response, f"{self.entrar}?next={self.acesso}")
        self.assertNotContains(response, "Usuário conectado", status_code=302)

    def test_campos_invalidos_e_limite_do_usuario(self):
        max_length = get_user_model()._meta.get_field("username").max_length
        for data, field, code in (
            ({"username": "  "}, "username", "required"),
            ({"password": " \t "}, "password", "required"),
            ({"password": ""}, "password", "required"),
            ({"username": "a" * (max_length + 1)}, "username", "max_length"),
        ):
            with self.subTest(field=field, code=code):
                response = self.login(**data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].has_error(field, code))
                self.assertNotContains(response, self.senha)
        self.assertNotIn(settings.SESSION_COOKIE_NAME, self.client.cookies)

    def test_recusa_publica_generica_e_senha_sem_aparar(self):
        for username, password in (
            (self.usuario.username, self.senha.strip()),
            ("nao-existe", self.senha),
            (self.inativo.username, self.senha),
        ):
            with self.subTest(username=username):
                response = self.login(username=username, password=password)
                self.assertContains(response, self.mensagem_recusa)
                self.assertNotContains(response, password)
                self.assertNotIn(settings.SESSION_COOKIE_NAME, self.client.cookies)
        self.assert_retorno_seguro(self.login(), self.acesso)

    def test_rotacao_da_sessao_e_ator_autenticado(self):
        old_session = self.client.session
        old_session["indicador"] = "sessao-anonima"
        old_session.save()

        response = self.login(is_staff="true", perfil="Supervisor", usuarioId=str(self.inativo.pk))
        self.assert_retorno_seguro(response, self.acesso)
        self.assertNotEqual(old_session.session_key, self.client.session.session_key)
        self.assertFalse(Session.objects.filter(session_key=old_session.session_key).exists())
        self.assertTrue(response.cookies[settings.SESSION_COOKIE_NAME]["httponly"])

        response = self.client.get(self.acesso)
        self.assertContains(response, self.usuario.username)
        self.assertIn("no-store", response.headers["Cache-Control"])
        self.assertFalse(response.wsgi_request.user.is_staff)
        self.assertNotContains(response, "Supervisor")
        self.assert_retorno_seguro(self.client.get(self.entrar), self.acesso)
        self.assert_retorno_seguro(self.login(username=self.inativo.username), self.acesso)
        self.assertEqual(self.client.get(self.acesso).wsgi_request.user.pk, self.usuario.pk)

    def test_destino_revalidado_apos_post(self):
        internal = f"{self.acesso}?origem=entrada"
        response = self.client.get(self.entrar, {"next": internal})
        self.assertContains(response, f'name="next" value="{internal}"')
        self.assert_retorno_seguro(self.login(next=internal), internal)
        self.assert_retorno_seguro(self.login(next=f"http://testserver{internal}"), f"http://testserver{internal}")

        for target in (
            "https://externo.invalid/", "//externo.invalid/", "javascript:alert(1)",
            r"/\externo.invalid/", self.entrar, self.sair, "/conta/%65ntrar/", "/conta/../conta/sair/",
            "/conta/..//externo.invalid/",
        ):
            with self.subTest(target=target):
                self.assert_retorno_seguro(self.login(next=target), self.acesso)
        self.assert_retorno_seguro(self.login(secure=True, next=f"http://testserver{self.acesso}"), self.acesso)

    def test_csrf_exige_token_e_rotaciona_apos_login(self):
        self.client.get(self.entrar)
        old_token = self.token()
        credentials = {"username": self.usuario.username, "password": self.senha}
        for data in (credentials, credentials | {"csrfmiddlewaretoken": "invalido"}):
            response = self.client.post(self.entrar, data)
            self.assertContains(response, "Envio não confirmado", status_code=403)
            self.assertNotIn(settings.SESSION_COOKIE_NAME, self.client.cookies)
        self.assert_retorno_seguro(self.login(), self.acesso)
        self.assertNotEqual(self.token(), old_token)
        response = self.client.post(self.sair, {"csrfmiddlewaretoken": old_token})
        self.assertContains(response, "Envio não confirmado", status_code=403)
        self.assertEqual(self.client.get(self.acesso).status_code, 200)

    def test_conta_inativa_e_sessao_expirada_sao_recusadas(self):
        self.login()
        session_key = self.client.session.session_key
        Session.objects.filter(session_key=session_key).update(expire_date=timezone.now())
        self.assert_retorno_seguro(self.client.get(self.acesso), f"{self.entrar}?next={self.acesso}")

        self.login()
        get_user_model().objects.filter(pk=self.usuario.pk).update(is_active=False)
        self.assert_retorno_seguro(self.client.get(self.acesso), f"{self.entrar}?next={self.acesso}")

    def test_saida_post_invalida_a_chave_no_postgresql(self):
        self.login()
        key = self.client.session.session_key
        for method in (self.client.get, self.client.head):
            self.assertEqual(method(self.sair).status_code, 405)
        self.assertEqual(self.client.post(self.sair, {}).status_code, 403)
        self.assertTrue(Session.objects.filter(session_key=key).exists())
        self.assertEqual(self.client.get(self.acesso).status_code, 200)

        self.assert_retorno_seguro(self.client.post(self.sair, {"csrfmiddlewaretoken": self.token()}), self.entrar)
        self.assertFalse(Session.objects.filter(session_key=key).exists())
        self.client.cookies[settings.SESSION_COOKIE_NAME] = key
        self.assert_retorno_seguro(self.client.get(self.acesso), f"{self.entrar}?next={self.acesso}")
        self.assert_retorno_seguro(self.client.post(self.sair, {"csrfmiddlewaretoken": self.token()}), self.entrar)

    def test_erro_operacional_na_consulta_de_credenciais(self):
        with patch("contas.forms.AuthenticationForm.clean", side_effect=OperationalError("segredo da conexão")):
            response = self.login()
        self.assertContains(response, "Acesso indisponível", status_code=503)
        self.assertNotContains(response, "segredo da conexão", status_code=503)
        self.assertNotIn(settings.SESSION_COOKIE_NAME, self.client.cookies)

    def test_falha_na_gravacao_de_sessao_apos_a_view(self):
        save_original = SessionStore.save

        def save(store, must_create=False):
            if not must_create:
                raise OperationalError("não persistido")
            return save_original(store, must_create=True)

        with patch.object(SessionStore, "save", save):
            response = self.login()
        self.assertContains(response, "Acesso indisponível", status_code=503)
        self.assertNotIn(settings.SESSION_COOKIE_NAME, response.cookies)
        self.assert_retorno_seguro(self.client.get(self.acesso), f"{self.entrar}?next={self.acesso}")

    def test_erros_registram_status_sem_credenciais_nem_referer(self):
        logger = logging.getLogger("django.security.csrf")
        handler = next(handler for handler in logger.handlers if handler.name == "request_errors")
        stream = StringIO()
        initial_stream = handler.setStream(stream)
        self.addCleanup(handler.setStream, initial_stream)

        response = self.client.post(self.entrar, {"password": self.senha}, secure=True, HTTP_REFERER="https://externo.invalid/segredo")
        self.assertContains(response, "Envio não confirmado", status_code=403)
        self.assertNotContains(response, self.senha, status_code=403)
        self.assertNotContains(response, "externo.invalid", status_code=403)
        self.assertIn("HTTP 403", stream.getvalue())
        self.assertNotIn("externo.invalid", stream.getvalue())
        self.assertNotIn(self.senha, stream.getvalue())

    def test_head_options_e_metodos_recusados(self):
        self.assertEqual(self.client.head(self.entrar).content, b"")
        response = self.client.options(self.sair)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.headers["Allow"].split(", ")), {"POST", "OPTIONS"})
        self.assertEqual(self.client.trace(self.entrar).status_code, 405)
        self.client.get(self.entrar)
        self.assertEqual(self.client.post(self.acesso, {"csrfmiddlewaretoken": self.token()}).status_code, 405)
