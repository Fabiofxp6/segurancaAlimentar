---
name: django-boas-praticas
description: Especificar, implementar ou revisar Django/PostgreSQL do sistema alimentar, incluindo views, forms, services, identidade, sessão e acesso. Use no recorte autorizado dessas camadas, preservando contratos e políticas ainda abertas.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Django e PostgreSQL

Consultar [estado](../../../docs/state.md), [arquitetura](../../../docs/arquitetura.md), [decisões](../../../docs/decisoes-confirmadas.md) e [pendências](../../../docs/pendencias.md), lendo apenas a spec aplicável:

| Trabalho | Referência principal |
|---|---|
| Configuração, PostgreSQL, usuário inicial e primeiras migrações | [Spec 0001](../../../docs/specs/0001-fundacao-tecnica.md), P001/P002 |
| Login, logout, form, redirecionamento, sessão e falhas | [Spec 0002](../../../docs/specs/0002-autenticacao.md), P014/P015/P020 |
| Perfil-base, vínculos, supervisão, consultas e revogação | [Spec 0003](../../../docs/specs/0003-acesso-vinculos-supervisao.md), P002–P006 |

As três specs permanecem Propostas. Confirmar a origem da escolha antes de transformar candidato em código/configuração. Conferir documentação oficial na versão efetivamente escolhida quando uma API depender dela; esta skill não seleciona versões, driver ou ferramenta de ambiente.

## Camadas e exceções nativas

- Views próprias herdam diretamente de `View`, com mixins de acesso admitidos. Não substituir por subclasses de `LoginView`, `LogoutView` ou `FormView` por conveniência; não reescrever as views internas do Django/Admin.
- Services concentram regras, autorização e ORM explícito da aplicação; não recebem `request` nem retornam `HttpResponse`. Forms validam entrada; templates apresentam; models representam persistência/restrições sem esconder atos oficiais em `save()`/signals.
- Consultas internas do framework em autenticação, sessão, permissões, `ModelForm`, Admin e migrações são exceções admitidas ao ORM centralizado. Elas não autorizam consultas explícitas de negócio em views/forms nem gravações que contornem o service.
- Login/logout nativos ligados à sessão ficam na view. A proposta de `AuthenticationForm` recebe `request` legitimamente; não criar `AuthService` para eliminar essa exceção nem reimplementar senha. O form/backend candidatos continuam sujeitos à Spec 0002.
- Admin utiliza os mesmos casos de uso para atos de negócio. Evitar edição/exclusão direta e segunda gravação automática que ignore autorização, história ou versões. As flags técnicas do Admin não são perfil sanitário.

## Fundação e identidade

- Usar PostgreSQL, sem fallback para SQLite. Falta de conexão, driver ou variável não autoriza criar outro banco ou assumir sucesso. Configurações inválidas falham sem expor valores secretos.
- Preservar arquivos de ambiente existentes. Sua presença não implica carregamento automático; ferramenta, configuração e valores reais dependem da fundação/ambiente aprovados.
- A base confirmada é usuário customizado `AbstractUser`, nome de usuário/senha e sessão Django. Resolver P001/P002 e a configuração do usuário antes da primeira migração correspondente. Referenciar o modelo configurado, sem um segundo cadastro de identidade.
- O nome `contas.Usuario`, chave física, campos, cardinalidades e estrutura de apps continuam candidatos. Dados lógicos de RS003/RS004 não criam colunas/tabelas paralelas de hash ou sessão.
- Sessão Django é confirmada; backend em banco é recomendação do [ADR 0008](../../../docs/adr/0008-sessoes-no-servidor-com-postgresql.md), ainda Proposto. Não assumir prazo, tentativas, cookies, concorrência ou revogação global por defaults.

## Acesso e consultas

- Distinguir identidade, perfil-base, vínculo e designação contextual. Supervisor é fiscal designado por ação, sem quarto perfil/booleano global. Participação, início direto, `is_staff`, superusuário ou `has_perm()` isolado não concedem autoridade de negócio.
- Obter ator confiável no servidor e validar escopo no service que produz o efeito. Não aceitar poder/ator do navegador nem usar uma checagem de tela como autorização reutilizável para o POST.
- Filtrar listas, contagens, detalhes e referências de arquivos pelo conjunto acessível. Não carregar dados globais para esconder depois no template. Preparar dados de apresentação e avaliar N+1/índices com consultas reais, sem impor otimização antecipada.
- Revalidar perfil, vínculo, vigência e estado após alteração/revogação, inclusive na sessão já aberta e antes da efetivação. Cache de autorização precisa de invalidação definida; não congelar a designação no login.
- Autoridades, autoaprovação, agrupamento ação/inspeção e quantidade de supervisores continuam em P003–P006. Não escolher um modelo ou conceder poder para contornar uma política indefinida.

## Consistência e validação

Coordenar alterações dependentes e história obrigatória no caso de uso. `atomic` sozinho não resolve disputa concorrente; mecanismo e restrições seguem schema/política aprovados. Não impor unicidade de supervisor por ação antes de P004, nem usar lote, SQL, signals ou `save()` como atalho. Preservar migrações aplicadas e história; não recriar banco por rotina.

Banco e arquivo externo não são automaticamente atômicos. Preservar checklist/regras iniciais, resultados e termos emitidos. Confirmação perdida/reenvio precisa evitar outro efeito oficial; botão desabilitado e redirecionamento não bastam. P016/P020 e specs funcionais escolherão o mecanismo. Não instalar fila, Redis, API, JWT ou biblioteca de permissões por inferência.

Usar PostgreSQL isolado nos testes de persistência pertinentes. Verificar VF/AU/AC e a [matriz](../../../docs/matriz-rastreabilidade.md) conforme a função existir, com a [skill de testes](../testes/SKILL.md). Falha ao persistir sessão pode ocorrer no middleware depois da view; verificar a resposta e o acesso seguinte, não apenas o retorno da função de login.

Relatar evidências reais, preservar o recorte documental quando esse for o pedido e atualizar o [Trello](../../../docs/acompanhamento-trello.md). Origem: [curadoria](../../../docs/curadoria-skills-agentes.md). Revisão integrada: [Etapa 7](../../../docs/revisao-skills-tecnicas.md).
