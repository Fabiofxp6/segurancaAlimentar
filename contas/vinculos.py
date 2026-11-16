from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from estabelecimentos.models import Estabelecimento, VinculoEstabelecimento

from .autorizacao import exigir_administrador
from .models import Perfil, Usuario


class VinculoDesatualizado(Exception):
    pass


def _contas_estabelecimento():
    return Usuario.objects.filter(
        perfil=Perfil.ESTABELECIMENTO, is_staff=False, is_superuser=False,
    )


def _abertos(usuario_id):
    return VinculoEstabelecimento.objects.filter(usuario_id=usuario_id, encerrado_em__isnull=True)


def dados_gestao(ator_id, usuario_id):
    exigir_administrador(ator_id)
    usuario = _contas_estabelecimento().only("username", "versao_gestao").get(pk=usuario_id)
    atual = _abertos(usuario_id).select_related("estabelecimento").first()
    opcoes = list(
        Estabelecimento.objects.filter(ativo=True).order_by("nome", "pk").values_list("pk", "nome")
    )
    return usuario, atual, opcoes


def estabelecimentos_acessiveis(usuario_id):
    return Estabelecimento.objects.filter(
        ativo=True,
        vinculoestabelecimento__usuario_id=usuario_id,
        vinculoestabelecimento__usuario__perfil=Perfil.ESTABELECIMENTO,
        vinculoestabelecimento__usuario__is_active=True,
        vinculoestabelecimento__usuario__is_staff=False,
        vinculoestabelecimento__usuario__is_superuser=False,
        vinculoestabelecimento__encerrado_em__isnull=True,
    )


def encerrar_abertos(usuario_id, autor_id):
    _abertos(usuario_id).update(encerrado_em=timezone.now(), encerrado_por_id=autor_id)


@transaction.atomic
def alterar(ator_id, usuario_id, *, versao, estabelecimento_id):
    autor = exigir_administrador(ator_id, bloquear=True)
    usuario = _contas_estabelecimento().select_for_update().get(pk=usuario_id)
    atual = _abertos(usuario_id).first()
    if (atual.estabelecimento_id if atual else None) == estabelecimento_id:
        return
    if versao != usuario.versao_gestao:
        raise VinculoDesatualizado
    if estabelecimento_id is not None:
        try:
            estabelecimento = Estabelecimento.objects.select_for_update().get(
                pk=estabelecimento_id, ativo=True,
            )
        except Estabelecimento.DoesNotExist:
            raise ValidationError({"estabelecimento_id": "Selecione um estabelecimento ativo."}) from None

    encerrar_abertos(usuario_id, autor.pk)
    if estabelecimento_id is not None:
        VinculoEstabelecimento.objects.create(
            usuario=usuario, estabelecimento=estabelecimento, criado_por=autor,
        )
    usuario.versao_gestao += 1
    usuario.save(update_fields=["versao_gestao"])
