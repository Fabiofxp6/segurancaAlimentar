import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .environment import read_csrf_origins, read_debug, read_hosts, read_port, required


if os.environ.get("DJANGO_SETTINGS_MODULE") not in {
    "config.settings.development",
    "config.settings.test",
    "config.settings.production",
}:
    raise ImproperlyConfigured("DJANGO_SETTINGS_MODULE deve selecionar development, test ou production.")

BASE_DIR = Path(__file__).resolve().parents[2]
SECRET_KEY = required("DJANGO_SECRET_KEY")
DEBUG = read_debug()
ALLOWED_HOSTS = read_hosts()
CSRF_TRUSTED_ORIGINS = read_csrf_origins()

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "contas.apps.ContasConfig",
    "estabelecimentos",
    "checklists",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "contas.middleware.SessaoMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
    },
]

AUTH_USER_MODEL = "contas.Usuario"
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_HTTPONLY = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
TEST_RUNNER = "config.testing.IsolatedTestRunner"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"http_status": {"()": "config.logging.HttpStatusFormatter"}},
    "handlers": {
        "request_errors": {"class": "logging.StreamHandler", "formatter": "http_status"},
    },
    "loggers": {
        "django.request": {
            "handlers": ["request_errors"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.security.csrf": {
            "handlers": ["request_errors"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": required("POSTGRES_DB"),
        "USER": required("POSTGRES_USER"),
        "PASSWORD": required("POSTGRES_PASSWORD"),
        "HOST": required("POSTGRES_HOST"),
        "PORT": read_port(),
    },
}

LANGUAGE_CODE = "pt-br"
USE_TZ = True
TIME_ZONE = "UTC"
