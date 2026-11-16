from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from threading import Barrier
from types import SimpleNamespace
from unittest.mock import patch
from uuid import UUID, uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, OperationalError, connections, transaction
from django.test import Client, SimpleTestCase, TestCase, TransactionTestCase
from django.urls import reverse

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario

from . import conclusao_services, pontuacao
from .cancelamento_services import CancelamentoDesatualizado, solicitar
from .campo_services import CampoDesatualizado, salvar_resposta
from .models import DocumentoEstabelecimento, HistoricoInspecao, Inspecao, ResultadoInspecao
from .services import iniciar_atribuida
from .test_documentos import pdf, preparar_documentos


def preparar_conclusao():
    admin, fiscal, cliente, unidade, inspecao = preparar_documentos()
    checklist = Checklist.objects.create(titulo="Avaliação ponderada", criado_por=admin)
    itens = [
        {
            "id": str(uuid4()), "enunciado": enunciado, "ordem": ordem, "peso": peso,
            "obrigatorio": ordem <= 2, "opcoes": ["Sim", "Não", "Não se aplica"],
        }
        for ordem, (enunciado, peso) in enumerate([
            ("Conservação", "4"), ("Higiene", None), ("Documentação visível", "100"), ("Observação opcional", "50"),
        ], start=1)
    ]
    versao = VersaoChecklist.objects.create(
        checklist=checklist, numero=1, revisao_rascunho=1, titulo=checklist.titulo, itens=itens, publicado_por=admin,
    )
    iniciar_atribuida(fiscal.pk, inspecao.pk, checklist_id=checklist.pk)
    return admin, fiscal, cliente, inspecao, versao, itens


def responder(fiscal, inspecao, item, opcao, *, revisao=0, chave=None):
    return salvar_resposta(
        fiscal.pk, inspecao.pk, UUID(item["id"]), operacao_id=chave or uuid4(), revisao=revisao,
        opcao=opcao, observacao="", descricao_irregularidade="",
    )


class PontuacaoTests(SimpleTestCase):
    def calcular(self, itens):
        versao = SimpleNamespace(
            regra_pontuacao=VersaoChecklist.REGRA_DEMONSTRACAO_1,
            itens=[{"id": str(i), "ordem": i, "peso": peso} for i, (peso, _) in enumerate(itens)],
        )
        respostas = {str(i): {"opcao": opcao} for i, (_, opcao) in enumerate(itens) if opcao is not None}
        return pontuacao.calcular(versao, respostas)

    def test_faixas_aplicadas_depois_do_arredondamento(self):
        for peso, nota, classificacao in [
            ("59.994", "59.99", "insatisfatoria"), ("59.995", "60.00", "regular"),
            ("79.994", "79.99", "regular"), ("79.995", "80.00", "satisfatoria"),
        ]:
            with self.subTest(peso=peso):
                self.assertEqual(self.calcular([
                    (peso, "CONFORME"), (str(100 - Decimal(peso)), "Não conforme"),
                ]), (Decimal(nota), classificacao))

    def test_sem_pontuacao_quando_todos_sao_na_ou_sem_peso_aplicavel(self):
        self.assertEqual(self.calcular([("50", "N/A"), ("0", "Sim"), ("4", None)]), (None, "sem_pontuacao"))
        self.assertEqual(self.calcular([(None, "Sim"), (None, "Não")]), (Decimal("50.00"), "insatisfatoria"))

    def test_peso_negativo_e_resposta_fora_da_regra_sao_explicitos(self):
        for valores in [[("-1", "Sim")], [("1", "Aguardando")]]:
            with self.subTest(valores=valores), self.assertRaises(ValidationError):
                self.calcular(valores)


class ConclusaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.inspecao, cls.versao, cls.itens = preparar_conclusao()

    def setUp(self):
        self.http = self.sessao(self.fiscal)

    def sessao(self, usuario):
        http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        http.force_login(usuario)
        resposta = http.get(reverse("contas:acesso"))
        self.assertEqual(resposta.status_code, 200)
        return http

    def url(self, nome, *args):
        return reverse("inspecoes:" + nome, args=[self.inspecao.pk, *args])

    def revisar(self):
        return self.http.get(self.url("conclusao"))

    def confirmar(self, *, revisao=None, chave=None, http=None):
        pagina = self.revisar()
        http = http or self.http
        contexto = pagina.context["contexto"]
        if http is not self.http:
            contexto = http.get(self.url("cancelamento")).context["contexto"]
        return http.post(self.url("conclusao_confirmar"), {
            "revisao_base": revisao or pagina.context["revisao_base"],
            "operacao_id": chave or uuid4(),
            "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
        }, headers={"X-Contexto-Campo": contexto})

    def responder_obrigatorios(self):
        responder(self.fiscal, self.inspecao, self.itens[0], "Sim")
        responder(self.fiscal, self.inspecao, self.itens[1], "Não")

    def test_versao_original_e_confirmacao_unica_com_documento_opcional(self):
        self.responder_obrigatorios()
        responder(self.fiscal, self.inspecao, self.itens[2], "Não se aplica")
        VersaoChecklist.objects.create(
            checklist=self.versao.checklist, numero=2, revisao_rascunho=2, titulo="Publicação posterior",
            itens=[{**self.itens[0], "peso": "99"}, self.itens[1]], publicado_por=self.admin,
        )
        pagina = self.revisar()
        base = pagina.context["revisao_base"]
        chave = uuid4()
        recibo = self.confirmar(revisao=base, chave=chave)
        self.assertEqual(recibo.status_code, 200)
        self.assertEqual(self.confirmar(revisao=base, chave=chave).json(), recibo.json())
        self.assertEqual(self.confirmar(revisao=base, chave=uuid4()).status_code, 409)
        self.assertEqual(self.confirmar(revisao="a" * 64, chave=chave).status_code, 409)
        resultado = ResultadoInspecao.objects.get()
        self.assertEqual(resultado.versao_checklist, self.versao)
        self.assertEqual(resultado.pontuacao, Decimal("80.00"))
        self.assertEqual(resultado.classificacao, "satisfatoria")
        self.assertEqual(resultado.concluido_por, self.fiscal)
        self.assertEqual(len(resultado.respostas_utilizadas), 3)
        self.assertContains(self.revisar(), "Satisfatória")
        self.assertContains(self.sessao(self.admin).get(self.url("conclusao")), "Satisfatória")
        cliente = self.sessao(self.cliente)
        self.assertEqual(cliente.get(self.url("conclusao")).status_code, 403)
        documentos = cliente.get(self.url("documentos_inspecao"))
        self.assertContains(documentos, "Enviar documento")
        self.assertNotContains(documentos, "Satisfatória")
        self.assertContains(self.http.get(self.url("auditoria")), "Conclusão confirmada")
        self.assertEqual(self.inspecao.historico.filter(ato=HistoricoInspecao.Ato.CONCLUSAO).count(), 1)

    def test_obrigatorio_e_cancelamento_pendente_impedem_post(self):
        pagina = self.revisar()
        self.assertContains(pagina, "Respostas obrigatórias faltantes")
        self.assertEqual(self.confirmar().status_code, 409)
        self.responder_obrigatorios()
        solicitar(self.fiscal.pk, self.inspecao.pk, justificativa="Equipe indisponível", operacao_id=uuid4())
        self.assertContains(self.revisar(), "Há um pedido de cancelamento pendente")
        self.assertEqual(self.confirmar().status_code, 409)
        self.assertFalse(ResultadoInspecao.objects.exists())

    def test_sem_pontuacao_e_leitura_de_campo_apos_concluir(self):
        gravada = responder(self.fiscal, self.inspecao, self.itens[0], "Não se aplica")
        responder(self.fiscal, self.inspecao, self.itens[1], "Não se aplica")
        self.assertEqual(self.confirmar().status_code, 200)
        self.assertContains(self.revisar(), "Sem pontuação")
        self.assertContains(self.http.get(self.url("campo_item", self.itens[0]["id"])), "Não se aplica")
        self.assertEqual(responder(
            self.fiscal, self.inspecao, self.itens[0], "Não se aplica", chave=gravada.operacao_id,
        ), gravada)
        with self.assertRaises(CampoDesatualizado):
            responder(self.fiscal, self.inspecao, self.itens[0], "Sim", revisao=1)
        with self.assertRaises(CancelamentoDesatualizado):
            solicitar(self.fiscal.pk, self.inspecao.pk, justificativa="Fora do estado", operacao_id=uuid4())

    def test_documento_existente_e_recibo_permanecem_apos_conclusao(self):
        cliente = self.sessao(self.cliente)
        pagina = cliente.get(self.url("documentos_inspecao"))

        def enviar(chave):
            return cliente.post(self.url("documentos_enviar"), {
                "operacao_id": chave, "arquivo": pdf(),
                "csrfmiddlewaretoken": cliente.cookies[settings.CSRF_COOKIE_NAME].value,
            }, headers={"X-Contexto-Campo": pagina.context["contexto"]})

        chave = uuid4()
        recibo = enviar(chave)
        self.assertEqual(recibo.status_code, 200)
        self.responder_obrigatorios()
        self.assertEqual(self.confirmar().status_code, 200)
        self.assertContains(cliente.get(self.url("documentos_inspecao")), "Complemento para reanálise")
        self.assertEqual(cliente.get(recibo.json()["url"]).status_code, 200)
        self.assertEqual(enviar(chave).json(), recibo.json())
        self.assertFalse(DocumentoEstabelecimento.objects.get(operacao_id=chave).complemento)
        self.assertEqual(enviar(uuid4()).status_code, 200)
        self.assertEqual(DocumentoEstabelecimento.objects.filter(complemento=True).count(), 1)

    def test_conclusao_exige_csrf_escopo_e_revisao_atual(self):
        self.responder_obrigatorios()
        antes = self.revisar().context["revisao_base"]
        responder(self.fiscal, self.inspecao, self.itens[0], "Não", revisao=1)
        self.assertEqual(self.confirmar(revisao=antes).status_code, 409)
        self.assertEqual(self.http.post(self.url("conclusao_confirmar")).status_code, 403)
        self.assertEqual(self.confirmar(http=self.sessao(self.admin)).status_code, 403)
        fora = Usuario.objects.create_user("fiscal-sem-vinculo", perfil=Perfil.FISCALIZACAO)
        self.assertEqual(self.sessao(fora).get(self.url("conclusao")).status_code, 404)
        self.assertFalse(ResultadoInspecao.objects.exists())

    def test_falha_reverte_estado_e_resultado_e_banco_protege_conclusao(self):
        self.responder_obrigatorios()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Inspecao.objects.filter(pk=self.inspecao.pk).update(estado=Inspecao.Estado.CONCLUIDA)
        with patch("inspecoes.conclusao_services.HistoricoInspecao.objects.create", side_effect=OperationalError):
            self.assertEqual(self.confirmar().status_code, 503)
        self.assertFalse(ResultadoInspecao.objects.exists())
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.EM_ANDAMENTO)
        self.assertEqual(self.confirmar().status_code, 200)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ResultadoInspecao.objects.update(pontuacao=11)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ResultadoInspecao.objects.all().delete()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Inspecao.objects.filter(pk=self.inspecao.pk).update(estado=Inspecao.Estado.EM_ANDAMENTO)


class ConclusaoConcorrenteTests(TransactionTestCase):
    def test_conclusoes_concorrentes_criam_um_resultado(self):
        _, fiscal, _, inspecao, _, itens = preparar_conclusao()
        responder(fiscal, inspecao, itens[0], "Sim")
        responder(fiscal, inspecao, itens[1], "Não")
        base = conclusao_services.consultar(fiscal.pk, inspecao.pk)["revisao_base"]
        juntos = Barrier(2, timeout=8)

        def concluir():
            try:
                juntos.wait()
                conclusao_services.concluir(fiscal.pk, inspecao.pk, operacao_id=uuid4(), revisao_base=base)
                return "confirmada"
            except conclusao_services.ConclusaoDesatualizada:
                return "conflito"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            tarefas = [executor.submit(concluir) for _ in range(2)]
            self.assertCountEqual([tarefa.result(timeout=10) for tarefa in tarefas], ["confirmada", "conflito"])
        self.assertEqual(ResultadoInspecao.objects.count(), 1)
        self.assertEqual(inspecao.historico.filter(ato=HistoricoInspecao.Ato.CONCLUSAO).count(), 1)
