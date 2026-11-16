# Entrega I11 — Correção autorizada, recálculo e retificação

Verificada em ambiente de demonstração em 16/11/2026. [Spec 0012](specs/0012-correcao-e-retificacao.md) · [DC035](decisoes-confirmadas.md#dc035-correção-e-retificação-na-i11) · [Trello](https://trello.com/c/agcLQc1S)

## Fluxo entregue

O fiscal da equipe solicita a correção de um item de uma inspeção concluída. O pedido registra justificativa, revisão e valores anteriores e propostos. Decide outro supervisor ativo da ação ou, na ausência de outro elegível, o Administrador. O fiscal solicitante ainda ativo na equipe ou o Administrador aplica a mudança aprovada em uma operação separada.

A aplicação grava revisão, executor e data. O servidor recalcula pela versão original do checklist e preserva a nota anterior, a classificação anterior e os registros de campo. A tela interna mostra as revisões e os dados de cada pedido. A inspeção permanece Concluída.

Quando uma correção muda os dados impressos de um termo emitido, o servidor gera o retificador na mesma transação. O PDF identifica a versão anterior. A justificativa e a decisão seguem na trilha interna. O estabelecimento consulta cada PDF liberado. A versão anterior continua disponível após a nova liberação.

## Verificação

| Cenário | Resultado |
|---|---|
| Autoridade e escopo | Negativas para pedido pendente ou rejeitado, autoaprovação, supervisor revogado, ator fora do escopo e tentativa de aplicação por fiscal sem permissão. |
| Recálculo e guarda | Regras originais mantidas após publicar novo checklist. Pedidos concorrentes sobre a mesma base produziram uma revisão. A base, o pedido e a decisão ficaram preservados. |
| Retificação | Original recuperável com os mesmos bytes. Retificador vinculado à nova revisão. Falha na geração reverteu aplicação e retificador e preservou a aprovação. Observação interna sem efeito no PDF gerou revisão sem nova emissão. |
| Navegador móvel | Chromium a 360 px confirmou pedido, decisão, aplicação recuperada após perda da resposta, bloqueio do retificador antes da liberação e download após nova liberação. A nota do cenário mudou de 80,00% para 0,00%. |
| PDF e migração | Revisão visual e de texto do retificador baixado. Migração em banco isolado com versão anterior preservou resultado inicial, datas, liberação e bytes do termo existente. |

**110 testes** passaram na suíte PostgreSQL, incluindo oito de correção e retificação. O check do Django e a detecção de migrações passaram. [Como demonstrar](../README.md#demonstrar-correção-e-retificação)

## Limites da demonstração

Um pedido altera a resposta, a observação ou a irregularidade de um item. Uma correção de observação interna pode criar revisão com a mesma nota. O portal identifica a versão mais recente liberada e mantém o histórico das versões liberadas. Correção documental, novos anexos após conclusão, reanálise e regras oficiais permanecem nos recortes correspondentes. [Pendências](pendencias.md) · [Plano](plano-implementacao.md)
