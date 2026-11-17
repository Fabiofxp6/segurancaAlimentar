from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.urls import include, path


urlpatterns = [
    path("conta/", include("contas.urls")),
    path("gestao/usuarios/", include("contas.urls_gestao")),
    path("gestao/estabelecimentos/", include("estabelecimentos.urls")),
    path("gestao/checklists/", include("checklists.urls")),
    path("inspecoes/", include("inspecoes.urls")),
]


if settings.SETTINGS_MODULE == "config.settings.development":
    urlpatterns += [path("static/<path:path>", serve, {"insecure": True})]
