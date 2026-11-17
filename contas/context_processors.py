from django.conf import settings


def navegacao_desktop(request):
    rota = request.resolver_match
    ativo = ""
    if rota:
        ativo = {
            "contas": "inicio",
            "gestao_contas": "usuarios",
            "estabelecimentos": "estabelecimentos",
            "checklists": "checklists",
        }.get(rota.namespace, "")
        if rota.namespace == "inspecoes":
            ativo = "inspecoes"
            for prefixo, secao in (
                ("indicadores", "indicadores"),
                ("adiamento", "adiamentos"),
                ("cancelamento", "cancelamentos"),
                ("correc", "correcoes"),
                ("revisoes", "correcoes"),
                ("termo", "termos"),
                ("documentos", "documentos"),
                ("resultado", "resultados"),
            ):
                if (rota.url_name or "").startswith(prefixo):
                    ativo = secao
                    break
    return {
        "navegacao_ativa": ativo,
        "inspecoes_habilitadas": settings.INSPECOES_DEMONSTRACAO,
    }
