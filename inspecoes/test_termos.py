from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from threading import Barrier
from unittest.mock import patch
from uuid import UUID, uuid4

from django.conf import settings
from django.db import IntegrityError, OperationalError, connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils.crypto import salted_hmac
from pypdf import PdfReader

from contas.models import Perfil, Usuario
from contas.vinculos import alterar
from estabelecimentos.models import Estabelecimento

from .campo_services import salvar_resposta
from .conclusao_services import concluir, consultar
from .models import HistoricoInspecao, Inspecao, LiberacaoTermo, TermoInspecao
from .services import alterar_supervisao, atribuir
from .termo_services import TermoDesatualizado, emitir, liberar
from .test_conclusao import preparar_conclusao


def confirmar_resultado(fiscal, inspecao, itens):
    for item, opcao, descricao, anterior in [
        (itens[0], "Sim", "Etiqueta parcial & <frente>", ""),
        (itens[1], "Não", "Equipamento com resíduos na superfície.", "Descrição anterior substituída"),
        (itens[2], "Não se aplica", "", ""),
    ]:
        dados = {
            "opcao": opcao, "observacao": "OBSERVAÇÃO INTERNA RESERVADA",
            "descricao_irregularidade": descricao,
        }
        if anterior:
            salvar_resposta(
                fiscal.pk, inspecao.pk, UUID(item["id"]), operacao_id=uuid4(), revisao=0,
                **{**dados, "descricao_irregularidade": anterior},
            )
        salvar_resposta(
            fiscal.pk, inspecao.pk, UUID(item["id"]), operacao_id=uuid4(), revisao=int(bool(anterior)), **dados,
        )
    return concluir(
        fiscal.pk, inspecao.pk, operacao_id=uuid4(),
        revisao_base=consultar(fiscal.pk, inspecao.pk)["revisao_base"],
    )


def designar_supervisor(admin, inspecao):
    supervisor = Usuario.objects.create_user("supervisor-termos", perfil=Perfil.FISCALIZACAO)
    atribuir(
        admin.pk, operacao=uuid4(), estabelecimento_id=inspecao.estabelecimento_id,
        acao_id=inspecao.acao_id, responsavel_id=supervisor.pk, participantes_ids=[],
    )
    alterar_supervisao(admin.pk, inspecao.acao_id, revisao=1, fiscais_ids=[supervisor.pk])
    return supervisor


class TermosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.inspecao, _, cls.itens = preparar_conclusao()

    def sessao(self, usuario):
        http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        http.force_login(usuario)
        http.get(reverse("contas:acesso"))
        http.contexto = salted_hmac(
            "inspecoes.campo", f"{usuario.pk}:{http.session.session_key}", algorithm="sha256",
        ).hexdigest()
        return http

    def url(self, nome, *args):
        return reverse("inspecoes:" + nome, args=args)

    def post(self, http, nome, *args, chave=None):
        return http.post(self.url(nome, self.inspecao.pk, *args), {
            "operacao_id": chave or uuid4(), "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
        }, headers={"X-Contexto-Campo": http.contexto})

    def preparar_termo(self):
        confirmar_resultado(self.fiscal, self.inspecao, self.itens)
        return emitir(self.fiscal.pk, self.inspecao.pk, operacao_id=uuid4())

    def test_emissao_requer_conclusao_e_preserva_pdf_por_revisao(self):
        fiscal = self.sessao(self.fiscal)
        self.assertEqual(self.post(fiscal, "termo_emitir").status_code, 409)
        self.assertFalse(TermoInspecao.objects.exists())
        resultado = confirmar_resultado(self.fiscal, self.inspecao, self.itens)
        chave = uuid4()
        recebido = self.post(fiscal, "termo_emitir", chave=chave)
        self.assertEqual(recebido.status_code, 200)
        self.assertEqual(self.post(fiscal, "termo_emitir", chave=chave).json(), recebido.json())
        self.assertEqual(self.post(fiscal, "termo_emitir").status_code, 409)
        termo = TermoInspecao.objects.get()
        self.assertEqual(termo.resultado, resultado)
        self.assertEqual(termo.versao, 1)
        self.assertFalse(LiberacaoTermo.objects.exists())
        download = fiscal.get(self.url("termo_pdf", self.inspecao.pk, termo.pk))
        self.assertEqual(download.status_code, 200)
        self.assertEqual(download["Content-Type"], "application/pdf")
        self.assertIn("no-store", download["Cache-Control"])
        self.assertIn(termo.codigo, download["Content-Disposition"])
        dados = b"".join(download.streaming_content)
        self.assertEqual(dados, termo.conteudo)
        texto = "\n".join(pagina.extract_text() for pagina in PdfReader(BytesIO(dados)).pages)
        for trecho in ("Demonstração", "Versão 1", "80,00%", "Higiene", "Não conforme", termo.codigo,
                       "Equipamento com resíduos na superfície.", "Etiqueta parcial & <frente>"):
            self.assertIn(trecho, texto)
        for trecho in ("OBSERVAÇÃO INTERNA RESERVADA", "Descrição anterior substituída", "Observação opcional"):
            self.assertNotIn(trecho, texto)

    def test_portal_exige_liberacao_e_vinculo_atual_inclusive_no_pdf(self):
        termo = self.preparar_termo()
        cliente = self.sessao(self.cliente)
        lista = self.url("resultados_liberados")
        detalhe = self.url("resultado_liberado", termo.pk)
        url_pdf = self.url("resultado_pdf", termo.pk)
        self.assertContains(cliente.get(lista), "Nenhum resultado liberado")
        for url in (detalhe, url_pdf):
            self.assertEqual(cliente.get(url).status_code, 404)
            self.assertEqual(Client().get(url).status_code, 302)

        admin = self.sessao(self.admin)
        chave = uuid4()
        recibo = self.post(admin, "termo_liberar", termo.pk, chave=chave)
        self.assertEqual(recibo.status_code, 200)
        self.assertEqual(self.post(admin, "termo_liberar", termo.pk, chave=chave).json(), recibo.json())
        self.assertEqual(self.post(admin, "termo_liberar", termo.pk).status_code, 409)

        mesma = Usuario.objects.create_user("mesma-unidade", perfil=Perfil.ESTABELECIMENTO)
        alterar(self.admin.pk, mesma.pk, versao=1, estabelecimento_id=self.inspecao.estabelecimento_id)
        self.assertContains(self.sessao(mesma).get(detalhe), termo.codigo)
        outra = Usuario.objects.create_user("conta-de-outra-unidade", perfil=Perfil.ESTABELECIMENTO)
        unidade = Estabelecimento.objects.create(nome="Unidade distinta")
        alterar(self.admin.pk, outra.pk, versao=1, estabelecimento_id=unidade.pk)
        fora = self.sessao(outra)
        self.assertContains(fora.get(lista), "Nenhum resultado liberado")
        self.assertEqual(fora.get(detalhe).status_code, 404)
        self.assertEqual(fora.get(url_pdf).status_code, 404)
        self.assertContains(cliente.get(detalhe), "Satisfatória")
        self.assertNotContains(cliente.get(detalhe), "OBSERVAÇÃO INTERNA RESERVADA")
        download = cliente.get(url_pdf)
        self.assertEqual(download.status_code, 200)
        self.assertEqual(b"".join(download.streaming_content), termo.conteudo)
        self.cliente.refresh_from_db()
        alterar(self.admin.pk, self.cliente.pk, versao=self.cliente.versao_gestao, estabelecimento_id=None)
        self.assertEqual(cliente.get(detalhe).status_code, 404)
        self.assertEqual(cliente.get(url_pdf).status_code, 404)

    def test_supervisor_da_acao_libera_e_revogacao_bloqueia_na_mesma_sessao(self):
        termo = self.preparar_termo()
        fiscal = self.sessao(self.fiscal)
        self.assertEqual(self.post(fiscal, "termo_liberar", termo.pk).status_code, 403)
        supervisor = designar_supervisor(self.admin, self.inspecao)
        http = self.sessao(supervisor)
        self.assertContains(http.get(self.url("termos")), termo.codigo)
        self.assertContains(http.get(self.url("termo", self.inspecao.pk)), "Liberar ao estabelecimento")
        self.assertEqual(http.get(self.url("conclusao", self.inspecao.pk)).status_code, 404)
        self.assertEqual(self.post(http, "termo_emitir").status_code, 404)
        fora = Usuario.objects.create_user("supervisor-outra-acao", perfil=Perfil.FISCALIZACAO)
        outra = atribuir(
            self.admin.pk, operacao=uuid4(), estabelecimento_id=self.inspecao.estabelecimento_id,
            acao_id=None, responsavel_id=fora.pk, participantes_ids=[],
        )
        alterar_supervisao(self.admin.pk, outra.acao_id, revisao=1, fiscais_ids=[fora.pk])
        self.assertEqual(self.post(self.sessao(fora), "termo_liberar", termo.pk).status_code, 404)

        chave = uuid4()
        self.assertEqual(self.post(http, "termo_liberar", termo.pk, chave=chave).status_code, 200)
        liberacao = LiberacaoTermo.objects.get(termo=termo)
        self.assertEqual(liberacao.designacao.fiscal, supervisor)
        self.assertEqual(liberacao.designacao.acao_id, self.inspecao.acao_id)
        alterar_supervisao(self.admin.pk, self.inspecao.acao_id, revisao=2, fiscais_ids=[])
        self.assertEqual(self.post(http, "termo_liberar", termo.pk, chave=chave).status_code, 404)
        self.assertEqual(http.get(self.url("termo_pdf", self.inspecao.pk, termo.pk)).status_code, 404)
        auditoria = fiscal.get(self.url("auditoria", self.inspecao.pk))
        self.assertContains(auditoria, "Termo emitido")
        self.assertContains(auditoria, "Resultado e termo liberados")

    def test_falhas_revertem_operacao_e_permitem_tentar_novamente(self):
        confirmar_resultado(self.fiscal, self.inspecao, self.itens)
        admin = self.sessao(self.admin)
        with patch("inspecoes.termo_services.termo_pdf.gerar", side_effect=ValueError):
            self.assertEqual(self.post(admin, "termo_emitir").status_code, 422)
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.CONCLUIDA)
        self.assertFalse(TermoInspecao.objects.exists())
        with patch("inspecoes.termo_services.HistoricoInspecao.objects.create", side_effect=OperationalError):
            self.assertEqual(self.post(admin, "termo_emitir").status_code, 503)
        self.assertFalse(TermoInspecao.objects.exists())

        self.assertEqual(self.post(admin, "termo_emitir").status_code, 200)
        termo = TermoInspecao.objects.get()
        with patch("inspecoes.termo_services.HistoricoInspecao.objects.create", side_effect=OperationalError):
            self.assertEqual(self.post(admin, "termo_liberar", termo.pk).status_code, 503)
        self.assertFalse(LiberacaoTermo.objects.exists())
        self.assertEqual(self.post(admin, "termo_liberar", termo.pk).status_code, 200)

    def test_banco_protege_emissao_e_liberacao_e_post_exige_csrf(self):
        termo = self.preparar_termo()
        admin = self.sessao(self.admin)
        caminho = self.url("termo_liberar", self.inspecao.pk, termo.pk)
        self.assertEqual(admin.get(caminho, headers={"X-Contexto-Campo": admin.contexto}).status_code, 405)
        self.assertEqual(admin.post(caminho).status_code, 403)
        self.assertEqual(self.post(admin, "termo_liberar", termo.pk).status_code, 200)
        with self.assertRaises(IntegrityError), transaction.atomic():
            TermoInspecao.objects.filter(pk=termo.pk).update(conteudo=b"outro")
        with self.assertRaises(IntegrityError), transaction.atomic():
            LiberacaoTermo.objects.filter(termo=termo).delete()


class TermosConcorrentesTests(TransactionTestCase):
    def test_emissao_e_liberacao_concorrentes_registram_um_ato_cada(self):
        admin, fiscal, _, inspecao, _, itens = preparar_conclusao()
        confirmar_resultado(fiscal, inspecao, itens)

        def comparar(operacao, *args):
            juntos = Barrier(2, timeout=8)

            def registrar():
                try:
                    juntos.wait()
                    operacao(admin.pk, inspecao.pk, *args, operacao_id=uuid4())
                    return "confirmada"
                except TermoDesatualizado:
                    return "conflito"
                finally:
                    connections.close_all()

            with ThreadPoolExecutor(max_workers=2) as executor:
                pedidos = [executor.submit(registrar) for _ in range(2)]
                self.assertCountEqual([pedido.result(timeout=12) for pedido in pedidos], ["confirmada", "conflito"])

        comparar(emitir)
        comparar(liberar, TermoInspecao.objects.get().pk)
        for ato in (HistoricoInspecao.Ato.TERMO_EMITIDO, HistoricoInspecao.Ato.TERMO_LIBERADO):
            self.assertEqual(inspecao.historico.filter(ato=ato).count(), 1)
