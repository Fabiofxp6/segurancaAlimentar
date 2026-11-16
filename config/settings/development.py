from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


if DATABASES["default"]["PORT"] == 55433:  # noqa: F405
    raise ImproperlyConfigured("A porta 55433 é reservada ao PostgreSQL de testes.")
