from django.conf import settings
from django.db import models


class Estabelecimento(models.Model):
    nome = models.TextField()
    documento = models.TextField(blank=True)
    endereco = models.TextField(blank=True)
    contato = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    versao = models.PositiveBigIntegerField(default=1)


class HistoricoEstabelecimento(models.Model):
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.PROTECT)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    versao = models.PositiveBigIntegerField()
    registrado_em = models.DateTimeField(auto_now_add=True)
    alteracoes = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estabelecimento", "versao"],
                name="estabelecimento_historico_versao_unica",
            ),
        ]


class VinculoEstabelecimento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.PROTECT)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="vinculos_concedidos",
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    encerrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT,
        related_name="vinculos_encerrados",
    )
    encerrado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario"], condition=models.Q(encerrado_em__isnull=True),
                name="vinculo_aberto_unico_por_usuario",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(encerrado_em__isnull=True, encerrado_por__isnull=True)
                    | models.Q(encerrado_em__isnull=False, encerrado_por__isnull=False)
                ),
                name="vinculo_encerramento_completo",
            ),
        ]
