from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from io import BytesIO
from threading import Barrier
from unittest.mock import patch
from uuid import UUID, uuid4

from django.conf import settings
from django.db import IntegrityError, connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils.crypto import salted_hmac
from pypdf import PdfReader

from checklists.models import VersaoChecklist
from contas.models import Perfil, Usuario

from .correcao_services import CorrecaoDesatualizada, aplicar, decidir, solicitar
from .models import DecisaoCorrecao, HistoricoInspecao, Inspecao, PedidoCorrecao, ResultadoInspecao, TermoInspecao
from .resultados import atual
from .services import alterar_supervisao
from .termo_services import emitir, liberar
from .test_conclusao import preparar_conclusao
from .test_termos import confirmar_resultado, designar_supervisor


def preparar_correcao():
    admin, fiscal, cliente, inspecao, versao, itens = preparar_conclusao()
    base = confirmar_resultado(fiscal, inspecao, itens)
    return admin, fiscal, cliente, inspecao, versao, itens, base


def propor(fiscal, inspecao, base, item, **dados):
    entrada = {
        "base_id": base.pk, "operacao_id": uuid4(), "justificativa": "Conferência autorizada",
        "opcao": "Não", "observacao": "", "descricao_irregularidade": "Descrição corrigida",
    } | dados
    return solicitar(fiscal.pk, inspecao.pk, UUID(item["id"]), **entrada)


def autorizar(admin, inspecao, pedido):
    return decidir(admin.pk, inspecao.pk, pedido.pk, aprovada=True, motivo="Aceito", operacao_id=uuid4())


class CorrecoesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.inspecao, cls.versao, cls.itens, cls.base = preparar_correcao()

    def navegador(self, usuario):
        http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        http.force_login(usuario)
        http.get(reverse("contas:acesso"))
        http.contexto = salted_hmac(
            "inspecoes.campo", f"{usuario.pk}:{http.session.session_key}", algorithm="sha256",
        ).hexdigest()
        return http

    def url(self, nome, *args):
        return reverse("inspecoes:" + nome, args=args)

    def post(self, http, nome, *args, inspecao_id=None, **dados):
        return http.post(self.url(nome, inspecao_id or self.inspecao.pk, *args), {
            "operacao_id": uuid4(), "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
            **dados,
        }, headers={"X-Contexto-Campo": http.contexto})

    def pedir(self, indice=0, **dados):
        return propor(self.fiscal, self.inspecao, self.base, self.itens[indice], **dados)

    def test_solicitacao_registra_base_conteudo_exato_e_idempotencia(self):
        http = self.navegador(self.fiscal)
        item = self.itens[0]["id"]
        self.assertContains(http.get(self.url("revisoes", self.inspecao.pk)), "Escolher item para corrigir")
        self.assertContains(http.get(self.url("correcao_item", self.inspecao.pk, item)), "Registro atual")
        chave = uuid4()
        dados = {
            "base_id": self.base.pk, "operacao_id": chave, "justificativa": "Dado conferido",
            "opcao": "Não", "observacao": "", "descricao_irregularidade": "Confirmada",
        }
        caminho = self.url("correcao_solicitar", self.inspecao.pk, item)
        self.assertEqual(http.post(caminho, dados).status_code, 403)
        self.assertEqual(self.post(http, "correcao_solicitar", item, **{**dados, "justificativa": "  "}).status_code, 400)
        resposta = self.post(http, "correcao_solicitar", item, **dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(self.post(http, "correcao_solicitar", item, **dados).json(), resposta.json())
        self.assertEqual(self.post(http, "correcao_solicitar", item, **{**dados, "opcao": "Sim"}).status_code, 409)
        pedido = PedidoCorrecao.objects.get()
        self.assertEqual(pedido.antes["opcao"], "Sim")
        self.assertEqual(pedido.proposto["opcao"], "Não")
        self.assertEqual(atual(self.inspecao), self.base)
        self.assertContains(http.get(resposta.json()["url"]), "Mudança solicitada")
        with self.assertRaises(IntegrityError), transaction.atomic():
            PedidoCorrecao.objects.filter(pk=pedido.pk).update(justificativa="Outra")
        cliente = self.navegador(self.cliente)
        self.assertEqual(cliente.get(resposta.json()["url"]).status_code, 403)

    def test_autoridade_contextual_impede_autoaprovacao_e_respeita_revogacao(self):
        supervisor = designar_supervisor(self.admin, self.inspecao)
        alterar_supervisao(self.admin.pk, self.inspecao.acao_id, revisao=2,
                           fiscais_ids=[supervisor.pk, self.fiscal.pk])
        pedido = self.pedir()
        fiscal, admin, superior = map(self.navegador, (self.fiscal, self.admin, supervisor))
        dados = {"aprovada": "aprovar", "motivo": "Conferido"}
        self.assertEqual(self.post(fiscal, "correcao_decidir", pedido.pk, **dados).status_code, 403)
        self.assertEqual(self.post(admin, "correcao_decidir", pedido.pk, **dados).status_code, 403)
        outro = Usuario.objects.create_user("fiscal-fora-correcao", perfil=Perfil.FISCALIZACAO)
        self.assertEqual(self.post(self.navegador(outro), "correcao_decidir", pedido.pk, **dados).status_code, 404)
        self.assertContains(superior.get(self.url("correcoes")), f"Pedido #{pedido.pk}")
        self.assertEqual(self.post(superior, "correcao_decidir", pedido.pk, inspecao_id=self.inspecao.pk + 200, **dados).status_code, 404)
        alterar_supervisao(self.admin.pk, self.inspecao.acao_id, revisao=3, fiscais_ids=[self.fiscal.pk])
        self.assertEqual(self.post(superior, "correcao_decidir", pedido.pk, **dados).status_code, 404)
        self.assertEqual(self.post(admin, "correcao_decidir", pedido.pk, **dados).status_code, 200)
        self.assertEqual(atual(self.inspecao), self.base)
        self.assertEqual(self.post(fiscal, "correcao_aplicar", pedido.pk).status_code, 200)

    def test_pendente_rejeitada_ou_sem_poder_nao_aplica(self):
        pedido = self.pedir()
        fiscal = self.navegador(self.fiscal)
        self.assertEqual(self.post(fiscal, "correcao_aplicar", pedido.pk).status_code, 409)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ResultadoInspecao.objects.create(
                inspecao=self.inspecao, revisao=2, correcao=pedido, aplicado_em=self.base.concluido_em,
                aplicado_por=self.fiscal, versao_checklist=self.versao, regra_pontuacao=self.base.regra_pontuacao,
                pontuacao=self.base.pontuacao, classificacao=self.base.classificacao,
                respostas_utilizadas=self.base.respostas_utilizadas, revisao_base=self.base.revisao_base,
                concluido_por=self.fiscal, operacao_id=uuid4(),
            )
        admin = self.navegador(self.admin)
        self.assertEqual(self.post(
            admin, "correcao_decidir", pedido.pk, aprovada="rejeitar", motivo="Base divergente",
        ).status_code, 200)
        self.assertEqual(self.post(admin, "correcao_aplicar", pedido.pk).status_code, 409)
        supervisor = designar_supervisor(self.admin, self.inspecao)
        outro = self.pedir()
        decisao = decidir(supervisor.pk, self.inspecao.pk, outro.pk, aprovada=True, motivo="Aceito", operacao_id=uuid4())
        self.assertEqual(decisao.designacao.fiscal, supervisor)
        self.assertEqual(self.post(self.navegador(supervisor), "correcao_aplicar", outro.pk).status_code, 403)
        self.assertEqual(atual(self.inspecao), self.base)
        with self.assertRaises(IntegrityError), transaction.atomic():
            DecisaoCorrecao.objects.filter(pk=decisao.pk).delete()

    def test_recalculo_pela_regra_original_e_base_concorrente(self):
        anterior = self.pedir(3)
        concorrente = self.pedir(1, opcao="Sim")
        for pedido in (anterior, concorrente):
            autorizar(self.admin, self.inspecao, pedido)
        VersaoChecklist.objects.create(
            checklist=self.versao.checklist, numero=2, revisao_rascunho=2, titulo="Publicação posterior",
            itens=[{**self.itens[0], "peso": "400"}, *self.itens[1:]], publicado_por=self.admin,
        )
        chave = uuid4()
        novo = aplicar(self.admin.pk, self.inspecao.pk, anterior.pk, operacao_id=chave)
        self.assertEqual(aplicar(self.admin.pk, self.inspecao.pk, anterior.pk, operacao_id=chave), novo)
        self.assertEqual(novo.revisao, 2)
        self.assertEqual(novo.versao_checklist, self.versao)
        self.assertEqual(novo.pontuacao, Decimal("7.27"))
        self.assertEqual(novo.classificacao, "insatisfatoria")
        self.assertEqual(novo.concluido_em, self.base.concluido_em)
        self.assertEqual(novo.concluido_por, self.base.concluido_por)
        self.assertEqual(self.base.pontuacao, Decimal("80.00"))
        self.assertFalse(self.inspecao.respostas_campo.filter(item_id=self.itens[3]["id"]).exists())
        with self.assertRaises(CorrecaoDesatualizada):
            aplicar(self.admin.pk, self.inspecao.pk, concorrente.pk, operacao_id=uuid4())
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.CONCLUIDA)
        termo = emitir(self.fiscal.pk, self.inspecao.pk, operacao_id=uuid4())
        self.assertEqual(termo.resultado, novo)
        self.assertIsNone(termo.anterior)
        atual_page = self.navegador(self.fiscal).get(self.url("conclusao", self.inspecao.pk))
        self.assertContains(atual_page, "7,27%")

    def test_retificador_preserva_original_e_exige_liberacao_por_versao(self):
        chave = uuid4()
        original = emitir(self.fiscal.pk, self.inspecao.pk, operacao_id=chave)
        liberar(self.admin.pk, self.inspecao.pk, original.pk, operacao_id=uuid4())
        pedido = self.pedir()
        autorizar(self.admin, self.inspecao, pedido)
        novo = aplicar(self.fiscal.pk, self.inspecao.pk, pedido.pk, operacao_id=uuid4())
        novo_termo = TermoInspecao.objects.get(resultado=novo)
        self.assertEqual(novo_termo.versao, 2)
        self.assertEqual(novo_termo.anterior, original)
        self.assertEqual(emitir(self.fiscal.pk, self.inspecao.pk, operacao_id=chave), original)
        texto = " ".join(p.extract_text() for p in PdfReader(BytesIO(novo_termo.conteudo)).pages)
        self.assertIn("Termo retificador", texto)
        self.assertIn(original.codigo, texto)
        self.assertIn("Descrição corrigida", texto)
        self.assertNotIn(pedido.justificativa, texto)

        cliente = self.navegador(self.cliente)
        antiga = self.url("resultado_pdf", original.pk)
        recente = self.url("resultado_pdf", novo_termo.pk)
        self.assertEqual(cliente.get(recente).status_code, 404)
        self.assertEqual(b"".join(cliente.get(antiga).streaming_content), original.conteudo)
        liberar(self.admin.pk, self.inspecao.pk, novo_termo.pk, operacao_id=uuid4())
        self.assertEqual(b"".join(cliente.get(recente).streaming_content), novo_termo.conteudo)
        self.assertEqual(b"".join(cliente.get(antiga).streaming_content), original.conteudo)
        self.assertContains(cliente.get(self.url("resultado_liberado", original.pk)), "Versão anterior")
        self.assertContains(cliente.get(self.url("resultado_liberado", novo_termo.pk)), "Versão mais recente liberada")
        self.assertContains(self.navegador(self.fiscal).get(
            self.url("termo_versao", self.inspecao.pk, original.pk),
        ), original.codigo)

    def test_observacao_interna_nao_gera_novo_pdf_e_revisoes_sucessivas(self):
        termo = emitir(self.admin.pk, self.inspecao.pk, operacao_id=uuid4())
        pedido = self.pedir(0, opcao="Sim", observacao="Informação interna revisada",
                           descricao_irregularidade="Etiqueta parcial & <frente>")
        autorizar(self.admin, self.inspecao, pedido)
        segundo = aplicar(self.admin.pk, self.inspecao.pk, pedido.pk, operacao_id=uuid4())
        self.assertEqual(TermoInspecao.objects.count(), 1)
        self.assertEqual(segundo.pontuacao, self.base.pontuacao)
        proximo = propor(self.fiscal, self.inspecao, segundo, self.itens[0], opcao="Sim")
        autorizar(self.admin, self.inspecao, proximo)
        terceiro = aplicar(self.admin.pk, self.inspecao.pk, proximo.pk, operacao_id=uuid4())
        self.assertEqual(proximo.antes["observacao"], "Informação interna revisada")
        self.assertEqual(terceiro.revisao, 3)
        self.assertEqual(TermoInspecao.objects.get(resultado=terceiro).anterior, termo)

    def test_falha_ao_retificar_preserva_pedido_aprovado_e_resultado(self):
        emitir(self.fiscal.pk, self.inspecao.pk, operacao_id=uuid4())
        pedido = self.pedir()
        autorizar(self.admin, self.inspecao, pedido)
        admin = self.navegador(self.admin)
        with patch("inspecoes.termo_services.termo_pdf.gerar", side_effect=ValueError):
            self.assertEqual(self.post(admin, "correcao_aplicar", pedido.pk).status_code, 422)
        self.assertEqual(atual(self.inspecao), self.base)
        self.assertFalse(self.inspecao.historico.filter(ato=HistoricoInspecao.Ato.CORRECAO_APLICADA).exists())
        self.assertEqual(TermoInspecao.objects.count(), 1)
        self.assertEqual(self.post(admin, "correcao_aplicar", pedido.pk).status_code, 200)
        self.assertEqual(TermoInspecao.objects.count(), 2)


class CorrecoesConcorrentesTests(TransactionTestCase):
    def test_dois_pedidos_aprovados_sobre_mesma_base_so_aplicam_um(self):
        admin, fiscal, _, inspecao, _, itens, base = preparar_correcao()
        pedidos = [propor(fiscal, inspecao, base, item) for item in (itens[0], itens[3])]
        for pedido in pedidos:
            autorizar(admin, inspecao, pedido)
        juntos = Barrier(2, timeout=8)

        def executar(pedido):
            try:
                juntos.wait()
                aplicar(admin.pk, inspecao.pk, pedido.pk, operacao_id=uuid4())
                return "confirmada"
            except CorrecaoDesatualizada:
                return "conflito"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [executor.submit(executar, pedido) for pedido in pedidos]
            self.assertCountEqual([tarefa.result(timeout=12) for tarefa in tarefas], ["confirmada", "conflito"])
        self.assertEqual(inspecao.resultados.count(), 2)
        self.assertEqual(inspecao.historico.filter(ato=HistoricoInspecao.Ato.CORRECAO_APLICADA).count(), 1)
