from django.conf import settings
from django.db import models


class Checklist(models.Model):
    titulo = models.TextField()
    referencia = models.TextField(blank=True)
    regras = models.TextField(blank=True)
    itens = models.JSONField(default=list, blank=True)
    revisao = models.PositiveBigIntegerField(default=1)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)


class VersaoChecklist(models.Model):
    class Finalidade(models.TextChoices):
        DEMONSTRACAO = "demonstracao", "Demonstração"

    REGRA_DEMONSTRACAO_1 = "demonstracao-1"

    checklist = models.ForeignKey(Checklist, on_delete=models.PROTECT, related_name="versoes")
    numero = models.PositiveBigIntegerField()
    revisao_rascunho = models.PositiveBigIntegerField()
    titulo = models.TextField()
    referencia = models.TextField(blank=True)
    regras = models.TextField(blank=True)
    itens = models.JSONField()
    finalidade = models.CharField(max_length=16, choices=Finalidade, default=Finalidade.DEMONSTRACAO)
    regra_pontuacao = models.CharField(max_length=32, default=REGRA_DEMONSTRACAO_1)
    publicado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    publicado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["checklist", "numero"], name="checklist_numero_versao_unico"),
            models.UniqueConstraint(
                fields=["checklist", "revisao_rascunho"], name="checklist_revisao_publicada_unica",
            ),
            models.CheckConstraint(
                condition=models.Q(finalidade="demonstracao"), name="checklist_finalidade_publicavel",
            ),
        ]
