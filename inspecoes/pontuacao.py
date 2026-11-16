from decimal import Decimal, ROUND_HALF_UP, localcontext

from django.core.exceptions import ValidationError

from checklists.models import VersaoChecklist

from .models import ResultadoInspecao


OPCOES_DEMONSTRACAO_1 = {
    "conforme": 1,
    "sim": 1,
    "não conforme": 0,
    "não": 0,
    "não se aplica": None,
    "n/a": None,
}


def calcular(versao, respostas):
    if versao.regra_pontuacao != VersaoChecklist.REGRA_DEMONSTRACAO_1:
        raise ValidationError("A regra desta versão do checklist não está disponível para cálculo.")

    classificacao = ResultadoInspecao.Classificacao
    with localcontext() as contexto:
        contexto.prec = 32 + len(str(len(versao.itens)))
        conforme = Decimal(0)
        aplicavel = Decimal(0)
        for item in versao.itens:
            resposta = respostas.get(item["id"])
            if resposta is None:
                continue
            opcao = resposta["opcao"].casefold()
            if opcao not in OPCOES_DEMONSTRACAO_1:
                raise ValidationError(f"O item {item['ordem']} tem uma resposta sem regra de pontuação.")
            valor = OPCOES_DEMONSTRACAO_1[opcao]
            if valor is None:
                continue
            peso = Decimal(item["peso"]) if item.get("peso") is not None else Decimal(1)
            if peso < 0:
                raise ValidationError(f"O item {item['ordem']} tem peso negativo na versão vinculada.")
            conforme += peso * valor
            aplicavel += peso
        if not aplicavel:
            return None, classificacao.SEM_PONTUACAO
        nota = (100 * conforme / aplicavel).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if nota >= 80:
        return nota, classificacao.SATISFATORIA
    if nota >= 60:
        return nota, classificacao.REGULAR
    return nota, classificacao.INSATISFATORIA
