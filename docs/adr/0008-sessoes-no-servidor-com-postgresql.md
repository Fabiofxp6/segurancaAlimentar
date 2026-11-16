# ADR 0008: Sessões no servidor com PostgreSQL

- **Status:** Aceito para a I02 em 15/11/2026.
- **Data:** 2026-11-10.
- **Decisão registrada:** DC026. [Entrega da I02](../entrega-i02.md).
- **Origem:** detalhamento de RF001 e RS004 na [Spec 0002](../specs/0002-autenticacao.md); base de sessão Django confirmada no [ADR 0003](0003-usuario-customizado-e-sessao-django.md).

## Contexto

O produto exige encerrar a sessão corrente e impedir sua reutilização após logout. Uma cópia anterior do identificador deve perder o acesso após a saída. As políticas complementares continuam em P014/P015 nas [pendências](../pendencias.md).

PostgreSQL é o banco adotado pela aplicação e já inclui as migrações nativas de sessão no ambiente local.

## Decisão

Usar o backend nativo `django.contrib.sessions.backends.db` com PostgreSQL. Manter apenas o identificador opaco no navegador e a sessão no servidor, sob os mecanismos de login/logout do Django. O teste de saída verifica a exclusão da sessão corrente no PostgreSQL e a recusa no acesso seguinte com a chave anterior.

Não criar tabela própria de sessão, booleano de revogação ou cópia de permissões para reproduzir o modelo de referência do RS004. A estrutura nativa e o efeito da expiração foram conferidos na versão local. A escolha reutiliza o PostgreSQL adotado pelo projeto.

## Alternativas e razões

| Alternativa | Avaliação para o projeto |
|---|---|
| Sessão nativa em banco | Adotada pela I02. Persiste o estado no servidor e permite invalidar a sessão corrente no PostgreSQL. |
| Cookies assinados como único backend de sessão | Não recomendar para este contrato: uma cópia anterior pode ser reapresentada após logout, sem estado equivalente de revogação no servidor |
| Cache ou combinação banco/cache | Possível alternativa futura, mas cache, persistência, perda de estado e operação não foram escolhidos; não introduzir Redis por inferência |
| Backend próprio ou tokens de API | Sem necessidade demonstrada para a base web confirmada; amplia mecanismo e obrigações de manutenção |

As diferenças de persistência e reutilização de cookies assinados são descritas na [documentação oficial de sessões do Django](https://docs.djangoproject.com/en/stable/topics/http/sessions/). A I01 registra as versões verificadas no projeto.

## Consequências e limites

O reconhecimento da sessão dependerá do banco e da configuração de conexão. Indisponibilidade deve resultar em falha segura e mensagem operacional, sem afirmar senha incorreta. A implantação remota deverá aplicar as migrações existentes e definir a manutenção de sessões expiradas.

Logout da sessão atual não equivale a revogar todos os dispositivos. Prazo, atividade/inatividade, fechamento do navegador, quantidade de sessões, alteração de senha, revogação administrativa, cookies, TLS, proxy, retenção e tratamento de abas permanecem abertos. Também não se promete cancelar requisição já autorizada e em execução.

Não há medição de carga, custo ou desempenho; avaliar conforme P018. Autenticação multifator, recuperação de conta, autorização por ação, proteção de arquivos e deduplicação de atos de inspeção seguem nos seus recortes.

## Verificação

A I02 verificou em PostgreSQL a entrada com sessão reconhecida, rotação da chave, saída, recusa da chave encerrada, expiração e conta inativa. Também verificou a resposta a uma falha de persistência simulada no middleware. Os limites e cenários da Spec 0002 estão no [registro da I02](../entrega-i02.md).

Relacionados: [Spec 0001](../specs/0001-fundacao-tecnica.md), [arquitetura](../arquitetura.md), [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md).
