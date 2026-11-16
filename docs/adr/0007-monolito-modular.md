# ADR 0007: Proposta de monólito modular

- **Status:** Aceito para a fundação I01 em 15/11/2026.
- **Data:** 2026-11-10.
- **Natureza:** decisão estrutural aceita ao autorizar a I01. [DC025](../decisoes-confirmadas.md#dc025-monólito-modular-na-fundação)
- **Origem:** proposta em F007 no [índice de fontes](../referencias/README.md), analisada a partir de DC003 a DC006 e do [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md).

## Contexto

A base escolhida é Django com templates e PostgreSQL. Não há volume, equipe operacional, orçamento ou integrações que justifiquem distribuição em serviços independentes neste momento. Essa ausência de informação recomenda simplicidade inicial, sem provar uma capacidade de atendimento ainda não medida.

## Proposta

Iniciar com uma aplicação Django, organizada por responsabilidades do domínio e com contratos explícitos de services. Manter a coordenação das alterações oficiais dentro dessa aplicação. A [arquitetura](../arquitetura.md) apresenta áreas lógicas para discutir propriedade dos dados e dependências.

Isso não define um app para cada área, nome de diretório, esquema físico ou número de processos em produção. Arquivos podem ficar em serviço externo conforme a estratégia futura, sem transformar cada área de negócio em microserviço.

## Alternativas consideradas

- Microserviços desde o início: acrescentam comunicação, implantação e consistência distribuídas antes de existir necessidade demonstrada.
- Aplicação sem separação de responsabilidades: reduz a organização inicial, mas dificulta manter acesso, autorizações e versões coerentes entre áreas.
- Frontend independente e API obrigatória: amplia a superfície de contratos e não é exigência da base com templates confirmada.

As comparações são avaliação técnica desta proposta; não houve experimento ou seleção formal dessas alternativas pela equipe.

## Consequências esperadas

Há menos unidades de implantação e a coordenação no banco tende a ser mais direta. Em contrapartida, a implantação e parte do dimensionamento ficam acopladas; a equipe precisa preservar fronteiras para evitar dependências circulares e concentração indevida em um módulo comum.

Se a carga ou organização da equipe exigir separação futura, será necessário avaliar contratos, dados e custos de migração. Não há promessa de que dividir a aplicação depois será trivial.

## Pendências e verificação futura

A I01 implementou a estrutura mínima de configuração, contas e templates. As decisões restantes de P002 e P003 interferem nos vínculos. P015, P016 e P018 tratam de implantação e capacidade. [Entrega da I01](../entrega-i01.md)

A preparação local foi verificada na I01. Dependências entre áreas e cenários de carga serão verificados quando as funções e suas metas estiverem definidas.
