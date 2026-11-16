# I02 — Autenticação e sessão

Verificada localmente em 15/11/2026, com PostgreSQL isolado. A etapa cobre a entrada, o reconhecimento da identidade e a saída da sessão corrente do RF001. As políticas de acesso e operação ainda abertas constam nas [pendências](pendencias.md).

## Fluxo entregue

| Rota | Métodos do fluxo | Comportamento |
|---|---|---|
| `/conta/entrar/` | GET, POST | Valida usuário e senha de conta ativa. Usa mensagem genérica para senha errada, conta inexistente ou inativa. Mantém apenas destinos permitidos e retorna à página protegida por padrão. |
| `/conta/acesso/` | GET | Exibe o usuário conectado e a ação Sair. Sessão ausente, expirada ou inválida redireciona para a entrada. |
| `/conta/sair/` | POST | Exige token CSRF. Exclui no servidor a sessão corrente e volta à entrada. |

A etapa reutiliza `contas.Usuario`, o backend de autenticação e o formulário do Django. O usuário é identificado pelo servidor, usando a sessão no PostgreSQL. A duração e a renovação seguem os padrões técnicos do Django no ambiente local. O perfil de produção configura cookies de sessão e CSRF com `Secure`, e o cookie de sessão usa `HttpOnly`. A verificação no ambiente remoto depende de P015. [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md)

As páginas de conta sinalizam falhas operacionais reconhecidas de banco com HTTP 503. O envio com CSRF rejeitado recebe HTTP 403 e oferece retorno à entrada. As respostas de conta desabilitam cache, e os diagnósticos configurados preservam o status sem registrar senha, token ou detalhes de conexão.

## Evidências

- **PostgreSQL isolado:** 15 testes executados, com 12 testes de autenticação e os 3 da fundação. Foram usados dados fictícios e o banco descartável é removido pelo executor.
- **Chromium, largura de 360 px:** conferidos foco e navegação por Tab, mensagem de erro sem reposição da senha, entrada válida, acesso protegido, saída e recusa no acesso seguinte.
- **Esquema:** usa as migrações já presentes da fundação, incluindo a tabela de sessão nativa. Nenhuma migração nova foi necessária.

| Referência da Spec 0002 | Evidência e alcance |
|---|---|
| AU01–AU13 | Respostas do formulário, limite de usuário, preservação da senha digitada, autenticação, destino permitido, identidade atual e CSRF. |
| AU14 | Rotação do token e recusa do token antigo verificadas por HTTP. O cenário visual em duas abas segue para a validação de navegador. |
| AU15–AU22 | Proteção da página, usuário identificado, expiração, inatividade e saída. A tentativa com a chave da sessão encerrada é recusada. |
| AU23–AU24 | Falhas de consulta e persistência injetadas nos pontos correspondentes. A resposta ao erro de gravação não emite cookie de sessão, e o acesso seguinte exige login. |
| AU25–AU27 | Chave encerrada e cabeçalho de cache já conferidos. A perda real de resposta, a retomada assistida e o tratamento de telas em outras abas dependem de P014/P020. |
| AU28–AU29 | Campos extras não concedem privilégios. Testes de erro conferem resposta e registro sanitizados em cenários controlados. |
| AU30 | Fluxo de teclado conferido em Chromium. Tecnologias assistivas e a matriz de dispositivos dependem da homologação P019. |
| AU31–AU32 | Métodos HTTP e ordem da proteção conferidos. Revisados o uso do modelo e sessão nativos, a herança direta de `View` e o esquema sem novos modelos. |

## Continuidade

P014 mantém abertas as políticas de credenciais, recuperação, tentativas, expiração de produto e revogação global. P015 cobre TLS, proxy, configuração remota e limpeza operacional das sessões vencidas. P020 cobre o tratamento da resposta perdida e a proteção de telas ou dados que continuem em outras abas. Perfis de negócio, vínculos e concessão de permissões permanecem nos seus recortes.

Para experimentar o fluxo, siga o [preparo local](../README.md#preparo-local). O acompanhamento está no [cartão da I02](https://trello.com/c/DpZG5hth).
