from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings
from django.db import IntegrityError, OperationalError, connections, transaction
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse

from checklists.models import Checklist, VersaoChecklist
from contas.models import Perfil, Usuario
from estabelecimentos.models import Estabelecimento

from .models import AcaoFiscalizacao, DesignacaoSupervisor, HistoricoInspecao, Inspecao
from .services import atribuir, iniciar_atribuida, supervisor_ativo


class InspecoesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_user("gestao-i05", perfil=Perfil.ADMINISTRADOR)
        cls.fiscal = Usuario.objects.create_user("fiscal-a", perfil=Perfil.FISCALIZACAO)
        cls.colega = Usuario.objects.create_user("fiscal-b", perfil=Perfil.FISCALIZACAO)
        cls.outro = Usuario.objects.create_user("fiscal-c", perfil=Perfil.FISCALIZACAO)
        cls.cliente = Usuario.objects.create_user("cliente", perfil=Perfil.ESTABELECIMENTO)
        cls.tecnico = Usuario.objects.create_user("tecnico", is_staff=True, is_superuser=True)
        cls.unidade = Estabelecimento.objects.create(nome="Mercado Fictício", documento="0007")
        cls.outra_unidade = Estabelecimento.objects.create(nome="Feira Fictícia")
        cls.checklist = Checklist.objects.create(titulo="Checklist fictício", criado_por=cls.admin)
        cls.v1 = cls.publicar_versao(1, "Regra preservada")
        cls.rascunho = Checklist.objects.create(titulo="Ainda em rascunho", criado_por=cls.admin)

    @classmethod
    def publicar_versao(cls, numero, regra):
        return VersaoChecklist.objects.create(
            checklist=cls.checklist, numero=numero, revisao_rascunho=numero,
            titulo="Checklist de teste", regras=regra,
            itens=[{"enunciado": "Item fictício", "opcoes": ["Sim", "Não"], "ordem": 1}],
            publicado_por=cls.admin,
        )

    def navegador(self, ator):
        http = Client(enforce_csrf_checks=True, raise_request_exception=False)
        http.force_login(ator)
        http.get(reverse("contas:acesso"))
        return http

    def post(self, http, nome, *args, **dados):
        return http.post(reverse(f"inspecoes:{nome}", args=args), {
            **dados, "csrfmiddlewaretoken": http.cookies[settings.CSRF_COOKIE_NAME].value,
        })

    def dados_atribuicao(self, **dados):
        return {
            "estabelecimento_id": self.unidade.pk, "responsavel_id": self.fiscal.pk,
            "participantes_ids": [self.colega.pk], "operacao": uuid4(), **dados,
        }

    def criar_atribuida(self, *, acao_id=None, participantes_ids=None, responsavel_id=None):
        return atribuir(
            self.admin.pk, estabelecimento_id=self.unidade.pk, acao_id=acao_id, operacao=uuid4(),
            responsavel_id=responsavel_id or self.fiscal.pk,
            participantes_ids=[self.colega.pk] if participantes_ids is None else participantes_ids,
        )

    def test_atribuicao_agrupa_inspecoes_e_registra_autoria(self):
        http = self.navegador(self.admin)
        dados = self.dados_atribuicao(criada_por=self.tecnico.pk)
        resposta = self.post(http, "atribuir", **dados)
        primeira = Inspecao.objects.get()
        self.assertRedirects(resposta, reverse("inspecoes:detalhe", args=[primeira.pk]))
        self.assertEqual(primeira.estado, Inspecao.Estado.ATRIBUIDA)
        self.assertIsNone(primeira.versao_checklist_id)
        self.assertEqual(primeira.criada_por, self.admin)
        self.assertEqual(primeira.historico.get().autor, self.admin)
        self.assertCountEqual(primeira.participantes.all(), [self.colega])
        self.assertRedirects(self.post(http, "atribuir", **dados), resposta.url)
        self.assertEqual(self.post(
            http, "atribuir", **{**dados, "estabelecimento_id": self.outra_unidade.pk},
        ).status_code, 409)
        segunda_resposta = self.post(http, "atribuir", **self.dados_atribuicao(
            acao_id=primeira.acao_id, estabelecimento_id=self.outra_unidade.pk, responsavel_id=self.outro.pk,
        ))
        self.assertEqual(segunda_resposta.status_code, 302)
        self.assertEqual(primeira.acao.inspecoes.count(), 2)
        self.assertEqual(AcaoFiscalizacao.objects.count(), 1)
        self.assertFalse(DesignacaoSupervisor.objects.exists())

    def test_detalhe_filtrado_por_equipe_e_perfil(self):
        atribuida = self.criar_atribuida()
        url = reverse("inspecoes:detalhe", args=[atribuida.pk])
        self.assertContains(self.navegador(self.colega).get(url), "Mercado Fictício")
        self.assertNotContains(self.navegador(self.outro).get(url), "Mercado Fictício", status_code=404)
        for pessoa in (self.cliente, self.tecnico):
            navegador = self.navegador(pessoa)
            self.assertEqual(navegador.get(reverse("inspecoes:lista")).status_code, 403)
            resposta = navegador.get(url)
            self.assertEqual(resposta.status_code, 403)
            self.assertIn("no-store", resposta.headers["Cache-Control"])

    def test_rejeita_fiscal_inativo_csrf_e_alteracao_de_terceiro(self):
        navegador = self.navegador(self.admin)
        Usuario.objects.filter(pk=self.outro.pk).update(is_active=False)
        resposta = self.post(navegador, "atribuir", **self.dados_atribuicao(responsavel_id=self.outro.pk))
        self.assertTrue(resposta.context["form"].has_error("responsavel_id"))
        self.assertEqual(navegador.post(reverse("inspecoes:atribuir"), self.dados_atribuicao()).status_code, 403)
        self.assertEqual(self.post(self.navegador(self.fiscal), "atribuir", **self.dados_atribuicao()).status_code, 403)
        self.assertFalse(AcaoFiscalizacao.objects.exists())

    def test_atribuida_inicia_pelo_responsavel_e_congela_versao_no_inicio(self):
        inspecao = self.criar_atribuida()
        self.assertEqual(self.post(
            self.navegador(self.colega), "inicio", inspecao.pk, checklist_id=self.checklist.pk,
        ).status_code, 404)
        v2 = self.publicar_versao(2, "Regra no início")
        navegador = self.navegador(self.fiscal)
        resposta = self.post(navegador, "inicio", inspecao.pk, checklist_id=self.checklist.pk)
        self.assertEqual(resposta.status_code, 302)
        inspecao.refresh_from_db()
        self.assertEqual(inspecao.versao_checklist, v2)
        self.assertEqual(inspecao.iniciada_por, self.fiscal)
        self.assertEqual(inspecao.origem, Inspecao.Origem.ADMINISTRATIVA)

        v3 = self.publicar_versao(3, "Regra posterior")
        Estabelecimento.objects.filter(pk=self.unidade.pk).update(nome="Unidade renomeada")
        self.assertEqual(self.post(navegador, "inicio", inspecao.pk, checklist_id=self.checklist.pk).status_code, 302)
        self.assertEqual(inspecao.historico.filter(ato=HistoricoInspecao.Ato.INICIO).count(), 1)
        with self.assertRaisesRegex(IntegrityError, "imutável"), transaction.atomic():
            Inspecao.objects.filter(pk=inspecao.pk).update(versao_checklist=v3)
        pagina = navegador.get(resposta.url)
        self.assertContains(pagina, "Regra no início")
        self.assertContains(pagina, "Mercado Fictício")
        self.assertNotContains(pagina, "Regra posterior")
        self.assertNotContains(pagina, "Unidade renomeada")

    def test_inicio_direto_idempotente_e_sem_designacao(self):
        http = self.navegador(self.fiscal)
        dados = {"operacao": uuid4(), "estabelecimento_id": self.unidade.pk, "checklist_id": self.checklist.pk}
        pagina = http.get(reverse("inspecoes:inicio_direto"))
        self.assertContains(pagina, "Checklist de teste · Versão 1")
        self.assertNotContains(pagina, "Ainda em rascunho")
        invalido = self.post(http, "inicio_direto", **{**dados, "checklist_id": self.rascunho.pk})
        self.assertTrue(invalido.context["form"].has_error("checklist_id"))
        resposta = self.post(http, "inicio_direto", **dados, responsavel_id=self.outro.pk)
        self.assertEqual(resposta.status_code, 302)
        registro = Inspecao.objects.get()
        self.assertEqual(registro.estado, Inspecao.Estado.EM_ANDAMENTO)
        self.assertEqual(registro.responsavel, self.fiscal)
        self.assertEqual(registro.origem, Inspecao.Origem.FISCAL)
        self.assertEqual(registro.identificacao_estabelecimento["documento"], "0007")
        self.assertEqual(registro.historico.get().autor, self.fiscal)

        self.publicar_versao(2, "Regra posterior")
        self.assertRedirects(self.post(http, "inicio_direto", **dados), resposta.url)
        self.assertEqual(self.post(
            http, "inicio_direto", **{**dados, "estabelecimento_id": self.outra_unidade.pk},
        ).status_code, 409)
        self.assertEqual(Inspecao.objects.count(), 1)
        self.assertFalse(supervisor_ativo(registro.acao_id, self.fiscal.pk))

    def test_falha_no_historico_reverte_inicio_e_acao(self):
        http = self.navegador(self.fiscal)
        with patch("inspecoes.services.HistoricoInspecao.objects.create", side_effect=OperationalError("privado")):
            resposta = self.post(
                http, "inicio_direto", operacao=uuid4(), estabelecimento_id=self.unidade.pk,
                checklist_id=self.checklist.pk,
            )
        self.assertContains(resposta, "Operação indisponível", status_code=503)
        self.assertNotContains(resposta, "privado", status_code=503)
        self.assertFalse(Inspecao.objects.exists())
        self.assertFalse(AcaoFiscalizacao.objects.exists())

    def test_supervisores_simultaneos_limitados_a_acao_e_revogacao_na_sessao(self):
        primeira = self.criar_atribuida()
        outra = self.criar_atribuida()
        self.criar_atribuida(acao_id=primeira.acao_id, responsavel_id=self.outro.pk, participantes_ids=[])
        gestor = self.navegador(self.admin)
        fiscal = self.navegador(self.fiscal)
        chave = fiscal.session.session_key
        self.assertEqual(self.post(
            gestor, "supervisao", primeira.acao_id, revisao=1, fiscais_ids=[self.fiscal.pk, self.outro.pk],
        ).status_code, 302)
        self.assertTrue(supervisor_ativo(primeira.acao_id, self.fiscal.pk))
        self.assertTrue(supervisor_ativo(primeira.acao_id, self.outro.pk))
        self.assertFalse(supervisor_ativo(outra.acao_id, self.fiscal.pk))
        self.assertEqual(self.post(
            fiscal, "supervisao", primeira.acao_id, revisao=2, fiscais_ids=[self.fiscal.pk],
        ).status_code, 403)

        detalhe = reverse("inspecoes:detalhe", args=[primeira.pk])
        self.assertContains(fiscal.get(detalhe), "Você é supervisor nesta ação.")
        self.assertEqual(self.post(
            gestor, "supervisao", primeira.acao_id, revisao=2, fiscais_ids=[self.outro.pk],
        ).status_code, 302)
        self.assertEqual(fiscal.session.session_key, chave)
        self.assertNotContains(fiscal.get(detalhe), "Você é supervisor nesta ação.")
        designacao = DesignacaoSupervisor.objects.get(acao=primeira.acao, fiscal=self.fiscal)
        self.assertEqual(designacao.encerrado_por, self.admin)
        self.assertIsNotNone(designacao.fim)
        self.assertEqual(self.post(gestor, "supervisao", primeira.acao_id, revisao=1, fiscais_ids=[]).status_code, 409)

    def test_alterar_equipe_preserva_autoria_e_encerra_designacao_fora_da_acao(self):
        inspecao = self.criar_atribuida()
        gestor = self.navegador(self.admin)
        iniciar_atribuida(self.fiscal.pk, inspecao.pk, checklist_id=self.checklist.pk)
        self.post(gestor, "supervisao", inspecao.acao_id, revisao=1, fiscais_ids=[self.fiscal.pk])
        self.assertEqual(self.post(
            gestor, "equipe", inspecao.pk, revisao=1, responsavel_id=self.colega.pk,
        ).status_code, 302)
        inspecao.refresh_from_db()
        self.assertEqual(inspecao.responsavel, self.colega)
        self.assertEqual(inspecao.iniciada_por, self.fiscal)
        self.assertFalse(supervisor_ativo(inspecao.acao_id, self.fiscal.pk))
        self.assertEqual(inspecao.historico.get(ato=HistoricoInspecao.Ato.INICIO).autor, self.fiscal)
        self.assertEqual(inspecao.historico.get(ato=HistoricoInspecao.Ato.EQUIPE).autor, self.admin)
        self.assertEqual(DesignacaoSupervisor.objects.get().encerrado_por, self.admin)

    def test_designacao_exige_equipe_e_perfil_ativo_atual(self):
        inspecao = self.criar_atribuida()
        gestor = self.navegador(self.admin)
        invalidado = self.post(gestor, "supervisao", inspecao.acao_id, revisao=1, fiscais_ids=[self.outro.pk])
        self.assertTrue(invalidado.context["form"].has_error("fiscais_ids"))
        self.assertEqual(self.post(
            gestor, "supervisao", inspecao.acao_id, revisao=1, fiscais_ids=[self.fiscal.pk],
        ).status_code, 302)
        Usuario.objects.filter(pk=self.fiscal.pk).update(perfil=Perfil.ESTABELECIMENTO)
        self.assertFalse(supervisor_ativo(inspecao.acao_id, self.fiscal.pk))

    @override_settings(INSPECOES_DEMONSTRACAO=False)
    def test_fluxo_de_demonstracao_desabilitado_no_perfil_de_producao(self):
        gestor = self.navegador(self.admin)
        self.assertNotContains(gestor.get(reverse("contas:acesso")), ">Inspeções<")
        self.assertEqual(gestor.get(reverse("inspecoes:lista")).status_code, 403)


class InicioConcorrenteTests(TransactionTestCase):
    def test_dois_envios_confirmam_o_mesmo_inicio_de_uma_atribuicao(self):
        admin = Usuario.objects.create_user("gestao", perfil=Perfil.ADMINISTRADOR)
        fiscal = Usuario.objects.create_user("fiscal", perfil=Perfil.FISCALIZACAO)
        unidade = Estabelecimento.objects.create(nome="Unidade")
        checklist = Checklist.objects.create(titulo="Checklist", criado_por=admin)
        VersaoChecklist.objects.create(
            checklist=checklist, numero=1, revisao_rascunho=1, titulo="Checklist",
            itens=[{"enunciado": "Pergunta"}], publicado_por=admin,
        )
        inspecao = atribuir(
            admin.pk, operacao=uuid4(), estabelecimento_id=unidade.pk, acao_id=None,
            responsavel_id=fiscal.pk, participantes_ids=[],
        )
        juntos = Barrier(2, timeout=8)

        def iniciar():
            try:
                juntos.wait()
                iniciar_atribuida(fiscal.pk, inspecao.pk, checklist_id=checklist.pk)
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futuros = [executor.submit(iniciar) for _ in range(2)]
            for futuro in futuros:
                futuro.result(timeout=10)
        self.assertEqual(inspecao.historico.filter(ato=HistoricoInspecao.Ato.INICIO).count(), 1)
        inspecao.refresh_from_db()
        self.assertEqual(inspecao.estado, Inspecao.Estado.EM_ANDAMENTO)
