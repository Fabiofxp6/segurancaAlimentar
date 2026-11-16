from django.http import JsonResponse
from django.utils.crypto import constant_time_compare, salted_hmac


def contexto_envio(request):
    sessao = f"{request.user.pk}:{request.session.session_key}"
    return salted_hmac("inspecoes.campo", sessao, algorithm="sha256").hexdigest()


class ContextoEnvioMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not constant_time_compare(
            request.headers.get("X-Contexto-Campo", ""), contexto_envio(request),
        ):
            return JsonResponse({"erro": "A sessão da tela mudou. Reabra a página."}, status=401)
        return super().dispatch(request, *args, **kwargs)
