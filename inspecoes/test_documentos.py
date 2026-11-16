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
from pypdf import PdfWriter

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario
from contas.vinculos import alterar
from estabelecimentos.models import Estabelecimento

from .campo_arquivos import LIMITE_BYTES
from .documentos_arquivos import validar_documento
from .documentos_services import salvar
from .models import DocumentoEstabelecimento, EvidenciaCampo, Inspecao, RespostaCampo
from .services import atribuir, iniciar_atribuida
from .test_campo import foto


def pdf(*, cifrado=False, paginas=1, nome="alvara.pdf"):
    with PdfWriter() as escritor:
        for _ in range(paginas):
            escritor.add_blank_page(width=72, height=72)
        if cifrado:
            escritor.encrypt("senha-ficticia")
        buffer = BytesIO()
        escritor.write(buffer)
    return SimpleUploadedFile(nome, buffer.getvalue(), content_type="application/octet-stream")


def preparar_documentos():
    admin = Usuario.objects.create_user("admin-documentos", perfil=Perfil.ADMINISTRADOR)
    fiscal = Usuario.objects.create_user("fiscal-documentos", perfil=Perfil.FISCALIZACAO)
    cliente = Usuario.objects.create_user("cliente-documentos", perfil=Perfil.ESTABELECIMENTO)
    unidade = Estabelecimento.objects.create(nome="Unidade Norte")
    alterar(admin.pk, cliente.pk, versao=1, estabelecimento_id=unidade.pk)
    inspecao = atribuir(
        admin.pk, operacao=uuid4(), estabelecimento_id=unidade.pk, acao_id=None,
        responsavel_id=fiscal.pk, participantes_ids=[],
    )
    return admin, fiscal, cliente, unidade, inspecao


class DocumentosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.unidade, cls.inspecao = preparar_documentos()
        cls.colega = Usuario.objects.create_user("conta-mesma-unidade", perfil=Perfil.ESTABELECIMENTO)
        cls.outro = Usuario.objects.create_user("conta-outra-unidade", perfil=Perfil.ESTABELECIMENTO)
        cls.fiscal_fora = Usuario.objects.create_user("fiscal-fora", perfil=Perfil.FISCALIZACAO)
        outra_unidade = Estabelecimento.objects.create(nome="Unidade Sul")
        alterar(cls.admin.pk, cls.colega.pk, versao=1, estabelecimento_id=cls.unidade.pk)
        alterar(cls.admin.pk, cls.outro.pk, versao=1, estabelecimento_id=outra_unidade.pk)
        cls.outra = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=outra_unidade.pk, acao_id=None,
            responsavel_id=cls.fiscal_fora.pk, participantes_ids=[],
        )
        checklist = Checklist.objects.create(titulo="Avaliação interna reservada", criado_por=cls.admin)
        VersaoChecklist.objects.create(
            checklist=checklist, numero=1, revisao_rascunho=1, titulo=checklist.titulo,
            itens=[{"id": str(uuid4()), "enunciado": "Pergunta reservada", "opcoes": ["Sim"]}],
            publicado_por=cls.admin,
        )
        cls.checklist = checklist

    def setUp(self):
        self.http = self.navegador(self.cliente)
        resposta = self.http.get(self.url("documentos_inspecao"))
        self.assertEqual(resposta.status_code, 200)
        self.contexto = resposta.context["contexto"]

    def navegador(self, usuario):
        browser = Client(enforce_csrf_checks=True, raise_request_exception=False)
        browser.force_login(usuario)
        return browser

    def url(self, nome, *args, outra=False):
        pk = self.outra.pk if outra else self.inspecao.pk
        return reverse("inspecoes:" + nome, args=[pk, *args])

    def enviar(self, *, navegador=None, outra=False, **dados):
        navegador = navegador or self.http
        default = {"operacao_id": uuid4(), "descricao": "Licença de demonstração", "arquivo": pdf()}
        return navegador.post(self.url("documentos_enviar", outra=outra), {
            "csrfmiddlewaretoken": navegador.cookies[settings.CSRF_COOKIE_NAME].value,
            **default, **dados,
        }, headers={"X-Contexto-Campo": self.contexto})

    def test_janela_da_atribuicao_ao_andamento_sem_expor_checklist(self):
        lista = self.http.get(reverse("inspecoes:documentos"))
        self.assertContains(lista, "Unidade Norte")
        self.assertNotContains(lista, "Unidade Sul")
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.ATRIBUIDA)
        envio = self.enviar(autor=self.outro.pk, estabelecimento=self.outra.estabelecimento_id)
        self.assertEqual(envio.status_code, 200)
        doc = DocumentoEstabelecimento.objects.get()
        self.assertEqual(doc.autor, self.cliente)
        self.assertEqual(doc.inspecao.estabelecimento, self.unidade)
        self.assertTrue(envio.json()["confirmado_em"])
        iniciar_atribuida(self.fiscal.pk, self.inspecao.pk, checklist_id=self.checklist.pk)
        self.inspecao.refresh_from_db()
        versao = self.inspecao.versao_checklist_id
        self.assertEqual(self.enviar(arquivo=foto(formato="JPEG")).status_code, 200)
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.versao_checklist_id, versao)
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.EM_ANDAMENTO)
        self.assertEqual(list(self.inspecao.historico.values_list("ato", flat=True)), ["atribuicao", "inicio"])
        self.assertFalse(RespostaCampo.objects.exists())
        self.assertFalse(EvidenciaCampo.objects.exists())
        self.assertNotContains(self.http.get(self.url("documentos_inspecao")), "Pergunta reservada")
        self.assertEqual(self.http.get(self.url("detalhe")).status_code, 403)

    def test_compartilha_dentro_da_unidade_e_so_equipe_fiscal_consulta(self):
        url = self.enviar().json()["url"]
        for autorizado in (self.colega, self.fiscal):
            with self.subTest(autorizado=autorizado.username):
                navegador = self.navegador(autorizado)
                self.assertContains(navegador.get(self.url("documentos_inspecao")), "alvara.pdf")
                download = navegador.get(url)
                self.assertEqual(download.status_code, 200)
                self.assertEqual(download["Content-Type"], "application/pdf")
                self.assertIn("attachment", download["Content-Disposition"])
                self.assertEqual(download["X-Content-Type-Options"], "nosniff")
                self.assertIn("no-store", download["Cache-Control"])
                self.assertEqual(b"".join(download.streaming_content), bytes(DocumentoEstabelecimento.objects.get().conteudo))
        for terceiro in (self.outro, self.fiscal_fora):
            navegador = self.navegador(terceiro)
            self.assertEqual(navegador.get(url).status_code, 404)
            self.assertEqual(navegador.get(self.url("documentos_inspecao")).status_code, 404)

    def test_bloqueia_referencia_alheia_e_revalida_vinculo_na_mesma_sessao(self):
        self.assertEqual(self.enviar(outra=True).status_code, 404)
        confirmacao = self.enviar()
        sessao = self.http.session.session_key
        self.cliente.refresh_from_db()
        alterar(self.admin.pk, self.cliente.pk, versao=self.cliente.versao_gestao, estabelecimento_id=None)
        self.assertEqual(self.http.session.session_key, sessao)
        self.assertEqual(self.http.get(confirmacao.json()["url"]).status_code, 404)
        self.assertEqual(self.enviar().status_code, 404)
        sonda = self.http.get(self.url("documentos_conexao"), headers={"X-Contexto-Campo": self.contexto})
        self.assertEqual(sonda.status_code, 404)
        self.assertEqual(DocumentoEstabelecimento.objects.count(), 1)

    def test_arquivo_invalido_cifrado_grande_demais_e_png_valido(self):
        for invalido in (
            SimpleUploadedFile("falso.pdf", b"%PDF-1.7\ninvalido"),
            pdf(cifrado=True),
            pdf(paginas=51),
            SimpleUploadedFile("grande.png", b"x" * (LIMITE_BYTES + 1)),
        ):
            with self.subTest(arquivo=invalido.name):
                self.assertEqual(self.enviar(arquivo=invalido).status_code, 400)
        self.assertFalse(DocumentoEstabelecimento.objects.exists())
        self.assertEqual(self.enviar(arquivo=foto()).status_code, 200)
        self.assertEqual(DocumentoEstabelecimento.objects.get().mime, "image/png")

    def test_repeticao_recupera_recibo_e_mesma_chave_divergente_conflita(self):
        chave = uuid4()
        primeira = self.enviar(operacao_id=chave).json()
        self.assertEqual(self.enviar(operacao_id=chave).json(), primeira)
        self.assertEqual(self.enviar(operacao_id=chave, descricao="Diferente").status_code, 409)
        self.assertEqual(self.enviar(operacao_id=chave, arquivo=pdf(paginas=2)).status_code, 409)
        self.assertEqual(DocumentoEstabelecimento.objects.count(), 1)

    def test_janela_fechada_preserva_consulta_e_recibo_anterior(self):
        chave = uuid4()
        confirmacao = self.enviar(operacao_id=chave).json()
        with patch("inspecoes.documentos_services.JANELA_ENVIO", ()):
            self.assertNotContains(self.http.get(self.url("documentos_inspecao")), "Enviar documento")
            self.assertEqual(self.enviar().status_code, 400)
            self.assertEqual(self.enviar(operacao_id=chave).json(), confirmacao)
        self.assertEqual(DocumentoEstabelecimento.objects.count(), 1)

    def test_sessao_trocada_e_csrf_ausente_bloqueiam_envio(self):
        self.assertEqual(self.http.post(self.url("documentos_enviar"), {"arquivo": pdf()}).status_code, 403)
        self.http.logout()
        self.http.force_login(self.colega)
        self.http.get(self.url("documentos_inspecao"))
        self.assertEqual(self.enviar().status_code, 401)
        self.assertFalse(DocumentoEstabelecimento.objects.exists())

    def test_falha_de_gravacao_nao_produz_confirmacao(self):
        with patch("inspecoes.documentos_services.DocumentoEstabelecimento.objects.create", side_effect=OperationalError):
            self.assertEqual(self.enviar().status_code, 503)
        self.assertFalse(DocumentoEstabelecimento.objects.exists())


class ReenvioDocumentoTests(TransactionTestCase):
    def test_envios_concorrentes_confirmam_um_unico_documento(self):
        _, _, cliente, _, inspecao = preparar_documentos()
        meta, conteudo = validar_documento(pdf())
        chave = uuid4()
        juntos = Barrier(2, timeout=8)

        def enviar():
            try:
                juntos.wait()
                return salvar(
                    cliente.pk, inspecao.pk, operacao_id=chave, descricao="",
                    metadados=meta, conteudo=conteudo,
                ).pk
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [executor.submit(enviar) for _ in range(2)]
            ids = [tarefa.result(timeout=10) for tarefa in tarefas]
        self.assertEqual(ids, [DocumentoEstabelecimento.objects.get().pk] * 2)
