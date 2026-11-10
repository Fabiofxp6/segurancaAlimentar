# ADR 0001: Python com Django e PostgreSQL

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** registro de escolha já confirmada; o status documental não reabre essa escolha.
- **Origem:** DC003 e DC004 nas [decisões confirmadas](../decisoes-confirmadas.md); F003, F005 e F008 no [índice de fontes](../referencias/README.md).

## Contexto

O sistema precisa de aplicação web para tablets e celulares, persistência oficial, acesso controlado e preservação de relações e histórico. O usuário substituiu Java por Python com Django e manteve PostgreSQL. As versões e o ambiente ainda não foram definidos.

## Decisão registrada

Usar Python com Django e PostgreSQL. Hospedar o sistema remotamente ou em nuvem, sem escolher fornecedor nesta etapa. O blog fornece referência documental e de organização; seu SQLite não será herdado como banco do projeto alimentar.

## Alternativas e razões

- Java: escolha anterior substituída por instrução do usuário; não volta a ser opção vigente por existir em cartão antigo.
- SQLite da referência: pertence ao contexto do blog; não substitui a escolha explícita de PostgreSQL.
- Outro framework Python ou outra base: não existe decisão que autorize essa troca.

A análise técnica identifica conveniência em aproveitar autenticação, formulários, ORM e templates do Django e concentrar os registros relacionais no PostgreSQL. Essa é uma avaliação desta documentação, não uma justificativa atribuída ao usuário ou resultado de comparação experimental.

## Consequências

A equipe precisa preparar e manter um ambiente Python/Django com PostgreSQL, incluindo configuração, migrações e recuperação. Há custo de operação do banco e de acompanhamento das versões. O uso do framework não resolve sozinho autorização contextual, rede intermitente ou coordenação de arquivos.

Não há migração do banco do blog prevista. Versões serão escolhidas pela compatibilidade e suporte, sem copiar as da referência.

## Pendências e verificação futura

P001 trata de versões; P015 de hospedagem/operação; P018 de capacidade e recuperação. Na Etapa 4, especificar preparação reproduzível e validações da fundação; a execução virá em fase autorizada posterior. Não há ambiente instalado ou teste de aplicação executado neste ADR.

Relacionados: RNF05, RNF09, RNF11 e RNF12 no [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md); [arquitetura](../arquitetura.md).
