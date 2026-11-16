from django.contrib.sessions.middleware import SessionMiddleware
from django.db import InterfaceError, OperationalError
from django.shortcuts import render
from django.utils.cache import add_never_cache_headers


class SessaoMiddleware(SessionMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, (OperationalError, InterfaceError)) and self._rota_protegida(request):
            return self._indisponivel(request)
        return None

    def process_response(self, request, response):
        rota_protegida = self._rota_protegida(request)
        try:
            response = super().process_response(request, response)
        except (OperationalError, InterfaceError):
            if not rota_protegida:
                raise
            response = self._indisponivel(request)
        if rota_protegida:
            add_never_cache_headers(response)
        return response

    @staticmethod
    def _rota_protegida(request):
        route = request.resolver_match
        return route is not None and route.namespace in {"contas", "estabelecimentos", "gestao_contas", "checklists"}

    @staticmethod
    def _indisponivel(request):
        template = (
            "contas/indisponivel.html" if request.resolver_match.namespace == "contas"
            else "gestao/indisponivel.html"
        )
        return render(request, template, status=503)
