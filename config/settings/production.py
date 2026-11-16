from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


if DEBUG:  # noqa: F405
    raise ImproperlyConfigured("DJANGO_DEBUG deve ser false em produção.")
if "*" in ALLOWED_HOSTS:  # noqa: F405
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS deve indicar hosts explícitos em produção.")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
