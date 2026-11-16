import os
import re
from urllib.parse import urlsplit

from django.core.exceptions import ImproperlyConfigured


HOST_PATTERN = re.compile(r"(?:\.?[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.?|\[[a-fA-F0-9:]+\]|\*)")


def required(name: str) -> str:
    value = os.environ.get(name, "")
    if not value.strip():
        raise ImproperlyConfigured(f"{name} deve ser definida e não pode estar vazia.")
    return value


def read_debug() -> bool:
    value = os.environ.get("DJANGO_DEBUG", "false").strip().lower()
    if value not in {"true", "false"}:
        raise ImproperlyConfigured("DJANGO_DEBUG deve ser true ou false.")
    return value == "true"


def read_hosts() -> list[str]:
    hosts = [host.strip() for host in required("DJANGO_ALLOWED_HOSTS").split(",")]
    if not all(HOST_PATTERN.fullmatch(host) for host in hosts):
        raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS deve conter hosts válidos separados por vírgula.")
    return hosts


def read_csrf_origins() -> list[str]:
    value = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").strip()
    if not value:
        return []
    origins = [origin.strip() for origin in value.split(",")]
    for origin in origins:
        try:
            url = urlsplit(origin)
            port = url.port
            hostname = url.hostname or ""
            if ":" in hostname:
                hostname = f"[{hostname}]"
            host = hostname.removeprefix("*.")
            valid = (
                url.scheme in {"http", "https"}
                and HOST_PATTERN.fullmatch(host)
                and host != "*"
                and url.username is None
                and url.password is None
                and (port is None or port > 0)
                and not url.path
                and "?" not in origin
                and "#" not in origin
                and not any(char.isspace() for char in origin)
            )
        except ValueError:
            valid = False
        if not valid:
            raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS deve conter origens HTTP ou HTTPS válidas.")
    return origins


def read_port() -> int:
    try:
        port = int(required("POSTGRES_PORT"))
    except ValueError:
        port = 0
    if not 1 <= port <= 65535:
        raise ImproperlyConfigured("POSTGRES_PORT deve ser uma porta entre 1 e 65535.")
    return port
