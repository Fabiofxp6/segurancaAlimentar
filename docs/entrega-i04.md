# I04 — Checklist e versões

Fluxo local de checklist verificado em 15/11/2026. Cobre a manutenção e publicação de demonstração do RF004 e prepara a versão que a I05 deverá associar ao início da inspeção em RF007.

## Entrega

- O Administrador ativo abre **Gerir checklists** para criar e editar rascunhos, cadastrar e remover itens e consultar versões publicadas. Pode configurar enunciado, ordem, opções de resposta, peso opcional e obrigatoriedade.
- A publicação exige pelo menos um item. Cada versão guarda seu próprio título, referência, regras e itens, além de número, autor, data e finalidade de demonstração.
- Uma publicação posterior preserva a anterior. Edição e exclusão de versão publicada são recusadas pelo PostgreSQL. O rascunho continua editável e sua revisão protege contra sobrescrita por uma tela antiga.
- Repetir a publicação da mesma revisão recupera a versão existente. Duas solicitações concorrentes da mesma revisão recebem a mesma referência sem gravar duas versões.

## Verificações

- **48 testes** passaram no PostgreSQL isolado, incluindo 9 da I04. Cobertura de validações de dados, acesso por perfil, CSRF, conflito de revisão, concorrência e falha simulada de persistência.
- Verificados por consulta os dados originais após uma segunda publicação, incluindo regras, opções, peso, título e autoria. Testes diretos confirmaram a recusa de edição e exclusão da versão antiga e a restrição à finalidade de demonstração.
- No Chromium a 360 px, foram conferidos criação do rascunho, navegação por teclado, publicação de duas versões e consulta da regra preservada na primeira.

## Continuidade

O conteúdo sanitário oficial e a autoridade para publicá-lo continuam em P009. A fórmula, pesos oficiais, arredondamento e tratamento de “Não se aplica” continuam em P010. O peso informado é guardado como texto decimal exato no conteúdo da versão. O fluxo local serve à demonstração com dados fictícios.

A I05 deverá guardar a referência à versão escolhida no início da inspeção. A verificação de ponta a ponta do RF007 depende desse vínculo. O tratamento geral de reconexão de formulários segue em P020, com repetição de publicação já coberta nesta etapa.

[Spec 0005](specs/0005-checklist-e-versoes.md) · [Como testar localmente](../README.md#demonstrar-o-checklist-no-ambiente-local) · [Cartão da I04](https://trello.com/c/hRV4arE6)
