from .models import OperacaoCampo


class RespostasConfirmadasIndisponiveis(Exception):
    pass


def atual(inspecao):
    return inspecao.resultados.select_related("concluido_por", "versao_checklist").latest("revisao")


def respostas_confirmadas(resultado):
    respostas = resultado.respostas_utilizadas
    if resultado.revisao > 1:
        return respostas
    recibos = OperacaoCampo.objects.filter(
        inspecao_id=resultado.inspecao_id, tipo=OperacaoCampo.Tipo.RESPOSTA, item_id__in=respostas,
    ).values_list(
        "item_id", "resultado__revisao", "dados__opcao", "dados__observacao", "dados__descricao_irregularidade",
    )
    confirmadas = {}
    for item_id, revisao, opcao, observacao, irregularidade in recibos:
        chave = str(item_id)
        if respostas[chave] == {"revisao": revisao, "opcao": opcao}:
            confirmadas[chave] = {
                "opcao": opcao, "revisao": revisao, "observacao": observacao or "",
                "descricao_irregularidade": irregularidade or "",
            }
    if confirmadas.keys() != respostas.keys():
        raise RespostasConfirmadasIndisponiveis("As revisões confirmadas não estão disponíveis.")
    return confirmadas
