# Entrega I08 — Cancelamento autorizado e auditoria

Concluída e verificada em ambiente de demonstração em 16/11/2026. [Spec 0009](specs/0009-cancelamento-e-auditoria.md) · [DC032](decisoes-confirmadas.md#dc032-cancelamento-autorizado-na-i08) · [Trello](https://trello.com/c/7sUzslD1)

## O que foi entregue

O fiscal da equipe solicita o cancelamento de uma inspeção em andamento e informa a justificativa. Outro supervisor ativo e elegível da ação decide. O Administrador decide quando não houver outro supervisor elegível. A autoridade é conferida novamente no momento da decisão.

O pedido pendente bloqueia novas respostas, fotos e documentos, inclusive em abas abertas antes da solicitação. A rejeição libera as operações permitidas para a inspeção. Na aprovação, o servidor registra a decisão e efetiva o cancelamento na mesma transação. Os dois eventos ficam identificados separadamente. Respostas, arquivos, recibos, histórico e a versão do checklist são preservados.

A tela apresenta a confirmação do servidor. Se a resposta se perder, a página aberta repete a mesma operação e recupera o recibo. A repetição permite consultar um envio anterior já confirmado, com autorização atual, sem gravar outro registro.

## Verificação

| Caso | Resultado observado |
|---|---|
| Justificativa, escopo e autoridade | Pedido vazio recusado. Decisão de outra ação, do próprio solicitante ou de supervisor revogado recusada. Administrador atua na ausência prevista. |
| Pedido pendente e rejeição | Novas respostas, fotos e documentos recusados no servidor durante a pendência. Os envios voltam a estar disponíveis após rejeição. |
| Aprovação e concorrência | Uma única efetivação. Falha durante a aprovação reverte a decisão e o efeito. Cancelamento direto sem registro válido é impedido. |
| Auditoria e preservação | Equipe atual da inspeção e Administrador consultam a trilha. A aplicação oferece apenas consulta, e o banco impede edição e exclusão de eventos de inspeção. Respostas e arquivos anteriores ficam disponíveis conforme o acesso. |
| Navegador móvel | Chromium a 360 px confirmou pedido, checklist em leitura, aprovação por supervisor de outra inspeção da mesma ação, recuperação após perda da confirmação e consulta ao histórico. Conferência no PostgreSQL encontrou uma única efetivação e a resposta anterior preservada. |

Suíte local com **86 testes**, dos quais **9** cobrem o cancelamento e a auditoria. Verificações do Django e detecção de migrações passaram. [Preparo e demonstração](../README.md#demonstrar-o-cancelamento)

## Limites do recorte

Na demonstração, cada inspeção tem no máximo um pedido pendente. Justificativa e motivo da decisão são obrigatórios, com até 2.000 caracteres. A auditoria é consultada por inspeção. A fila de pedidos do Supervisor segue o escopo da ação, e a trilha completa exige acesso à inspeção como membro da equipe ou Administrador.

Retenção, auditoria geral e acesso de produção continuam em P017. Autoridade e efeitos da correção seguem em P005/P006. A conclusão será introduzida na I09, e a guarda desta etapa já exige que a inspeção esteja em andamento. [Pendências](pendencias.md) · [Plano de implementação](plano-implementacao.md)
