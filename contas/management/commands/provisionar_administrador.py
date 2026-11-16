from getpass import getuser

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from contas.services import conceder_administrador


class Command(BaseCommand):
    help = "Concede o perfil Administrador a uma conta própria, ativa e com senha já configurada."

    def add_arguments(self, parser):
        parser.add_argument("username", metavar="nome-de-usuario")

    def handle(self, *args, **options):
        try:
            concedido = conceder_administrador(options["username"], getuser())
        except ValidationError as erro:
            raise CommandError(erro.messages[0]) from None
        if concedido:
            self.stdout.write(self.style.SUCCESS("Perfil Administrador concedido e registrado."))
        else:
            self.stdout.write("A conta já tem o perfil Administrador.")
