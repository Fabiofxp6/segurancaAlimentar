# Spec 0013 — Consultas e indicadores

I12 de demonstração para RF024, RF026, RS001 e RS009 conforme [DC036](../decisoes-confirmadas.md#dc036-consultas-e-indicadores-na-i12). A lista usa o escopo de inspeção da I05. O painel usa a revisão mais recente conforme I11. [Escopo de acesso](0003-acesso-vinculos-supervisao.md) · [Revisões](0012-correcao-e-retificacao.md)

## Consultas

| Tela | Acesso | Resultado |
|---|---|---|
| `GET /inspecoes/` | Administrador ou fiscal ativo da equipe da inspeção | Lista e total com os filtros aplicados. Paginação de 25 registros em ordem decrescente de ID. |
| `GET /inspecoes/indicadores/` | Administrador | Contagens por situação, resultados por versão e regra e irregularidades mais frequentes. |

Designação de supervisor mantém suas permissões nas operações da ação. A lista geral do fiscal continua vinculada às inspeções em que integra a equipe. As opções de estabelecimento e fiscal são obtidas do conjunto que o usuário pode consultar. O filtro de fiscal inclui responsável e participantes. O portal do estabelecimento segue seu fluxo de resultados e termos liberados.

| Filtro GET | Validação |
|---|---|
| `estado` | Opcional. Aceita os estados da inspeção. |
| `estabelecimento` e `fiscal` | Opcionais. IDs inteiros pertencentes às opções no escopo autorizado. |
| `inicio` e `fim` | Opcionais. Datas ISO ou dd/MM/yyyy; extremidades inclusive pela criação da inspeção no fuso do sistema. Início até fim. |
| `pagina` | Opcional na lista. Inteiro positivo. Navegar conserva os filtros; o formulário de filtros volta à primeira página. |

Entrada inválida retorna 400 com mensagem e sem consulta de resultado. Para uma página positiva acima da última, a lista usa a última página disponível. Toda consulta filtra o escopo antes de aplicar os parâmetros. A etapa entrega consultas e relatório na interface. Formatos de exportação e parâmetros de produção permanecem em P022/P018.

## Indicadores

- **Inspeções por situação.** Cada inspeção da consulta conta uma vez, inclusive quando o fiscal filtrado é o responsável ou integra a equipe com outros participantes.
- **Resultados por versão.** Usa somente inspeções concluídas e a revisão mais recente. Agrupa pela identidade da versão do checklist e pela regra de pontuação. Exibe quantidade, contagens por classificação e média dentro de cada grupo. Resultado Sem pontuação integra a contagem e fica fora da média.
- **Irregularidades mais frequentes.** Conta descrições de irregularidade não vazias da revisão válida de inspeções concluídas, uma vez por item e inspeção. Agrupa por versão e item e mostra até dez grupos em ordem de frequência. A revisão inicial usa os registros de campo fechados. A revisão corrigida usa os valores confirmados dessa revisão. O painel mostra o enunciado do item e a quantidade.

Verificar filtros combinados, datas inclusivas, opções do escopo do fiscal, revogação de equipe, paginação e exibição sem resultados. Conferir o painel com duas versões, resultado sem pontuação e correção que altera o resultado e a frequência. Verificar acesso direto fora do perfil. As métricas e a comparação entre versões para produção seguem em P010/P022. [Agregação no Django](https://docs.djangoproject.com/en/5.2/topics/db/aggregation/)
