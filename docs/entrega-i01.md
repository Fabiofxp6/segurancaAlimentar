# Entrega I01 — Fundação executável

Fundação implementada e verificada em 15/11/2026 no ambiente local. O comando de preparo está no [README](../README.md#preparo-local). O escopo e as decisões de partida estão no [roteiro](plano-implementacao.md) e no [registro da I00](decisoes-fundacao-i00.md). [Cartão da I01 no Trello](https://trello.com/c/hR9CIEZn)

| Componente | Versão verificada |
|---|---|
| CPython | 3.14.10 no macOS ARM64 |
| uv | 0.11.1 na resolução e no sincronismo das dependências |
| Django | 5.2.19 |
| Psycopg | 3.3.9 com implementação binária |
| PostgreSQL | 17.12 via Docker Engine 29.8.2 e Compose 5.5.1. Imagem base `postgres:17.12-bookworm` fixada por digest no Dockerfile. |

Desenvolvimento usa `127.0.0.1:55434`, pois 55432 já está alocada a outro projeto no Mac. Teste usa `127.0.0.1:55433`. Os projetos Compose e os volumes são separados. Cada operador do Django tem sua credencial local, com `CREATEDB` limitado ao papel na instância de teste. O `postgres` da imagem é usado no preparo inicial. Os valores de ambiente locais ficam em arquivos ignorados pelo Git.

## Verificações da Spec 0001

| Cenário | Resultado observado |
|---|---|
| VF01 | `uv sync --locked` instalou as dependências. O sincronismo foi reproduzido em outro ambiente virtual com `--locked --offline`. |
| VF02 | O carregamento rejeitou perfil ausente, uso direto do perfil base, chave e banco ausentes, debug inválido, debug ativo em produção, host inválido, curinga global em produção, origem CSRF com caminho e porta inválida. `false` resultou em `False`. A saída dos casos examinados não continha as credenciais da execução. |
| VF03 | Uma consulta pelo Django confirmou PostgreSQL 17.12 no banco de desenvolvimento. Com a porta apontando para destino indisponível, a checagem de migrações falhou com erro de conexão. |
| VF04 | A migração `contas.0001_initial` foi aplicada em PostgreSQL novo. `migrate --check` passou e `makemigrations --check --dry-run` indicou ausência de mudanças pendentes. |
| VF05 | O teste gravou e recarregou `contas.Usuario` com chave `BigAutoField` e senha codificada. A senha fictícia foi validada pelo mecanismo nativo do Django. |
| VF06 | O modelo inicial preserva os campos de `AbstractUser`. A migração e o teste confirmaram a estrutura de identidade e a criação de conta fictícia com `is_staff` e `is_superuser` falsos. A estrutura de perfis do produto fica no recorte correspondente. |
| VF07 | O teste provocou uma exceção dentro de `transaction.atomic()` e confirmou que o registro criado na transação não ficou persistido. |
| VF08 | O executor recusou o perfil de desenvolvimento. O perfil de teste rejeitou porta, host, banco e papel fora do conjunto esperado. A suíte criou e descartou seu banco na instância de teste. A conexão confirmou papéis distintos e `CREATEDB` somente no teste. |
| VF09 | O teste HTTP disparou uma falha com detalhe interno e parâmetro fictício. O log da aplicação emitido pelo handler de `django.request` trouxe o status 500 e omitiu ambos os valores. |
| VF10 | O cliente de teste recebeu as páginas 403, 404 e 500 com debug desativado. O 500 também foi verificado com o perfil de produção e o PostgreSQL inacessível. |
| VF11 | A estrutura efetiva contém configuração, identidade, templates e migrações. As rotas de falha exercitadas são restritas ao módulo de testes. |
| VF12 | `check`, a suíte de três testes, as verificações de migração e o sincronismo pelo lock passaram. A conferência incluiu `example.env` e as regras do `.gitignore`. |

As evidências correspondem à fundação local e aos controles exercitados nestes cenários. O ambiente de produção real e seus itens de deploy seguem para o recorte de operação. A próxima etapa do roteiro é a autenticação (I02), condicionada à autorização e às decisões de sessão aplicáveis da [Spec 0002](specs/0002-autenticacao.md).
