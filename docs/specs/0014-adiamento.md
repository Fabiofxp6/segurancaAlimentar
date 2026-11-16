# Spec 0014 — Adiamento de inspeção atribuída

**Escopo confirmado para a I14 local.** O RF027 permite ao fiscal ativo da equipe pedir o reagendamento de uma inspeção Atribuída, antes de começar. Requer justificativa e data proposta. Outro supervisor ativo e elegível da ação decide. O Administrador decide se faltar outro elegível. A aprovação mantém Atribuída, grava a nova data e conserva a tela de início existente. [DC038](../decisoes-confirmadas.md#dc038-adiamento-e-reanálise-na-i14) · [RF027](../prd/0001-sistema-avaliacao-seguranca-alimentar.md#rf027-solicitar-adiamento-da-fiscalização)

## Contrato local

- `Inspecao.agendada_em` guarda a próxima data e hora aprovadas, inicialmente vazia. A data real do início continua no campo próprio. A primeira aprovação não pressupõe data anterior.
- `PedidoAdiamento` guarda inspeção, fiscal, data e hora propostas no fuso de Maceió, justificativa, situação, chaves UUID de operação e horário de solicitação. A decisão acrescenta autor, designação quando aplicável, motivo e horário. As justificativas de demonstração têm até 2.000 caracteres, conforme o padrão da correção. A data proposta deve ser futura e posterior à data já agendada, quando houver. A aprovação exige que a proposta ainda esteja no futuro.
- Na demonstração, um pedido pendente impede o início. Após aprovação, o fiscal responsável usa a tela atual a partir da data agendada. Rejeição mantém a data vigente. Nada impede a consulta ou o recebimento de documentos já permitido enquanto Atribuída.
- A transação bloqueia a ação e a inspeção antes da decisão. A solicitação e o início bloqueiam a mesma inspeção. Um pedido pendente por inspeção e confirmação com a mesma chave evitam efeito duplicado. A auditoria registra pedido, decisão e, quando aprovada, data anterior e nova.
- A partir do detalhe da inspeção, a página **Adiamento** mostra a data, os pedidos e a decisão. A lista interna permite que o supervisor encontre pedidos em outras inspeções da sua ação. POSTs exigem sessão, CSRF e o contexto da tela. Respostas 400 indicam entrada inválida e 409 indicam disputa de estado ou reaproveitamento de chave com outro conteúdo.

## Aceite

Verificar solicitação e aprovação sem mudar o estado, rejeição com data preservada, início bloqueado durante pendência e antes da data, início pela tela existente após a data, expiração da proposta, autoaprovação negada, alternativa administrativa e repetição idempotente. O checklist só é fixado no início, conforme a I05.
