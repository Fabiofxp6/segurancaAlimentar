from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario

from . import adiamento_services, correcao_services
from .models import DocumentoEstabelecimento, HistoricoInspecao, Inspecao, PedidoAdiamento, PedidoCorrecao
from .termo_services import emitir, liberar
from .test_conclusao import preparar_conclusao
from .test_documentos import pdf, preparar_documentos
from .test_termos import confirmar_resultado, designar_supervisor


class OperacoesI14Tests(TestCase):
    def sessao(self, pessoa):
        http = Client(enforce_csrf_checks=True)
        http.force_login(pessoa)
        return http

    def url(self, nome, *args):
        return reverse(f"inspecoes:{nome}", args=[self.inspecao.pk, *args])

    def enviar(self, http, pagina, destino, dados):
        return http.post(destino, {
            "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
            **dados,
        }, headers={"X-Contexto-Campo": pagina.context["contexto"]})


class AdiamentoTests(OperacoesI14Tests):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, _, cls.inspecao = preparar_documentos()
        cls.supervisor = designar_supervisor(cls.admin, cls.inspecao)
        cls.checklist = Checklist.objects.create(titulo="Demonstração", criado_por=cls.admin)
        VersaoChecklist.objects.create(
            checklist=cls.checklist, numero=1, revisao_rascunho=1, titulo="Demonstração",
            itens=[{"id": str(uuid4()), "enunciado": "Higiene", "opcoes": ["Sim"]}], publicado_por=cls.admin,
        )

    def test_aprovacao_e_inicio_na_data_sem_mudar_estado_antes(self):
        fiscal = self.sessao(self.fiscal)
        supervisor = self.sessao(self.supervisor)
        pagina = fiscal.get(self.url("adiamento"))
        agendada = (timezone.now() + timedelta(days=2)).replace(second=0, microsecond=0)
        dados = {
            "operacao_id": uuid4(), "justificativa": "Mudança de data",
            "data_proposta": agendada.astimezone(ZoneInfo("America/Maceio")).strftime("%Y-%m-%dT%H:%M"),
        }
        destino = self.url("adiamento_solicitar")
        self.assertEqual(fiscal.post(destino, dados).status_code, 403)
        recibo = self.enviar(fiscal, pagina, destino, dados)
        self.assertEqual(recibo.status_code, 200)
        pedido = PedidoAdiamento.objects.get(inspecao=self.inspecao)
        self.assertEqual(pedido.data_proposta, agendada)
        self.assertEqual(self.enviar(fiscal, pagina, destino, dados).json(), recibo.json())
        self.assertContains(fiscal.get(self.url("detalhe")), "Aguarde a decisão")
        csrf = fiscal.cookies[settings.CSRF_COOKIE_NAME].value
        iniciar = {"csrfmiddlewaretoken": csrf, "checklist_id": self.checklist.pk}
        self.assertContains(fiscal.post(self.url("inicio"), iniciar), "Aguarde a decisão")
        decisao = {"operacao_id": uuid4(), "decisao": "aprovado", "motivo": "Agenda confirmada"}
        self.assertEqual(self.enviar(fiscal, pagina, self.url("adiamento_decidir", pedido.pk), decisao).status_code, 403)
        self.assertContains(supervisor.get(reverse("inspecoes:adiamentos")), f"Inspeção #{self.inspecao.pk}")
        pagina = supervisor.get(self.url("adiamento"))
        destino = self.url("adiamento_decidir", pedido.pk)
        self.assertContains(pagina, "Registrar decisão")
        confirmacao = self.enviar(supervisor, pagina, destino, decisao)
        self.assertEqual(confirmacao.status_code, 200)
        self.assertEqual(self.enviar(supervisor, pagina, destino, decisao).json(), confirmacao.json())
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.ATRIBUIDA)
        self.assertIsNone(self.inspecao.versao_checklist_id)
        self.assertEqual(self.inspecao.agendada_em, agendada)
        self.assertContains(fiscal.post(self.url("inicio"), iniciar), "a partir da data agendada")
        with patch("inspecoes.services.timezone.now", return_value=agendada):
            self.assertEqual(fiscal.post(self.url("inicio"), iniciar).status_code, 302)
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.estado, Inspecao.Estado.EM_ANDAMENTO)
        self.assertIsNotNone(self.inspecao.versao_checklist_id)
        trilha = self.inspecao.historico.filter(ato__in=[
            HistoricoInspecao.Ato.ADIAMENTO_PEDIDO, HistoricoInspecao.Ato.ADIAMENTO_DECISAO,
        ])
        self.assertEqual(trilha.count(), 2)
        self.assertIsNone(trilha.last().dados["data_anterior"])

    def test_admin_so_decide_na_ausencia_e_rejeicao_preserva_data(self):
        anterior = timezone.now() + timedelta(days=1)
        Inspecao.objects.filter(pk=self.inspecao.pk).update(agendada_em=anterior)
        pedido = adiamento_services.solicitar(
            self.fiscal.pk, self.inspecao.pk, operacao_id=uuid4(), data_proposta=anterior + timedelta(days=1),
            justificativa="Indisponibilidade",
        )
        decisao = {"operacao_id": uuid4(), "motivo": "Manter a data", "decisao": "rejeitado"}
        with self.assertRaises(PermissionDenied):
            adiamento_services.decidir(self.admin.pk, self.inspecao.pk, pedido.pk, **decisao)
        Usuario.objects.filter(pk=self.supervisor.pk).update(is_active=False)
        adiamento_services.decidir(self.admin.pk, self.inspecao.pk, pedido.pk, **decisao)
        self.inspecao.refresh_from_db()
        self.assertEqual(self.inspecao.agendada_em, anterior)
        with self.assertRaises(IntegrityError), transaction.atomic():
            PedidoAdiamento.objects.filter(pk=pedido.pk).update(justificativa="Tentativa de adulteração")


class ReanaliseTests(OperacoesI14Tests):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.inspecao, _, cls.itens = preparar_conclusao()
        cls.supervisor = designar_supervisor(cls.admin, cls.inspecao)
        cls.fora = Usuario.objects.create_user("fiscal-fora-i14", perfil=Perfil.FISCALIZACAO)
        cls.outra_unidade = Usuario.objects.create_user("cliente-fora-i14", perfil=Perfil.ESTABELECIMENTO)
        cls.base = confirmar_resultado(cls.fiscal, cls.inspecao, cls.itens)
        cls.termo = emitir(cls.fiscal.pk, cls.inspecao.pk, operacao_id=uuid4())
        liberar(cls.supervisor.pk, cls.inspecao.pk, cls.termo.pk, operacao_id=uuid4())

    def receber(self):
        cliente = self.sessao(self.cliente)
        pagina = cliente.get(self.url("documentos_inspecao"))
        self.assertContains(pagina, "Enviar documento")
        dados = {"operacao_id": uuid4(), "descricao": "Complemento", "arquivo": pdf()}
        recibo = self.enviar(cliente, pagina, self.url("documentos_enviar"), dados)
        self.assertEqual(recibo.status_code, 200)
        return cliente, DocumentoEstabelecimento.objects.get(inspecao=self.inspecao)

    def iniciar_parecer(self, encaminhamento):
        cliente, documento = self.receber()
        self.assertTrue(documento.complemento)
        fiscal = self.sessao(self.fiscal)
        pagina = fiscal.get(self.url("reanalise_documento", documento.pk))
        self.assertContains(pagina, "Registrar parecer")
        dados = {
            "base_id": self.base.pk, "parecer": "Documento revisto pela equipe",
            "indica_correcao": encaminhamento, "operacao_id": uuid4(),
        }
        destino = self.url("reanalise_registrar", documento.pk)
        recibo = self.enviar(fiscal, pagina, destino, dados)
        self.assertEqual(recibo.status_code, 200)
        self.assertEqual(self.enviar(fiscal, pagina, destino, dados).json(), recibo.json())
        self.assertEqual(self.enviar(fiscal, pagina, destino, {**dados, "operacao_id": uuid4()}).status_code, 409)
        return cliente, fiscal, documento

    def test_manter_resultado_com_acessos_e_historico(self):
        cliente, fiscal, doc = self.iniciar_parecer("manter")
        self.assertContains(fiscal.get(self.url("reanalise_documento", doc.pk)), "manter resultado")
        self.assertEqual(self.inspecao.resultados.count(), 1)
        self.assertEqual(self.inspecao.historico.filter(ato=HistoricoInspecao.Ato.REANALISE).count(), 1)
        self.assertNotContains(cliente.get(self.url("documentos_inspecao")), "Documento revisto pela equipe")
        self.assertEqual(cliente.get(self.url("reanalises")).status_code, 403)
        self.assertEqual(self.sessao(self.fora).get(self.url("reanalises")).status_code, 404)
        self.assertEqual(self.sessao(self.outra_unidade).get(self.url("documentos_baixar", doc.pk)).status_code, 404)

    def test_parecer_vincula_correcao_autorizada_e_retificador(self):
        cliente, fiscal, doc = self.iniciar_parecer("corrigir")
        self.assertEqual(self.inspecao.resultados.count(), 1)
        item = self.itens[0]["id"]
        pagina = fiscal.get(self.url("correcao_item", item), {"reanalise": doc.reanalise.pk})
        self.assertContains(pagina, f"Pedido vinculado à reanálise documental #{doc.reanalise.pk}")
        resp = self.enviar(fiscal, pagina, self.url("correcao_solicitar", item), {
            "base_id": self.base.pk, "reanalise_id": doc.reanalise.pk, "operacao_id": uuid4(),
            "opcao": "Não", "justificativa": "Parecer documentado", "descricao_irregularidade": " irregularidade ",
        })
        self.assertEqual(resp.status_code, 200)
        pedido = PedidoCorrecao.objects.get(base=self.base)
        self.assertEqual(pedido.reanalise_id, doc.reanalise.pk)
        self.assertEqual(self.inspecao.resultados.count(), 1)
        supervisor = self.sessao(self.supervisor)
        self.assertContains(supervisor.get(self.url("correcao", pedido.pk)), "Documento revisto pela equipe")
        self.assertEqual(supervisor.get(self.url("correcao_documento", pedido.pk)).status_code, 200)
        self.assertEqual(cliente.get(self.url("correcao_documento", pedido.pk)).status_code, 403)
        correcao_services.decidir(
            self.supervisor.pk, self.inspecao.pk, pedido.pk, aprovada=True, motivo="Conferido", operacao_id=uuid4(),
        )
        resultado = correcao_services.aplicar(self.fiscal.pk, self.inspecao.pk, pedido.pk, operacao_id=uuid4())
        retificador = resultado.termos.get()
        self.assertEqual(resultado.pontuacao, 0)
        self.assertEqual(retificador.anterior_id, self.termo.pk)
        self.assertEqual(cliente.get(reverse("inspecoes:resultado_pdf", args=[retificador.pk])).status_code, 404)
        self.assertEqual(cliente.get(reverse("inspecoes:resultado_pdf", args=[self.termo.pk])).status_code, 200)
