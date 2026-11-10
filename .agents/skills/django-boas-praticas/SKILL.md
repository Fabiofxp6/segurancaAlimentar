---
name: django-boas-praticas
description: Implementar ou revisar Django, PostgreSQL, models, ORM, services, views e Admin do sistema alimentar. Use em mudanças autorizadas dessas camadas; seguir as decisões e a versão do projeto, sem importar os padrões genéricos dos exemplos externos.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Django e PostgreSQL

Ler [arquitetura](../../../docs/arquitetura.md), spec pertinente, [decisões](../../../docs/decisoes-confirmadas.md) e [pendências](../../../docs/pendencias.md). A [spec de fundação](../../../docs/specs/0001-fundacao-tecnica.md) permanece Proposta, com versões, identidade e estrutura sujeitas à validação. Conferir documentação oficial compatível com a versão escolhida quando houver dúvida ou recurso específico de versão.

## Camadas e entradas

- Views próprias derivam diretamente de `View`; mixins de acesso são admitidos. Elas coordenam HTTP, forms, chamada do service e resposta.
- Services fazem regras e ORM explícito da aplicação, verificando ator, vínculo, escopo e estado. Não recebem `request` nem retornam resposta HTTP.
- Forms validam entrada; models representam persistência e restrições; templates apresentam. As exceções internas do framework e login/logout de sessão seguem a arquitetura.
- Admin usa os mesmos casos de uso para atos de negócio. Não permitir edição, exclusão em lote ou gravação automática posterior que ignore autorização, versão ou auditoria.

## Identidade e autorização

Usar a base customizada `AbstractUser` e sessão já confirmadas. Antes de gerar a primeira migração, resolver os bloqueios de P001/P002 e configurar o usuário escolhido. Referências futuras respeitam o modelo configurado, sem acoplamento ao usuário padrão.

Não confundir perfil de negócio com `is_staff` ou superusuário técnico. Supervisor é designação por ação; conhecer um ID ou participar da equipe não concede autoridade. Não adicionar JWT, API REST/GraphQL ou biblioteca de permissões como requisito implícito.

## Consultas, concorrência e integridade

Preparar consultas no service e controlar carregamentos usados pela apresentação. Usar dados e consultas reais para avaliar N+1, relacionamentos, paginação e índices. `select_related` e `prefetch_related` são opções a avaliar conforme o relacionamento, não regras aplicáveis a toda consulta.

Coordenar escritas dependentes no caso de uso e detectar conflito sem sobrescrita silenciosa. Escolher revisão, bloqueio ou restrições conforme a spec; não presumir que `atomic` sozinho impede toda condição de corrida. Verificar autorização aplicável ao efetivar a mudança.

Não usar `update`, operação em lote, SQL direto, signal ou `save()` como caminho alternativo para ignorar invariantes. Migrações e exclusões preservam a história necessária; não recriar banco nem editar migração aplicada sem plano adequado.

Preservar a base original de checklist, resultados e termos. Arquivo externo não se torna atômico com a transação do banco. Retentativa precisa tratar gravação confirmada com resposta perdida, sem efeito duplicado. A solução concreta continua na spec pertinente.

Usar PostgreSQL nos testes de persistência correspondentes, com destino isolado. Não introduzir fallback para SQLite, Redis, filas, replicas ou otimização estrutural sem necessidade demonstrada e decisão compatível. Verificar comportamento com a [skill de testes](../testes/SKILL.md) e registrar o resultado no [Trello](../../../docs/acompanhamento-trello.md).

Origem e adaptações: [registro da curadoria](../../../docs/curadoria-skills-agentes.md).
