from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction

from .autorizacao import exigir_administrador
from .vinculos import encerrar_abertos
from .models import PERFIS_GERENCIAVEIS, HistoricoUsuario, Perfil, Usuario


class CadastroDesatualizado(Exception):
    pass


def _gerenciaveis():
    return Usuario.objects.filter(is_staff=False, is_superuser=False).exclude(
        perfil=Perfil.ADMINISTRADOR,
    )


def _validar_perfil(perfil):
    if perfil not in PERFIS_GERENCIAVEIS:
        raise PermissionDenied


def listar(ator_id, pagina):
    exigir_administrador(ator_id)
    usuarios = _gerenciaveis().only(
        "nome", "username", "perfil", "is_active",
    ).order_by("username", "pk")
    return Paginator(usuarios, 25).get_page(pagina)


def consultar(ator_id, usuario_id):
    exigir_administrador(ator_id)
    return _gerenciaveis().get(pk=usuario_id)


def criar(ator_id, *, nome, username, perfil):
    try:
        return _criar(ator_id, nome=nome, username=username, perfil=perfil)
    except IntegrityError as erro:
        if getattr(getattr(erro.__cause__, "diag", None), "constraint_name", "") == "contas_usuario_username_key":
            raise ValidationError({"username": "Este nome de usuário já está em uso."}) from None
        raise


@transaction.atomic
def _criar(ator_id, *, nome, username, perfil):
    autor = exigir_administrador(ator_id, bloquear=True)
    _validar_perfil(perfil)
    usuario = Usuario.objects.create_user(
        username=username, nome=nome, perfil=perfil, is_active=False,
    )
    HistoricoUsuario.objects.create(
        usuario=usuario, autor=autor, versao=usuario.versao_gestao,
        alteracoes={
            "nome": {"atual": nome}, "username": {"atual": username},
            "perfil": {"atual": perfil}, "is_active": {"atual": False},
        },
    )
    return usuario


@transaction.atomic
def editar(ator_id, usuario_id, *, nome, perfil, situacao, versao):
    autor = exigir_administrador(ator_id, bloquear=True)
    _validar_perfil(perfil)
    usuario = _gerenciaveis().select_for_update().get(pk=usuario_id)
    if versao != usuario.versao_gestao:
        raise CadastroDesatualizado
    if situacao and not usuario.has_usable_password():
        raise ValidationError({"situacao": "A conta precisa de uma credencial antes de ser ativada."})

    valores = {"nome": nome, "perfil": perfil, "is_active": situacao}
    alteracoes = {
        campo: {"anterior": getattr(usuario, campo), "atual": valor}
        for campo, valor in valores.items()
        if valor != getattr(usuario, campo)
    }
    if alteracoes:
        if usuario.perfil == Perfil.ESTABELECIMENTO and perfil != Perfil.ESTABELECIMENTO:
            encerrar_abertos(usuario.pk, autor.pk)
        for campo in alteracoes:
            setattr(usuario, campo, valores[campo])
        usuario.versao_gestao += 1
        usuario.save(update_fields=[*alteracoes, "versao_gestao"])
        HistoricoUsuario.objects.create(
            usuario=usuario, autor=autor, versao=usuario.versao_gestao, alteracoes=alteracoes,
        )
    return usuario


@transaction.atomic
def conceder_administrador(username, operador):
    operador = operador.strip()
    if not operador:
        raise ValidationError("A concessão exige a identificação do operador técnico.")

    try:
        usuario = Usuario.objects.select_for_update().get(
            username=username, is_active=True, is_staff=False, is_superuser=False,
            perfil__in=("", Perfil.ADMINISTRADOR),
        )
    except Usuario.DoesNotExist:
        raise ValidationError("Use uma conta ativa e dedicada à gestão administrativa.") from None
    if not usuario.has_usable_password():
        raise ValidationError("Configure a senha da conta antes da concessão do perfil.")
    if usuario.perfil == Perfil.ADMINISTRADOR:
        return False

    usuario.perfil = Perfil.ADMINISTRADOR
    usuario.versao_gestao += 1
    usuario.save(update_fields=["perfil", "versao_gestao"])
    HistoricoUsuario.objects.create(
        usuario=usuario, operador_tecnico=operador, versao=usuario.versao_gestao,
        alteracoes={"perfil": {"anterior": "", "atual": Perfil.ADMINISTRADOR}},
    )
    return True
