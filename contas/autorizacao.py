from django.core.exceptions import PermissionDenied

from .models import Perfil, Usuario


def exigir_administrador(ator_id, *, bloquear=False):
    usuarios = Usuario.objects.all()
    if bloquear:
        usuarios = usuarios.select_for_update()
    try:
        return usuarios.get(pk=ator_id, is_active=True, perfil=Perfil.ADMINISTRADOR)
    except Usuario.DoesNotExist:
        raise PermissionDenied from None
