from django.conf import settings
from django.db import models
from django.utils import timezone


class AcaoFiscalizacao(models.Model):
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    criada_em = models.DateTimeField(auto_now_add=True)
    revisao_supervisao = models.PositiveBigIntegerField(default=1)


class Inspecao(models.Model):
    class Origem(models.TextChoices):
        ADMINISTRATIVA = "administrativa", "Atribuição administrativa"
        FISCAL = "fiscal", "Início pelo fiscal"

    class Estado(models.TextChoices):
        ATRIBUIDA = "atribuida", "Atribuída"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CANCELADA = "cancelada", "Cancelada"
        CONCLUIDA = "concluida", "Concluída"

    acao = models.ForeignKey(AcaoFiscalizacao, on_delete=models.PROTECT, related_name="inspecoes")
    estabelecimento = models.ForeignKey("estabelecimentos.Estabelecimento", on_delete=models.PROTECT)
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="inspecoes_responsavel",
    )
    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="inspecoes_participante",
    )
    origem = models.CharField(max_length=15, choices=Origem)
    estado = models.CharField(max_length=12, choices=Estado)
    criada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="inspecoes_criadas",
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    operacao_criacao = models.UUIDField()
    revisao = models.PositiveBigIntegerField(default=1)
    iniciada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name="inspecoes_iniciadas",
    )
    iniciada_em = models.DateTimeField(null=True)
    agendada_em = models.DateTimeField(null=True)
    cancelada_em = models.DateTimeField(null=True)
    versao_checklist = models.ForeignKey("checklists.VersaoChecklist", on_delete=models.PROTECT, null=True)
    identificacao_estabelecimento = models.JSONField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["criada_por", "operacao_criacao"], name="inspecao_operacao_criacao_unica",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        estado="atribuida", origem="administrativa", iniciada_por__isnull=True,
                        iniciada_em__isnull=True, versao_checklist__isnull=True,
                        identificacao_estabelecimento__isnull=True,
                    )
                    | models.Q(
                        estado__in=["em_andamento", "cancelada", "concluida"], origem__in=["administrativa", "fiscal"],
                        iniciada_por__isnull=False, iniciada_em__isnull=False,
                        versao_checklist__isnull=False, identificacao_estabelecimento__isnull=False,
                    )
                ),
                name="inspecao_estado_e_inicio_coerentes",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(estado="cancelada", cancelada_em__isnull=False)
                    | (~models.Q(estado="cancelada") & models.Q(cancelada_em__isnull=True))
                ),
                name="inspecao_cancelamento_e_data_coerentes",
            ),
        ]


class HistoricoInspecao(models.Model):
    class Ato(models.TextChoices):
        ATRIBUICAO = "atribuicao", "Atribuição"
        INICIO = "inicio", "Início"
        EQUIPE = "equipe", "Alteração de equipe"
        PEDIDO_CANCELAR = "pedido_cancelar", "Solicitação de cancelamento"
        DECISAO_CANCELAR = "decisao_cancelar", "Decisão de cancelamento"
        CANCELAMENTO = "cancelamento", "Cancelamento efetivado"
        CONCLUSAO = "conclusao", "Conclusão confirmada"
        TERMO_EMITIDO = "termo_emitido", "Termo emitido"
        TERMO_LIBERADO = "termo_liberado", "Resultado e termo liberados"
        CORRECAO_PEDIDA = "correcao_pedido", "Correção solicitada"
        CORRECAO_DECIDIDA = "correcao_decisao", "Decisão de correção"
        CORRECAO_APLICADA = "correcao_aplic", "Correção aplicada"
        ADIAMENTO_PEDIDO = "adiamento_pedido", "Adiamento solicitado"
        ADIAMENTO_DECISAO = "adiamento_dec", "Decisão de adiamento"
        REANALISE = "reanalise", "Reanálise documental registrada"
        OBSERVACAO = "observacao", "Observação geral registrada"

    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="historico")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    ato = models.CharField(max_length=16, choices=Ato)
    registrado_em = models.DateTimeField(auto_now_add=True)
    dados = models.JSONField(default=dict)

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(
                fields=["inspecao", "ato"], condition=models.Q(ato__in=["atribuicao", "inicio"]),
                name="inspecao_historico_inicio_atribuicao_unicos",
            ),
            models.UniqueConstraint(
                fields=["inspecao"], condition=models.Q(ato="conclusao"),
                name="inspecao_evento_conclusao_unico",
            ),
        ]


class DesignacaoSupervisor(models.Model):
    acao = models.ForeignKey(AcaoFiscalizacao, on_delete=models.PROTECT, related_name="designacoes")
    fiscal = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="designacoes_supervisor",
    )
    designado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="supervisores_designados",
    )
    inicio = models.DateTimeField()
    fim = models.DateTimeField(null=True)
    encerrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name="supervisoes_encerradas",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["acao", "fiscal"], condition=models.Q(fim__isnull=True),
                name="supervisao_aberta_unica_por_fiscal_acao",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(fim__isnull=True, encerrado_por__isnull=True)
                    | models.Q(fim__gte=models.F("inicio"), fim__isnull=False, encerrado_por__isnull=False)
                ),
                name="supervisao_encerramento_coerente",
            ),
        ]


class RespostaCampo(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="respostas_campo")
    item_id = models.UUIDField()
    opcao = models.TextField()
    observacao = models.TextField(blank=True)
    descricao_irregularidade = models.TextField(blank=True)
    revisao = models.PositiveBigIntegerField()
    alterada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    alterada_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["inspecao", "item_id"], name="campo_resposta_unica_por_item"),
        ]


class EvidenciaCampo(models.Model):
    class Vinculo(models.TextChoices):
        ITEM = "item", "Item"
        IRREGULARIDADE = "irregularidade", "Irregularidade"

    resposta = models.ForeignKey(RespostaCampo, on_delete=models.PROTECT, related_name="evidencias")
    vinculo = models.CharField(max_length=14, choices=Vinculo)
    descricao_irregularidade = models.TextField(blank=True)
    nome = models.CharField(max_length=160)
    mime = models.CharField(max_length=20)
    tamanho = models.PositiveIntegerField()
    conteudo = models.BinaryField(editable=False)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    recebida_em = models.DateTimeField(auto_now_add=True)


class OperacaoCampo(models.Model):
    class Tipo(models.TextChoices):
        RESPOSTA = "resposta", "Resposta"
        EVIDENCIA = "evidencia", "Evidência"

    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT)
    item_id = models.UUIDField()
    operacao_id = models.UUIDField()
    tipo = models.CharField(max_length=9, choices=Tipo)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    impressao = models.CharField(max_length=64)
    dados = models.JSONField()
    resultado = models.JSONField()
    confirmado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["inspecao", "operacao_id"], name="campo_operacao_unica_por_inspecao"),
        ]


class DocumentoEstabelecimento(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="documentos_estabelecimento")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    operacao_id = models.UUIDField()
    descricao = models.TextField(blank=True)
    nome = models.CharField(max_length=160)
    mime = models.CharField(max_length=20)
    tamanho = models.PositiveIntegerField()
    sha256 = models.CharField(max_length=64)
    conteudo = models.BinaryField(editable=False)
    recebido_em = models.DateTimeField(auto_now_add=True)
    complemento = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["inspecao", "operacao_id"], name="documento_estabelecimento_operacao_unica",
            ),
        ]

class PedidoCancelamento(models.Model):
    class Situacao(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        APROVADO = "aprovado", "Aprovado"
        REJEITADO = "rejeitado", "Rejeitado"
        EFETIVADO = "efetivado", "Efetivado"

    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="pedidos_cancelamento")
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="cancelamentos_solicitados",
    )
    justificativa = models.TextField()
    solicitada_em = models.DateTimeField(auto_now_add=True)
    operacao_solicitacao = models.UUIDField()
    situacao = models.CharField(max_length=9, choices=Situacao, default=Situacao.PENDENTE)
    decidido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name="cancelamentos_decididos",
    )
    decidida_em = models.DateTimeField(null=True)
    motivo_decisao = models.TextField(blank=True)
    operacao_decisao = models.UUIDField(null=True)
    designacao = models.ForeignKey(DesignacaoSupervisor, on_delete=models.PROTECT, null=True)
    efetivada_em = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["inspecao", "operacao_solicitacao"], name="cancelamento_operacao_solicitacao_unica",
            ),
            models.UniqueConstraint(
                fields=["inspecao"],
                condition=models.Q(situacao__in=["pendente", "aprovado", "efetivado"]),
                name="cancelamento_pedido_ativo_unico",
            ),
            models.CheckConstraint(
                condition=~models.Q(justificativa=""), name="cancelamento_justificativa_preenchida",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        situacao="pendente", decidido_por__isnull=True, decidida_em__isnull=True,
                        operacao_decisao__isnull=True, motivo_decisao="", designacao__isnull=True,
                    )
                    | (
                        models.Q(
                            situacao__in=["aprovado", "rejeitado", "efetivado"], decidido_por__isnull=False,
                            decidida_em__isnull=False, operacao_decisao__isnull=False,
                            decidida_em__gte=models.F("solicitada_em"),
                        )
                        & ~models.Q(motivo_decisao="")
                        & ~models.Q(decidido_por=models.F("solicitante"))
                    )
                ),
                name="cancelamento_decisao_coerente",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        situacao="efetivado", efetivada_em__isnull=False, efetivada_em__gte=models.F("decidida_em"),
                    )
                    | (
                        ~models.Q(situacao="efetivado")
                        & models.Q(efetivada_em__isnull=True)
                    )
                ),
                name="cancelamento_efetivacao_coerente",
            ),
        ]


class ResultadoInspecao(models.Model):
    class Classificacao(models.TextChoices):
        SATISFATORIA = "satisfatoria", "Satisfatória"
        REGULAR = "regular", "Regular"
        INSATISFATORIA = "insatisfatoria", "Insatisfatória"
        SEM_PONTUACAO = "sem_pontuacao", "Sem pontuação"

    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="resultados")
    revisao = models.PositiveIntegerField(default=1)
    correcao = models.OneToOneField(
        "PedidoCorrecao", on_delete=models.PROTECT, null=True, related_name="resultado_aplicado",
    )
    aplicado_em = models.DateTimeField(null=True)
    aplicado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name="resultados_corrigidos",
    )
    versao_checklist = models.ForeignKey("checklists.VersaoChecklist", on_delete=models.PROTECT)
    regra_pontuacao = models.CharField(max_length=32)
    pontuacao = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    classificacao = models.CharField(max_length=15, choices=Classificacao)
    respostas_utilizadas = models.JSONField()
    revisao_base = models.CharField(max_length=64)
    concluido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    concluido_em = models.DateTimeField(default=timezone.now, editable=False)
    operacao_id = models.UUIDField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(classificacao="sem_pontuacao", pontuacao__isnull=True)
                    | models.Q(
                        classificacao__in=["satisfatoria", "regular", "insatisfatoria"],
                        pontuacao__isnull=False, pontuacao__gte=0, pontuacao__lte=100,
                    )
                ),
                name="resultado_pontuacao_e_classificacao_coerentes",
            ),
            models.UniqueConstraint(fields=["inspecao", "revisao"], name="resultado_revisao_unica_por_inspecao"),
            models.CheckConstraint(
                condition=(
                    models.Q(revisao=1, correcao__isnull=True, aplicado_em__isnull=True, aplicado_por__isnull=True)
                    | models.Q(revisao__gt=1, correcao__isnull=False, aplicado_em__isnull=False, aplicado_por__isnull=False)
                ),
                name="resultado_revisao_e_correcao_coerentes",
            ),
        ]


class TermoInspecao(models.Model):
    resultado = models.ForeignKey(ResultadoInspecao, on_delete=models.PROTECT, related_name="termos")
    anterior = models.ForeignKey("self", on_delete=models.PROTECT, null=True, related_name="retificadores")
    codigo = models.CharField(max_length=48, unique=True)
    versao = models.PositiveSmallIntegerField(default=1)
    emitido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    emitido_em = models.DateTimeField()
    operacao_id = models.UUIDField()
    conteudo = models.BinaryField(editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["resultado", "versao"], name="termo_versao_unica_por_resultado"),
        ]


class LiberacaoTermo(models.Model):
    termo = models.OneToOneField(TermoInspecao, on_delete=models.PROTECT, related_name="liberacao")
    liberado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    designacao = models.ForeignKey(DesignacaoSupervisor, on_delete=models.PROTECT, null=True)
    liberado_em = models.DateTimeField(auto_now_add=True)
    operacao_id = models.UUIDField()


class PedidoCorrecao(models.Model):
    reanalise = models.ForeignKey("ReanaliseDocumento", null=True, on_delete=models.PROTECT)
    base = models.ForeignKey(ResultadoInspecao, on_delete=models.PROTECT, related_name="pedidos_correcao")
    item_id = models.UUIDField()
    antes = models.JSONField(null=True)
    proposto = models.JSONField()
    justificativa = models.CharField(max_length=2000)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    solicitada_em = models.DateTimeField(auto_now_add=True)
    operacao_id = models.UUIDField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["base", "operacao_id"], name="correcao_pedido_operacao_unica"),
        ]

    @property
    def situacao(self):
        if hasattr(self, "resultado_aplicado"):
            return "Aplicada"
        decisao = getattr(self, "decisao", None)
        if decisao is None:
            return "Pendente"
        return "Aprovada" if decisao.aprovada else "Rejeitada"


class DecisaoCorrecao(models.Model):
    pedido = models.OneToOneField(PedidoCorrecao, on_delete=models.PROTECT, related_name="decisao")
    aprovada = models.BooleanField()
    motivo = models.CharField(max_length=2000)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    designacao = models.ForeignKey(DesignacaoSupervisor, on_delete=models.PROTECT, null=True)
    decidida_em = models.DateTimeField(auto_now_add=True)
    operacao_id = models.UUIDField()


class PedidoAdiamento(models.Model):
    class Situacao(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        APROVADO = "aprovado", "Aprovado"
        REJEITADO = "rejeitado", "Rejeitado"

    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="pedidos_adiamento")
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="adiamentos_solicitados",
    )
    solicitada_em = models.DateTimeField(auto_now_add=True)
    operacao_id = models.UUIDField()
    data_proposta = models.DateTimeField()
    justificativa = models.CharField(max_length=2000)
    situacao = models.CharField(max_length=10, choices=Situacao, default=Situacao.PENDENTE)
    decidido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="adiamentos_decididos",
    )
    designacao = models.ForeignKey(DesignacaoSupervisor, null=True, on_delete=models.PROTECT)
    decidida_em = models.DateTimeField(null=True)
    operacao_decisao = models.UUIDField(null=True)
    motivo_decisao = models.CharField(max_length=2000, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["inspecao", "operacao_id"], name="adiamento_operacao_unica"),
            models.UniqueConstraint(
                fields=["inspecao"], condition=models.Q(situacao="pendente"), name="adiamento_pendente_unico",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        situacao="pendente", decidido_por__isnull=True, decidida_em__isnull=True,
                        operacao_decisao__isnull=True, designacao__isnull=True, motivo_decisao="",
                    )
                    | (
                        models.Q(
                            situacao__in=["aprovado", "rejeitado"], decidido_por__isnull=False,
                            decidida_em__isnull=False, operacao_decisao__isnull=False,
                        )
                        & ~models.Q(decidido_por=models.F("solicitante"))
                        & ~models.Q(motivo_decisao="")
                    )
                ),
                name="adiamento_decisao_coerente",
            ),
        ]


class ReanaliseDocumento(models.Model):
    documento = models.OneToOneField(DocumentoEstabelecimento, on_delete=models.PROTECT, related_name="reanalise")
    base = models.ForeignKey(ResultadoInspecao, on_delete=models.PROTECT)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    registrada_em = models.DateTimeField(auto_now_add=True)
    operacao_id = models.UUIDField()
    parecer = models.CharField(max_length=2000)
    indica_correcao = models.BooleanField()


class ObservacaoInspecao(models.Model):
    inspecao = models.ForeignKey(Inspecao, on_delete=models.PROTECT, related_name="observacoes_gerais")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    texto = models.CharField(max_length=1000)
    operacao_id = models.UUIDField()
    registrada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["inspecao", "operacao_id"], name="observacao_inspecao_operacao_unica",
            ),
        ]
