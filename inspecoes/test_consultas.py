from datetime import datetime, time, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from django.test import Client, TestCase
from django.urls import reverse

from checklists.models import VersaoChecklist
from contas.models import Perfil, Usuario
from estabelecimentos.models import Estabelecimento

from .campo_services import salvar_resposta
from .conclusao_services import concluir, consultar
from .correcao_services import aplicar
from .models import Inspecao
from .services import alterar_equipe, alterar_supervisao, atribuir, iniciar_atribuida
from .test_correcoes import autorizar, preparar_correcao, propor
from .test_documentos import preparar_documentos
from .test_termos import confirmar_resultado


class ConsultaInspecoesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.unidade, cls.propria = preparar_documentos()
        cls.colega = Usuario.objects.create_user("fiscal-compartilhado", perfil=Perfil.FISCALIZACAO)
        cls.fora = Usuario.objects.create_user("fiscal-reservado", perfil=Perfil.FISCALIZACAO)
        cls.unidade_reservada = Estabelecimento.objects.create(nome="Unidade reservada")
        cls.compartilhada = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=cls.unidade.pk, responsavel_id=cls.colega.pk,
            acao_id=cls.propria.acao_id, participantes_ids=[cls.fiscal.pk],
        )
        cls.reservada = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=cls.unidade_reservada.pk, responsavel_id=cls.fora.pk,
            acao_id=cls.propria.acao_id, participantes_ids=[],
        )
        alterar_supervisao(cls.admin.pk, cls.propria.acao_id, revisao=1, fiscais_ids=[cls.fiscal.pk])

    def navegador(self, usuario):
        http = Client()
        http.force_login(usuario)
        return http

    def consultar(self, usuario, **filtros):
        return self.navegador(usuario).get(reverse("inspecoes:lista"), filtros)

    def test_filtros_existentes_combinados_com_datas_inclusivas(self):
        data = datetime(2026, 11, 10, tzinfo=timezone.utc)
        Inspecao.objects.filter(pk=self.propria.pk).update(criada_em=data)
        Inspecao.objects.filter(pk=self.compartilhada.pk).update(criada_em=datetime.combine(
            data.date(), time.max, tzinfo=timezone.utc,
        ))
        Inspecao.objects.filter(pk=self.reservada.pk).update(criada_em=datetime(
            2026, 11, 11, tzinfo=timezone.utc,
        ))
        resposta = self.consultar(
            self.admin, estado="atribuida", estabelecimento=self.unidade.pk, fiscal=self.fiscal.pk,
            inicio="2026-11-10", fim="10/11/2026", pagina=1,
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual([i.pk for i in resposta.context["pagina"]], [self.compartilhada.pk, self.propria.pk])
        self.assertContains(resposta, 'value="2026-11-10"', count=2)
        self.assertIn("no-store", resposta["Cache-Control"])
        apenas_colega = self.consultar(self.admin, fiscal=self.colega.pk)
        self.assertEqual([i.pk for i in apenas_colega.context["pagina"]], [self.compartilhada.pk])
        todos_no_periodo = self.consultar(self.admin, inicio="2026-11-10", fim="2026-11-10")
        self.assertEqual(todos_no_periodo.context["pagina"].paginator.count, 2)

    def test_escopo_e_filtros_apos_remocao_de_equipe_na_mesma_sessao(self):
        http = self.navegador(self.fiscal)
        url = reverse("inspecoes:lista")
        primeira = http.get(url)
        self.assertEqual(primeira.context["pagina"].paginator.count, 2)
        self.assertNotContains(primeira, "Unidade reservada")
        self.assertNotContains(primeira, "fiscal-reservado")
        for filtro in ({"estabelecimento": self.unidade_reservada.pk}, {"fiscal": self.fora.pk}):
            resposta = http.get(url, filtro)
            self.assertEqual(resposta.status_code, 400)
            self.assertIsNone(resposta.context["pagina"])
        alterar_equipe(
            self.admin.pk, self.compartilhada.pk, revisao=1, responsavel_id=self.colega.pk, participantes_ids=[],
        )
        segunda = http.get(url)
        self.assertEqual([i.pk for i in segunda.context["pagina"]], [self.propria.pk])
        self.assertNotContains(segunda, "fiscal-compartilhado")
        self.assertEqual(self.consultar(self.cliente).status_code, 403)
        self.assertEqual(Client().get(url).status_code, 302)

    def test_datas_estado_e_paginacao_invalidos_nao_entregam_lista(self):
        for filtro in (
            {"inicio": "2026-11-12", "fim": "2026-11-11"}, {"inicio": "2026-13-01"},
            {"estado": "qualquer"}, {"pagina": 0}, {"pagina": -1}, {"pagina": "texto"},
        ):
            with self.subTest(filtro=filtro):
                resposta = self.consultar(self.admin, **filtro)
                self.assertEqual(resposta.status_code, 400)
                self.assertIsNone(resposta.context["pagina"])

    def test_paginacao_preserva_filtros_sem_duplicar_a_equipe(self):
        for _ in range(24):
            atribuir(
                self.admin.pk, operacao=uuid4(), estabelecimento_id=self.unidade.pk,
                responsavel_id=self.fiscal.pk, participantes_ids=[self.colega.pk, self.fora.pk],
                acao_id=self.propria.acao_id,
            )
        filtros = {"estado": "atribuida", "fiscal": self.fiscal.pk}
        primeira = self.consultar(self.admin, **filtros)
        pagina = primeira.context["pagina"]
        self.assertEqual(pagina.paginator.count, 26)
        self.assertEqual(len(pagina.object_list), 25)
        self.assertContains(primeira, f"?estado=atribuida&amp;fiscal={self.fiscal.pk}&amp;pagina=2")
        segunda = self.consultar(self.admin, **filtros, pagina=2)
        self.assertEqual([i.pk for i in segunda.context["pagina"]], [self.propria.pk])
        self.assertEqual(self.consultar(self.admin, **filtros, pagina=100).context["pagina"].number, 2)


class IndicadoresTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin, cls.fiscal, cls.cliente, cls.primeira, cls.v1, itens, base = preparar_correcao()
        cls.unidade = cls.primeira.estabelecimento
        cls.outra_unidade = Estabelecimento.objects.create(nome="Unidade da versão seguinte")
        pedido = propor(cls.fiscal, cls.primeira, base, itens[0], descricao_irregularidade="")
        autorizar(cls.admin, cls.primeira, pedido)
        aplicar(cls.fiscal.pk, cls.primeira.pk, pedido.pk, operacao_id=uuid4())
        segunda = cls.inspecao(cls.unidade, iniciar=True)
        confirmar_resultado(cls.fiscal, segunda, itens)
        sem_nota = cls.inspecao(cls.unidade, iniciar=True)
        for item in itens[:2]:
            salvar_resposta(
                cls.fiscal.pk, sem_nota.pk, UUID(item["id"]), operacao_id=uuid4(), revisao=0,
                opcao="Não se aplica", observacao="", descricao_irregularidade="",
            )
        concluir(cls.fiscal.pk, sem_nota.pk, operacao_id=uuid4(),
                 revisao_base=consultar(cls.fiscal.pk, sem_nota.pk)["revisao_base"])

        cls.v2 = VersaoChecklist.objects.create(
            checklist=cls.v1.checklist, numero=2, revisao_rascunho=2, titulo=cls.v1.titulo,
            itens=[{**itens[0], "peso": "9"}, *itens[1:]], publicado_por=cls.admin,
        )
        outra = cls.inspecao(cls.outra_unidade, iniciar=True)
        confirmar_resultado(cls.fiscal, outra, itens)
        em_andamento = cls.inspecao(cls.unidade, iniciar=True)
        salvar_resposta(
            cls.fiscal.pk, em_andamento.pk, UUID(itens[0]["id"]), operacao_id=uuid4(), revisao=0,
            opcao="Não", observacao="", descricao_irregularidade="Não entra no painel antes da conclusão",
        )
        cls.inspecao(cls.unidade, iniciar=False)
        alterar_supervisao(cls.admin.pk, cls.primeira.acao_id, revisao=1, fiscais_ids=[cls.fiscal.pk])

    @classmethod
    def inspecao(cls, unidade, *, iniciar):
        inspecao = atribuir(
            cls.admin.pk, operacao=uuid4(), estabelecimento_id=unidade.pk, responsavel_id=cls.fiscal.pk,
            participantes_ids=[], acao_id=None,
        )
        if iniciar:
            iniciar_atribuida(cls.fiscal.pk, inspecao.pk, checklist_id=cls.v1.checklist_id)
        return inspecao

    def consultar(self, usuario, **filtros):
        http = Client()
        http.force_login(usuario)
        return http.get(reverse("inspecoes:indicadores"), filtros)

    def test_agregados_usam_a_ultima_revisao_e_separam_versoes(self):
        resposta = self.consultar(self.admin)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context["total_inspecoes"], 6)
        situacoes = dict(resposta.context["situacoes"])
        self.assertEqual(situacoes, {"Atribuída": 1, "Em andamento": 1, "Concluída": 4, "Cancelada": 0})
        grupos = {grupo["versao_checklist_id"]: grupo for grupo in resposta.context["resultados_por_versao"]}
        primeiro, segundo = grupos[self.v1.pk], grupos[self.v2.pk]
        self.assertEqual(
            (primeiro["total"], primeiro["satisfatorias"], primeiro["insatisfatorias"],
             primeiro["sem_pontuacao"], primeiro["media"]),
            (3, 1, 1, 1, Decimal("40.00")),
        )
        self.assertEqual((segundo["total"], segundo["media"]), (1, Decimal("90.00")))
        frequencias = {(i["versao"].numero, i["enunciado"]): i["total"] for i in resposta.context["irregularidades"]}
        self.assertEqual(frequencias, {(1, "Conservação"): 1, (1, "Higiene"): 2, (2, "Conservação"): 1, (2, "Higiene"): 1})
        self.assertNotContains(resposta, "OBSERVAÇÃO INTERNA RESERVADA")

    def test_painel_exclusivo_do_administrador_com_filtros_e_estado_vazio(self):
        self.assertEqual(self.consultar(self.fiscal).status_code, 403)
        self.assertEqual(self.consultar(self.cliente).status_code, 403)
        resposta = self.consultar(self.admin, estabelecimento=self.outra_unidade.pk, estado="concluida")
        self.assertEqual(resposta.context["total_inspecoes"], 1)
        self.assertEqual(len(resposta.context["resultados_por_versao"]), 1)
        self.assertTrue(all(i["versao"] == self.v2 for i in resposta.context["irregularidades"]))
        vazio = self.consultar(self.admin, estado="cancelada")
        self.assertEqual(vazio.context["total_inspecoes"], 0)
        self.assertEqual(vazio.context["resultados_por_versao"], [])
        self.assertEqual(vazio.context["irregularidades"], [])
        invalido = self.consultar(self.admin, fiscal=99999999)
        self.assertEqual(invalido.status_code, 400)
        self.assertNotContains(invalido, "Inspeções por situação", status_code=400)
