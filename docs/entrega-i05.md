# I05 — Atribuição, início e supervisão

Entrega local em 16/11/2026. Uma ação pode agrupar várias inspeções. O Administrador pode designar vários fiscais ativos da equipe simultaneamente. A designação é opcional e vigora no momento em que é gravada. [Decisão DC029](decisoes-confirmadas.md#dc029-ações-e-supervisão-na-i05) · [Spec 0006](specs/0006-inicio-equipe-e-supervisao.md)

## Fluxo entregue

- O Administrador atribui uma inspeção, informa equipe e pode reutilizar uma ação existente. O fiscal responsável pode iniciar a inspeção atribuída. O fiscal ativo também pode iniciar diretamente, criando uma ação própria. Os dois caminhos preservam origem e autoria.
- No início, o servidor fixa a última versão de demonstração publicada do checklist escolhido e guarda nome e documento da unidade. Uma publicação nova ou alteração cadastral da unidade deixa intacta a base da inspeção anterior. O PostgreSQL protege a referência e os demais dados originais de início.
- A supervisão tem escopo de ação. O servidor verifica a designação e a elegibilidade atual em cada requisição. Encerrar a designação retira a função na sessão já aberta. A perda de toda participação na ação encerra a designação e preserva o histórico. A gestão da equipe conserva o autor original do início e das atribuições.
- A criação com a mesma chave e os mesmos dados recupera o registro. Dados incompatíveis com a chave retornam conflito. O início atribuído usa bloqueio de linha e registra uma vez. As gravações incluem o histórico na mesma transação.

## Verificações

- **59 testes** passaram no PostgreSQL isolado, incluindo 11 da I05. Verificados agrupamento, permissões, acesso indevido por URL, dois caminhos de início, concorrência, falha simulada, histórico, proteção da versão e revogação contextual.
- No Chromium a 360 px, foram conferidos atribuição, designação simultânea de dois fiscais, início atribuído e direto e retirada da designação na sessão corrente.

## Limites

O fluxo de demonstração está habilitado nos perfis de desenvolvimento e teste. As regras e o conteúdo oficiais continuam em P009. A autoridade para aprovar pedidos, incluindo pedido do próprio Supervisor, depende de P005. Respostas, evidências e retentativa automática seguem para a I06.

Escolhas do recorte local incluem criação de ação própria no início direto, início da atribuída pelo fiscal responsável e seleção automática da última publicação de demonstração do checklist escolhido. A elegibilidade de inspeções reais depende da futura política de publicação, da escolha do checklist aplicável e das regras operacionais.

[Como testar](../README.md#demonstrar-inspeções-no-ambiente-local) · [Cartão da I05](https://trello.com/c/OfaYG9v0)
