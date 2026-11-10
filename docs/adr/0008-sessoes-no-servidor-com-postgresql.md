# ADR 0008: Sessões no servidor com PostgreSQL

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** recomendação técnica nova, ainda não aprovada; não é decisão confirmada.
- **Origem:** detalhamento de RF001 e RS004 na [Spec 0002](../specs/0002-autenticacao.md); base de sessão Django confirmada no [ADR 0003](0003-usuario-customizado-e-sessao-django.md).

## Contexto

O produto exige encerrar a sessão corrente e impedir sua reutilização após logout. A escolha de sessão Django está confirmada, mas seu backend e suas políticas continuam em P014/P015 nas [pendências](../pendencias.md). Não basta a interface deixar de mostrar o usuário ou apagar seu cookie: uma cópia anterior do identificador não deve restabelecer a sessão encerrada.

PostgreSQL já é o banco escolhido para a aplicação. Ainda não há implantação, configuração de sessão ou migração executada. Este registro apresenta uma opção concreta para revisão, sem selecionar duração, concorrência ou procedimento de revogação global.

## Recomendação

Usar o backend nativo `django.contrib.sessions.backends.db` com PostgreSQL. Manter apenas o identificador opaco no navegador e a sessão no servidor, sob os mecanismos de login/logout do Django. A implementação futura deverá verificar que logout remove/invalida a sessão corrente e que a chave anterior não permite novo acesso.

Não criar tabela própria de sessão, booleano de revogação ou cópia de permissões para reproduzir o modelo de referência do RS004. Estrutura nativa, migrações e expiração devem ser conferidas na versão escolhida. Essa opção é recomendada por sua compatibilidade com o banco já previsto; não é uma exigência universal do Django.

## Alternativas e razões

| Alternativa | Avaliação para o projeto |
|---|---|
| Sessão nativa em banco | Recomendação: estado no servidor e uso da infraestrutura PostgreSQL já escolhida; permite verificar invalidação da sessão corrente |
| Cookies assinados como único backend de sessão | Não recomendar para este contrato: uma cópia anterior pode ser reapresentada após logout, sem estado equivalente de revogação no servidor |
| Cache ou combinação banco/cache | Possível alternativa futura, mas cache, persistência, perda de estado e operação não foram escolhidos; não introduzir Redis por inferência |
| Backend próprio ou tokens de API | Sem necessidade demonstrada para a base web confirmada; amplia mecanismo e obrigações de manutenção |

As diferenças de persistência e reutilização de cookies assinados são descritas na [documentação oficial de sessões do Django](https://docs.djangoproject.com/en/stable/topics/http/sessions/). O documento apoia a análise, sem escolher a versão do projeto ou aprovar esta recomendação.

## Consequências e limites

O reconhecimento da sessão dependerá do banco e da configuração de conexão. Indisponibilidade deve resultar em falha segura e mensagem operacional, sem afirmar senha incorreta. Será necessário preparar as migrações nativas e definir manutenção de sessões expiradas quando a implementação for autorizada.

Logout da sessão atual não equivale a revogar todos os dispositivos. Prazo, atividade/inatividade, fechamento do navegador, quantidade de sessões, alteração de senha, revogação administrativa, cookies, TLS, proxy, retenção e tratamento de abas permanecem abertos. Também não se promete cancelar requisição já autorizada e em execução.

Não há medição de carga, custo ou desempenho; avaliar conforme P018. A opção proposta não resolve autenticação multifator, recuperação de conta, autorização por ação, proteção de arquivos ou deduplicação de atos de inspeção.

## Aceite e verificação futura

Validar esta recomendação e registrar a escolha antes de configurar o backend. Se a alternativa mudar, revisar os contratos da Spec 0002 que dependem da invalidação no servidor, sem enfraquecer silenciosamente RF001/RS004.

Verificar no PostgreSQL de teste: entrada com sessão reconhecida, renovação da chave, saída, repetição com chave anterior, expiração configurada, conta inativa e falha de persistência no middleware. AU17 a AU24 da Spec 0002 descrevem parte dessas evidências; nenhum cenário foi executado nesta etapa.

Relacionados: [Spec 0001](../specs/0001-fundacao-tecnica.md), [arquitetura](../arquitetura.md), [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md). Este ADR continua Proposto até decisão explícita.
