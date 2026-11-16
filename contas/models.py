from django.contrib.auth.models import AbstractUser
from django.db import models


class Perfil(models.TextChoices):
    ADMINISTRADOR = "administrador", "Administrador"
    FISCALIZACAO = "fiscalizacao", "Fiscalização"
    ESTABELECIMENTO = "estabelecimento", "Estabelecimento"


PERFIS_GERENCIAVEIS = (Perfil.FISCALIZACAO, Perfil.ESTABELECIMENTO)


class Usuario(AbstractUser):
    perfil = models.CharField(max_length=15, choices=Perfil, blank=True, default="")

    nome = models.TextField(blank=True)
    versao_gestao = models.PositiveBigIntegerField(default=1)

    class Meta(AbstractUser.Meta):
        constraints = [
            models.CheckConstraint(
                condition=models.Q(perfil__in=["", *Perfil.values]),
                name="contas_usuario_perfil_valido",
            ),
        ]


class HistoricoUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="historico_gestao")
    autor = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, related_name="atos_de_gestao", null=True, blank=True,
    )
    operador_tecnico = models.TextField(blank=True, default="")
    versao = models.PositiveBigIntegerField()
    registrado_em = models.DateTimeField(auto_now_add=True)
    alteracoes = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["usuario", "versao"], name="contas_historico_versao_unica"),
            models.CheckConstraint(
                condition=(
                    models.Q(autor__isnull=False, operador_tecnico="")
                    | (models.Q(autor__isnull=True) & ~models.Q(operador_tecnico=""))
                ),
                name="contas_historico_autor_ou_operador",
            ),
        ]
