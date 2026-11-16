# Entrega I12 — Consultas e indicadores

Verificada em ambiente de demonstração em 16/11/2026. [Spec 0013](specs/0013-consultas-e-indicadores.md) · [DC036](decisoes-confirmadas.md#dc036-consultas-e-indicadores-na-i12) · [Trello](https://trello.com/c/SAjKk3dG)

## Fluxo entregue

A lista interna permite combinar situação, estabelecimento, fiscal responsável ou participante e período pela data de criação. Cada página mostra até 25 inspeções. O fiscal vê as inspeções da sua equipe atual e as opções de filtro desse conjunto. O Administrador pode consultar as inspeções de demonstração. O servidor refaz a autorização a cada consulta.

O Administrador pode abrir **Indicadores de inspeção** na lista. O painel mostra totais por situação e resultados de inspeções concluídas pela revisão mais recente. As médias ficam separadas por versão do checklist e regra e excluem resultados sem pontuação. As dez maiores frequências contam irregularidades descritas por item e versão, uma vez por inspeção concluída. O painel exibe enunciados e quantidades.

## Verificação

| Cenário | Resultado |
|---|---|
| Filtros e escopo | Combinação de filtros e limites inclusivos de datas verificados. Datas inválidas, página não positiva e valores fora do escopo retornam erro. Remover o fiscal da equipe remove o acesso na mesma sessão. |
| Paginação | Páginas de 25, sem duplicar inspeções com vários participantes. Próxima e Anterior preservam filtros. |
| Indicadores | Base fictícia com seis inspeções confirmou os totais. A revisão mais recente substituiu a anterior no cálculo. Médias de 40,00% e 90,00% apareceram em grupos separados. Resultado sem pontuação contou no grupo. Irregularidade de inspeção em andamento ficou fora. |
| Navegador móvel | Chromium a 360 px confirmou paginação, filtros, médias separadas, filtro de unidade e negativa de acesso direto ao painel pelo fiscal. |

**116 testes** passaram no PostgreSQL, incluindo seis de consultas e indicadores. O check do Django e a verificação de migrações passaram. [Como demonstrar](../README.md#demonstrar-consultas-e-indicadores)

## Limites da demonstração

O período usa a criação da inspeção no fuso configurado pelo sistema. Escolhi 25 registros por página e até dez grupos de irregularidade por consulta. O relatório é consultável na interface. Exportações, comparação oficial entre versões e metas de desempenho permanecem em P022/P010/P018. [Pendências](pendencias.md) · [Plano](plano-implementacao.md)
