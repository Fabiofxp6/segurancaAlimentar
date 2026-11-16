from io import StringIO
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import path
from django.views import View


class AcessoNegado(View):
    def get(self, request):
        raise PermissionDenied("detalhe-interno-de-teste")


class FalhaInterna(View):
    def get(self, request):
        raise RuntimeError("detalhe-interno-de-teste")


urlpatterns = [
    path("negado/", AcessoNegado.as_view()),
    path("falha/", FalhaInterna.as_view()),
]


@override_settings(ROOT_URLCONF=__name__, DEBUG=False)
class PaginasDeErroTests(SimpleTestCase):
    def test_pagina_e_log_revelam_apenas_a_falha_publica(self):
        logger = logging.getLogger("django.request")
        handler = next(handler for handler in logger.handlers if handler.name == "request_errors")
        output = StringIO()
        initial_stream = handler.setStream(output)
        self.addCleanup(handler.setStream, initial_stream)
        client = Client(raise_request_exception=False)

        for url, code, title in (
            ("/negado/", 403, "Acesso negado"),
            ("/ausente/", 404, "Página não encontrada"),
            ("/falha/?valor=dado-privado-de-teste", 500, "Erro no servidor"),
        ):
            with self.subTest(code=code):
                response = client.get(url)
                self.assertContains(response, title, status_code=code)
                self.assertNotContains(response, "detalhe-interno-de-teste", status_code=code)

        log = output.getvalue()
        self.assertIn("ERROR django.request HTTP 500", log)
        self.assertNotIn("detalhe-interno-de-teste", log)
        self.assertNotIn("dado-privado-de-teste", log)


class IdentidadeTests(TestCase):
    def test_usuario_customizado_persiste_com_senha_codificada(self):
        usuario = get_user_model()
        senha = "Senha fictícia da I01!"
        conta = usuario.objects.create_user(username="fiscal-teste", password=senha)
        conta.refresh_from_db()

        self.assertEqual(usuario._meta.label, "contas.Usuario")
        self.assertEqual(usuario._meta.pk.get_internal_type(), "BigAutoField")
        self.assertEqual(connection.vendor, "postgresql")
        self.assertNotEqual(conta.password, senha)
        self.assertTrue(conta.check_password(senha))
        self.assertTrue(conta.is_active)
        self.assertFalse(conta.is_staff)
        self.assertFalse(conta.is_superuser)

    def test_falha_antes_do_commit_reverte_a_gravacao(self):
        usuario = get_user_model()
        with self.assertRaisesRegex(RuntimeError, "falha simulada"):
            with transaction.atomic():
                usuario.objects.create_user(username="usuario-temporario")
                raise RuntimeError("falha simulada")

        self.assertFalse(usuario.objects.filter(username="usuario-temporario").exists())
