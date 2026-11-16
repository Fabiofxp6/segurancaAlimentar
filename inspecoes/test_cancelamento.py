from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings
from django.db import IntegrityError, OperationalError, connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario

from .cancelamento_services import CancelamentoDesatualizado, decidir, solicitar
from .models import DocumentoEstabelecimento, EvidenciaCampo, HistoricoInspecao, Inspecao, PedidoCancelamento, RespostaCampo
from .services import alterar_supervisao, atribuir, iniciar_atribuida
from .test_campo import foto
from .test_documentos import pdf, preparar_documentos


def preparar_cancelamento():
    admin, fiscal, cliente, unidade, inspecao = preparar_documentos()
    checklist = Checklist.objects.create(titulo="Versão de demonstração", criado_por=admin)
    item = uuid4()
    VersaoChecklist.objects.create(
        checklist=checklist, numero=1, revisao_rascunho=1, titulo=checklist.titulo,
        itens=[{"id": str(item), "enunciado": "Enunciado fiscal", "ordem": 1, "opcoes": ["Sim", "Não"]}],
        publicado_por=admin,
    )
    iniciar_atribuida(fiscal.pk, inspecao.pk, checklist_id=checklist.pk)
    inspecao.refresh_from_db()
    return admin, fiscal, cliente, unidade, inspecao, item


class CancelamentoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, unidade, cls.inspecao, cls.item = preparar_cancelamento()
        cls.supervisor = Usuario.objects.create_user("supervisor-acao", perfil=Perfil.FISCALIZACAO)
        cls.fora = Usuario.objects.create_user("fiscal-outra-acao", perfil=Perfil.FISCALIZACAO)
        cls.agrupada = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=unidade.pk, acao_id=cls.inspecao.acao_id,
            responsavel_id=cls.supervisor.pk, participantes_ids=[],
        )
        cls.outra = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=unidade.pk, acao_id=None,
            responsavel_id=cls.fora.pk, participantes_ids=[],
        )

    def sessao(self, usuario, pagina="cancelamento", *args):
        http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        http.force_login(usuario)
        http.get(reverse("contas:acesso"))
        resposta = http.get(self.url(pagina, *args))
        if resposta.status_code == 200:
            http.contexto = resposta.context["contexto"]
        return http

    def url(self, nome, *args, pk=None):
        return reverse(f"inspecoes:{nome}", args=[pk or self.inspecao.pk, *args])

    def post(self, http, nome, *args, pk=None, **dados):
        return http.post(self.url(nome, *args, pk=pk), {
            "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
            "operacao_id": uuid4(), **dados,
        }, headers={"X-Contexto-Campo": http.contexto})

    def pedido(self):
        return solicitar(
            self.fiscal.pk, self.inspecao.pk, justificativa="Unidade indisponível", operacao_id=uuid4(),
        )

    def designar(self, fiscais):
        self.inspecao.acao.refresh_from_db()
        alterar_supervisao(
            self.admin.pk, self.inspecao.acao_id, revisao=self.inspecao.acao.revisao_supervisao,
            fiscais_ids=[fiscal.pk for fiscal in fiscais],
        )

    def decisao(self, http, pedido, decisao="aprovado", **dados):
        return self.post(http, "cancelamento_decidir", pedido.pk, decisao=decisao, motivo_decisao="Conferido", **dados)

    def test_solicitacao_exige_justificativa_csrf_e_inspecao_em_andamento(self):
        http = self.sessao(self.fiscal)
        self.assertEqual(self.post(http, "cancelamento_solicitar", justificativa="   ").status_code, 400)
        self.assertEqual(http.post(self.url("cancelamento_solicitar"), {"justificativa": "Teste"}).status_code, 403)
        primeiro = self.post(http, "cancelamento_solicitar", justificativa="Unidade fechada")
        self.assertEqual(primeiro.status_code, 200)
        self.assertTrue(primeiro.json()["confirmado_em"])
        pedido = PedidoCancelamento.objects.get()
        self.assertEqual(pedido.solicitante, self.fiscal)
        self.assertEqual(pedido.situacao, PedidoCancelamento.Situacao.PENDENTE)
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.EM_ANDAMENTO)
        self.assertEqual(self.post(http, "cancelamento_solicitar", justificativa="Outro").status_code, 409)

        sup = self.sessao(self.supervisor)
        resposta = sup.get(self.url("cancelamento", pk=self.agrupada.pk))
        sup.contexto = resposta.context["contexto"]
        self.assertEqual(self.post(
            sup, "cancelamento_solicitar", pk=self.agrupada.pk, justificativa="Ainda atribuída",
        ).status_code, 409)

    def test_solicitacao_repetida_recupera_recibo_e_rejeita_texto_diferente(self):
        http = self.sessao(self.fiscal)
        chave = uuid4()
        dados = {"justificativa": "Justificativa original", "operacao_id": chave}
        primeira = self.post(http, "cancelamento_solicitar", **dados)
        self.assertEqual(self.post(http, "cancelamento_solicitar", **dados).json(), primeira.json())
        self.assertEqual(self.post(
            http, "cancelamento_solicitar", operacao_id=chave, justificativa="Alterada",
        ).status_code, 409)
        self.assertEqual(PedidoCancelamento.objects.count(), 1)

    def test_supervisor_da_acao_decide_e_admin_so_com_ausencia(self):
        self.designar([self.fiscal, self.supervisor])
        pedido = self.pedido()
        self.assertEqual(self.decisao(self.sessao(self.admin), pedido).status_code, 403)
        self.assertEqual(self.decisao(self.sessao(self.fiscal), pedido).status_code, 403)
        sup = self.sessao(self.supervisor)
        self.assertContains(sup.get(reverse("inspecoes:cancelamentos")), f"Pedido #{pedido.pk}")
        self.assertEqual(sup.get(self.url("detalhe")).status_code, 404)
        confirmacao = self.decisao(sup, pedido)
        self.assertEqual(confirmacao.status_code, 200)
        pedido.refresh_from_db()
        self.assertEqual(pedido.decidido_por, self.supervisor)
        self.assertEqual(pedido.designacao.fiscal, self.supervisor)
        self.assertEqual(pedido.situacao, PedidoCancelamento.Situacao.EFETIVADO)

    def test_supervisor_de_outra_acao_e_intercambio_de_pedido_recusados(self):
        alterar_supervisao(self.admin.pk, self.outra.acao_id, revisao=1, fiscais_ids=[self.fora.pk])
        pedido = self.pedido()
        fora = self.sessao(self.fora)
        resposta = fora.get(self.url("cancelamento", pk=self.outra.pk))
        fora.contexto = resposta.context["contexto"]
        self.assertEqual(self.decisao(fora, pedido).status_code, 404)
        self.assertEqual(self.post(
            self.sessao(self.admin), "cancelamento_decidir", pedido.pk, pk=self.outra.pk,
            decisao="aprovado", motivo_decisao="Forjado",
        ).status_code, 404)
        pedido.refresh_from_db()
        self.assertEqual(pedido.situacao, PedidoCancelamento.Situacao.PENDENTE)

    def test_revogacao_na_sessao_remove_supervisor_e_habilita_admin(self):
        self.designar([self.fiscal, self.supervisor])
        pedido = self.pedido()
        sup = self.sessao(self.supervisor)
        chave = sup.session.session_key
        self.designar([self.fiscal])
        self.assertEqual(sup.session.session_key, chave)
        self.assertEqual(self.decisao(sup, pedido).status_code, 404)
        self.assertEqual(self.decisao(self.sessao(self.admin), pedido).status_code, 200)
        pedido.refresh_from_db()
        self.assertIsNone(pedido.designacao)
        self.assertEqual(pedido.decidido_por, self.admin)

    def test_pendente_bloqueia_abas_ja_abertas_e_rejeicao_libera(self):
        fiscal = self.sessao(self.fiscal, "campo_item", self.item)
        cliente = self.sessao(self.cliente, "documentos_inspecao")
        chave = uuid4()
        dados = {"opcao": "Sim", "revisao": 0, "operacao_id": chave}
        confirmado = self.post(fiscal, "campo_responder", self.item, **dados).json()
        pedido = self.pedido()
        self.assertEqual(self.post(fiscal, "campo_responder", self.item, **dados).json(), confirmado)
        self.assertEqual(self.post(fiscal, "campo_responder", self.item, revisao=1, opcao="Não").status_code, 409)
        self.assertEqual(self.post(
            fiscal, "campo_anexar", self.item, revisao=1, vinculo="item", arquivo=foto(),
        ).status_code, 409)
        self.assertEqual(self.post(cliente, "documentos_enviar", arquivo=pdf()).status_code, 409)
        self.assertNotContains(fiscal.get(self.url("campo_item", self.item)), "Salvar resposta")
        self.assertEqual(self.decisao(self.sessao(self.admin), pedido, "rejeitado").status_code, 200)
        self.assertEqual(self.post(fiscal, "campo_responder", self.item, revisao=1, opcao="Não").status_code, 200)
        self.assertEqual(self.post(cliente, "documentos_enviar", arquivo=pdf()).status_code, 200)
        self.assertNotEqual(self.pedido().pk, pedido.pk)

    def test_aprovacao_automatica_preserva_materiais_e_recibo_e_protege_historico(self):
        fiscal = self.sessao(self.fiscal, "campo_item", self.item)
        cliente = self.sessao(self.cliente, "documentos_inspecao")
        self.post(fiscal, "campo_responder", self.item, revisao=0, opcao="Sim")
        evidencia = self.post(fiscal, "campo_anexar", self.item, revisao=1, vinculo="item", arquivo=foto()).json()["url"]
        documento = self.post(cliente, "documentos_enviar", arquivo=pdf()).json()["url"]
        pedido = self.pedido()
        admin = self.sessao(self.admin)
        chave = uuid4()
        confirmacao = self.decisao(admin, pedido, operacao_id=chave)
        self.assertEqual(confirmacao.status_code, 200)
        self.assertEqual(self.decisao(admin, pedido, operacao_id=chave).json(), confirmacao.json())
        self.assertEqual(self.decisao(admin, pedido, "rejeitado", operacao_id=chave).status_code, 409)
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.CANCELADA)
        self.assertIsNotNone(self.inspecao.cancelada_em)
        self.assertEqual((RespostaCampo.objects.count(), EvidenciaCampo.objects.count(), DocumentoEstabelecimento.objects.count()), (1, 1, 1))
        self.assertEqual(fiscal.get(evidencia).status_code, 200)
        self.assertEqual(cliente.get(documento).status_code, 200)
        self.assertEqual(self.post(fiscal, "campo_responder", self.item, revisao=1, opcao="Não").status_code, 409)
        self.assertEqual(self.post(cliente, "documentos_enviar", arquivo=pdf()).status_code, 400)

        trilha = fiscal.get(self.url("auditoria"))
        for texto in ("Solicitação de cancelamento", "Decisão de cancelamento", "Cancelamento efetivado",
                      "Resposta confirmada", "Evidência confirmada", "Documento recebido"):
            self.assertContains(trilha, texto)
        self.assertEqual(cliente.get(self.url("auditoria")).status_code, 403)
        self.assertEqual(fiscal.post(self.url("auditoria"), {
            "csrfmiddlewaretoken": fiscal.cookies[settings.CSRF_COOKIE_NAME].value,
        }).status_code, 405)
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.inspecao.historico.filter(ato=HistoricoInspecao.Ato.CANCELAMENTO).update(dados={})
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.inspecao.historico.filter(ato=HistoricoInspecao.Ato.CANCELAMENTO).delete()
        with self.assertRaises(IntegrityError), transaction.atomic():
            PedidoCancelamento.objects.filter(pk=pedido.pk).update(justificativa="Alterada")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Inspecao.objects.filter(pk=self.inspecao.pk).update(estado=Inspecao.Estado.EM_ANDAMENTO, cancelada_em=None)

    def test_estado_cancelada_exige_efetivacao_e_falha_reverte_decisao(self):
        pedido = self.pedido()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Inspecao.objects.filter(pk=self.inspecao.pk).update(
                estado=Inspecao.Estado.CANCELADA, cancelada_em=timezone.now(),
            )
        admin = self.sessao(self.admin)
        with patch("inspecoes.cancelamento_services._efetivar", side_effect=OperationalError):
            self.assertEqual(self.decisao(admin, pedido).status_code, 503)
        pedido.refresh_from_db()
        self.inspecao.refresh_from_db()
        self.assertEqual(pedido.situacao, PedidoCancelamento.Situacao.PENDENTE)
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.EM_ANDAMENTO)
        self.assertFalse(self.inspecao.historico.filter(ato=HistoricoInspecao.Ato.DECISAO_CANCELAR).exists())


class CancelamentoConcorrenteTests(TransactionTestCase):
    def test_decisoes_concorrentes_produzem_uma_efetivacao(self):
        admin, fiscal, _, _, inspecao, _ = preparar_cancelamento()
        pedido = solicitar(fiscal.pk, inspecao.pk, justificativa="Motivo", operacao_id=uuid4())
        juntos = Barrier(2, timeout=8)

        def aprovar():
            try:
                juntos.wait()
                decidir(
                    admin.pk, inspecao.pk, pedido.pk, decisao="aprovado",
                    motivo_decisao="Autorizado", operacao_id=uuid4(),
                )
                return "efetivado"
            except CancelamentoDesatualizado:
                return "conflito"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [executor.submit(aprovar) for _ in range(2)]
            self.assertCountEqual([tarefa.result(timeout=10) for tarefa in tarefas], ["efetivado", "conflito"])
        self.assertEqual(inspecao.historico.filter(ato=HistoricoInspecao.Ato.CANCELAMENTO).count(), 1)
