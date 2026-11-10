# ADR 0005: Autorização contextual por ação

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** registro de restrição confirmada; representação física e autoridades permanecem abertas.
- **Origem:** DC008 a DC013, DC017 e DC020 nas [decisões confirmadas](../decisoes-confirmadas.md); F003 no [índice de fontes](../referencias/README.md).

## Contexto

Há três perfis-base e supervisão atribuída a um fiscal por ação. A equipe pode repetir os participantes e mudar o supervisor entre ações. Estabelecimentos só acessam conteúdo próprio permitido, e atos de cancelamento/correção precisam de autorização.

## Decisão registrada

Verificar no servidor a identidade, o perfil, o vínculo, a situação e o escopo necessários ao ato. Quando a decisão couber ao supervisor, verificar sua designação para a ação correspondente. Essa verificação acompanha consultas, alterações e arquivos e pertence ao caso de uso, independentemente da tela de origem.

Não representar a supervisão apenas como poder global no usuário. Não presumir que administrador, participante da equipe ou fiscal que iniciou uma inspeção pode designar, aprovar ou autoaprovar. O estabelecimento não recebe avaliação em elaboração ao consultar ou enviar documento.

## Alternativas e razões

- Esconder botões sem verificar no servidor: não protege o acesso direto.
- Quarto perfil Supervisor ou booleano global: perde o escopo e a mudança de responsável entre ações.
- Confiar em IDs/perfis enviados pelo navegador: permite confundir entrada com autoridade.
- Usar `is_staff` ou superusuário técnico como autoridade sanitária: mistura administração técnica e decisão de negócio.

As consequências de implementação são análise técnica; não definem tabelas, biblioteca de permissões ou lista de aprovadores.

## Consequências

São necessários vínculos e histórico de designação, além da checagem de permissão simples por perfil. Isso aumenta o cuidado com consultas, downloads e revogação, mas preserva os limites confirmados. Uma autorização antiga não deve sustentar automaticamente um novo ato após perda do vínculo aplicável.

## Pendências e verificação futura

P002 a P006 tratam de representação, ação/inspeção, designação, autoridade e mudanças em andamento. A Etapa 6 detalhará o contrato. Verificar futuramente ações e estabelecimentos distintos, alteração de vínculo, designação revogada e tentativa por acesso direto. Autoridade e autoaprovação continuam sem decisão; não se cria regra para elas neste ADR.

Relacionados: RF002, RF016 a RF019, RF022, RS001, RS002 e RS010 no [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md); [arquitetura](../arquitetura.md).
