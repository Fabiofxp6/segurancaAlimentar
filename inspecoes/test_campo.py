from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from threading import Barrier
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import OperationalError, connections
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from PIL import Image

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario
from estabelecimentos.models import Estabelecimento

from .campo_arquivos import LIMITE_BYTES
from .campo_services import salvar_resposta
from .models import EvidenciaCampo, OperacaoCampo, RespostaCampo
from .services import iniciar_diretamente


def montar_inspecao(fiscal):
    checklist = Checklist.objects.create(titulo="Checklist fictício", criado_por=fiscal)
    item_id = uuid4()
    versao = VersaoChecklist.objects.create(
        checklist=checklist, numero=1, revisao_rascunho=1, titulo=checklist.titulo,
        itens=[{"id": str(item_id), "enunciado": "Temperatura adequada?", "ordem": 1,
                "obrigatorio": True, "opcoes": ["Sim", "Não"]}],
        publicado_por=fiscal,
    )
    inspecao = iniciar_diretamente(
        fiscal.pk, operacao=uuid4(), estabelecimento_id=Estabelecimento.objects.create(nome="Unidade").pk,
        checklist_id=checklist.pk,
    )
    return inspecao, versao, item_id


def foto(formato="PNG", nome="foto.png"):
    buffer = BytesIO()
    Image.new("RGB", (4, 3), "blue").save(buffer, format=formato)
    return SimpleUploadedFile(nome, buffer.getvalue(), content_type="application/octet-stream")


class CampoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fiscal = Usuario.objects.create_user("fiscal-campo", perfil=Perfil.FISCALIZACAO)
        cls.outro = Usuario.objects.create_user("fiscal-fora", perfil=Perfil.FISCALIZACAO)
        cls.cliente = Usuario.objects.create_user("cliente", perfil=Perfil.ESTABELECIMENTO)
        cls.inspecao, cls.versao, cls.item = montar_inspecao(cls.fiscal)

    def setUp(self):
        self.http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        self.http.force_login(self.fiscal)
        pagina = self.http.get(self.url("campo_item"))
        self.assertEqual(pagina.status_code, 200)
        self.contexto = pagina.context["contexto"]

    def url(self, nome, *args):
        if nome == "campo":
            args = ()
        else:
            args = (self.item, *args)
        return reverse("inspecoes:" + nome, args=[self.inspecao.pk, *args])

    def post(self, nome, **dados):
        return self.http.post(self.url(nome), {
            "csrfmiddlewaretoken": self.http.cookies[settings.CSRF_COOKIE_NAME].value, **dados,
        }, headers={"X-Contexto-Campo": self.contexto})

    def responder(self, **dados):
        envio = {"operacao_id": uuid4(), "revisao": 0, "opcao": "Sim", "observacao": "Local conferido"}
        return self.post("campo_responder", **{**envio, **dados})

    def anexar(self, **dados):
        envio = {"operacao_id": uuid4(), "revisao": 1, "vinculo": "item", "arquivo": foto()}
        return self.post("campo_anexar", **{**envio, **dados})

    def test_resposta_e_irregularidade_ficam_na_versao_original(self):
        self.assertContains(self.http.get(self.url("campo")), "Sem resposta")
        VersaoChecklist.objects.create(
            checklist=self.versao.checklist, numero=2, revisao_rascunho=2, titulo="Nova versão",
            itens=[{"id": str(self.item), "opcoes": ["Outra"], "enunciado": "Outro item"}],
            publicado_por=self.fiscal,
        )
        resposta = self.responder(opcao="Não", ha_irregularidade="on", descricao_irregularidade="Acima da referência")
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.json()["confirmado_em"])
        registro = RespostaCampo.objects.get()
        self.assertEqual(registro.inspecao, self.inspecao)
        self.assertEqual(registro.item_id, self.item)
        self.assertEqual(registro.alterada_por, self.fiscal)
        self.assertEqual(registro.descricao_irregularidade, "Acima da referência")
        self.assertContains(self.http.get(self.url("campo")), "Salva")

    def test_invalidos_rejeitados_sem_gravacao(self):
        self.assertEqual(self.responder(opcao="De outro checklist").status_code, 400)
        self.assertEqual(self.responder(ha_irregularidade="on").status_code, 400)
        self.assertEqual(self.http.get(reverse(
            "inspecoes:campo_item", args=[self.inspecao.pk, uuid4()],
        )).status_code, 404)
        self.assertEqual(self.http.post(
            self.url("campo_responder"), {"opcao": "Sim"},
            headers={"X-Contexto-Campo": self.contexto},
        ).status_code, 403)
        self.assertFalse(OperacaoCampo.objects.exists())

    def test_repetir_resposta_recupera_confirmacao_sem_sobrescrever(self):
        chave = uuid4()
        primeira = self.responder(operacao_id=chave)
        self.assertEqual(self.responder(operacao_id=chave).json(), primeira.json())
        self.assertEqual(self.responder(operacao_id=chave, observacao="Divergente").status_code, 409)
        self.assertEqual(self.responder().status_code, 409)
        self.assertEqual(self.responder(revisao=1, opcao="Não").json()["revisao"], 2)
        self.assertEqual(self.responder(operacao_id=chave).json(), primeira.json())
        self.assertEqual(RespostaCampo.objects.get().opcao, "Não")
        self.assertEqual(OperacaoCampo.objects.count(), 2)

    def test_arquivo_repetido_preserva_binario_e_irregularidade_original(self):
        self.assertEqual(self.anexar().status_code, 409)
        self.responder(ha_irregularidade="on", descricao_irregularidade="Ocorrência observada")
        chave = uuid4()
        primeira = self.anexar(operacao_id=chave, vinculo="irregularidade")
        self.assertEqual(primeira.status_code, 200)
        self.assertEqual(self.anexar(operacao_id=chave, vinculo="irregularidade").json(), primeira.json())
        self.assertEqual(self.anexar(operacao_id=chave, vinculo="item").status_code, 409)
        self.responder(revisao=1)
        evidencia = EvidenciaCampo.objects.get()
        self.assertEqual(evidencia.autor, self.fiscal)
        self.assertEqual(evidencia.descricao_irregularidade, "Ocorrência observada")
        download = self.http.get(primeira.json()["url"])
        self.assertEqual(download.status_code, 200)
        self.assertIn("attachment", download["Content-Disposition"])
        self.assertEqual(download["Content-Type"], "image/png")
        self.assertEqual(download["X-Content-Type-Options"], "nosniff")
        self.assertIn("no-store", download["Cache-Control"])
        self.assertEqual(b"".join(download.streaming_content), bytes(evidencia.conteudo))

    def test_tipo_real_e_limite_validados_sem_confiar_no_mime(self):
        self.responder()
        self.assertEqual(self.anexar(arquivo=SimpleUploadedFile("falsa.png", b"<html>")).status_code, 400)
        maior = SimpleUploadedFile("grande.png", b"0" * (LIMITE_BYTES + 1), "image/png")
        self.assertEqual(self.anexar(arquivo=maior).status_code, 400)
        self.assertEqual(self.anexar(vinculo="irregularidade").status_code, 400)
        retorno = self.anexar(arquivo=foto("JPEG", "foto.png"))
        self.assertEqual(retorno.status_code, 200)
        registro = EvidenciaCampo.objects.get()
        self.assertEqual(registro.mime, "image/jpeg")
        self.assertEqual(registro.nome, "foto.jpg")

    def test_url_direta_nega_download_de_outro_escopo(self):
        self.responder()
        url = self.anexar().json()["url"]
        acaso = Client()
        acaso.force_login(self.outro)
        self.assertEqual(acaso.get(url).status_code, 404)
        acaso.force_login(self.cliente)
        self.assertEqual(acaso.get(url).status_code, 403)

    def test_troca_de_sessao_bloqueia_operacao_pendente(self):
        self.http.logout()
        self.http.force_login(self.fiscal)
        self.http.get(self.url("campo_item"))
        self.assertEqual(self.responder().status_code, 401)
        sonda = self.http.get(self.url("campo_conexao"), headers={"X-Contexto-Campo": self.contexto})
        self.assertEqual(sonda.status_code, 401)
        self.assertFalse(RespostaCampo.objects.exists())

    def test_falha_ao_persistir_confirmacao_reverte_dado_e_arquivo(self):
        with patch("inspecoes.campo_services.OperacaoCampo.objects.create", side_effect=OperationalError("privado")):
            self.assertEqual(self.responder().status_code, 503)
        self.assertFalse(RespostaCampo.objects.exists())
        self.responder()
        with patch("inspecoes.campo_services.OperacaoCampo.objects.create", side_effect=OperationalError("privado")):
            self.assertEqual(self.anexar().status_code, 503)
        self.assertFalse(EvidenciaCampo.objects.exists())
        self.assertEqual(OperacaoCampo.objects.count(), 1)


class ReenvioCampoTests(TransactionTestCase):
    def test_duas_tentativas_da_mesma_operacao_confirmam_uma_vez(self):
        fiscal = Usuario.objects.create_user("campo", perfil=Perfil.FISCALIZACAO)
        inspecao, _, item_id = montar_inspecao(fiscal)
        chave = uuid4()
        juntos = Barrier(2, timeout=8)

        def enviar():
            try:
                juntos.wait()
                return salvar_resposta(
                    fiscal.pk, inspecao.pk, item_id, operacao_id=chave, revisao=0, opcao="Sim",
                    observacao="", descricao_irregularidade="",
                ).pk
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [executor.submit(enviar) for _ in range(2)]
            ids = [tarefa.result(timeout=10) for tarefa in tarefas]
        self.assertEqual(ids, [OperacaoCampo.objects.get().pk] * 2)
        self.assertEqual(RespostaCampo.objects.get().revisao, 1)
