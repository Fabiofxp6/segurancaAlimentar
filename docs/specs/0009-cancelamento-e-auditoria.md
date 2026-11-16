# Spec 0009 — Cancelamento e auditoria

I08, com RF022, RF023, RS001, RS002, RS007 e RS013. Pedidos, decisões, efetivação e eventos mantêm autoria e contexto. [DC032](../decisoes-confirmadas.md) · [Spec 0006](0006-inicio-equipe-e-supervisao.md)

## Solicitação e decisão

| Operação | Quem pode | Efeito |
|---|---|---|
| Solicitar | Fiscal ativo da equipe da inspeção em andamento | Registra justificativa, solicitante e data. A inspeção segue em andamento, com resposta, foto e documento novos bloqueados durante a pendência. |
| Rejeitar | Outro supervisor ativo e elegível da ação ou Administrador quando não houver outro supervisor elegível | Registra decisor, motivo, instante e designação quando aplicável. Retoma os registros permitidos pelo estado da inspeção. |
| Aprovar | Mesma regra de autoridade da rejeição | Registra a decisão. O servidor efetiva automaticamente na mesma transação, em evento separado. A inspeção muda para Cancelada. |
| Consultar | Administrador e equipe atual da inspeção. Supervisor elegível da ação pode consultar os pedidos da ação. | Mostra situação, autoria, justificativa, decisão, motivo e datas no escopo interno. |

O solicitante nunca decide o próprio pedido. A elegibilidade de supervisores combina perfil, conta ativa, vínculo atual à equipe da ação e designação aberta. A ausência é calculada excluindo o solicitante. O Administrador que decide por ausência de outro supervisor fica identificado como autoridade alternativa. Equipe e designação são verificadas no servidor antes da decisão.

O servidor permite um pedido pendente por inspeção. Rejeitar preserva o pedido e permite nova solicitação com justificativa. Uma decisão válida só se aplica ao próprio pedido. O cancelamento preserva a versão do checklist, respostas, evidências, documentos e autores. Em Cancelada, equipe consulta o material confirmado e a trilha interna. Novas gravações de campo e documentos ficam fechadas.

## Consistência e perda de conexão

Cada comando tem identificador para retentativa. A mesma operação confirmada recupera o recibo. Dados divergentes com a mesma chave recebem conflito. A transação bloqueia ação e inspeção para serializar decisões, revogação de designação e registros concorrentes. A aprovação e a efetivação aparecem como eventos distintos, gravados atomicamente. Falha reverte ambas.

A tela exige confirmação do servidor. A retentativa reutiliza o controle em memória da I06. Um envio já confirmado antes do pedido ou do cancelamento pode recuperar seu recibo, com autorização atual. O acesso a documentos do estabelecimento segue o vínculo da unidade. A justificativa, o motivo e o histórico do cancelamento são internos.

## Trilha e limites

A consulta da inspeção reúne atribuição, início, equipe, designações da ação, respostas, fotos, documentos e cancelamento. Mostra ator, fonte, evento e data. O PostgreSQL protege os eventos de inspeção e os recibos de campo contra alteração ou exclusão. A trilha da I08 é paginada e segue o escopo interno da inspeção.

Justificativa e motivo são obrigatórios e limitados a 2.000 caracteres no recorte local. A operação de cancelamento parte de Em andamento. A conclusão é tratada na I09 e a política de correção após conclusão continua no seu recorte. Retenção, auditoria geral e acesso de produção permanecem em P017. [Django, transações](https://docs.djangoproject.com/en/5.2/topics/db/transactions/) · [PostgreSQL, gatilhos](https://www.postgresql.org/docs/17/sql-createtrigger.html)
