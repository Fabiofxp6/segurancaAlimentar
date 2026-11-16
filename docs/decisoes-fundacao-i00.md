# I00 — Decisões para a fundação executável

Em 15/11/2026, Fábio aprovou o [roteiro](plano-implementacao.md) e autorizou a I00. Ao pedir “pode seguir” após esta entrega, Fábio autorizou a I01 com as escolhas apresentadas. [Cartão da I00 no Trello](https://trello.com/c/ChWnlfZ8)

## 1. Versões e dependências

| Componente | Recomendação | Alternativa e impacto |
|---|---|---|
| Python | **CPython 3.14.x**, com a correção estável vigente da série na preparação. A série tem suporte previsto até outubro de 2030 e é compatível com Django 5.2 desde 5.2.8. [Ciclo do Python](https://devguide.python.org/versions/) · [Compatibilidade do Django](https://docs.djangoproject.com/en/5.2/faq/install/#what-python-version-can-i-use-with-django) | 3.13.x tem suporte previsto até outubro de 2029 e é alternativa caso alguma dependência necessária tenha incompatibilidade comprovada com 3.14. |
| Django | **5.2 LTS**, com a última correção estável da série. Recomendo o suporte estendido até abril de 2028 para a primeira versão do projeto. [Versões suportadas](https://www.djangoproject.com/download/#supported-versions) | 6.1 é uma série com funcionalidades mais recentes e suporte estendido até dezembro de 2027. A fundação descrita na Spec 0001 cabe na 5.2. |
| PostgreSQL | **17.x**, com a correção estável vigente. Django 5.2 aceita PostgreSQL 14 ou superior, e a série 17 tem suporte previsto até novembro de 2029. Usar a mesma versão principal em desenvolvimento e teste. [Compatibilidade](https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes) · [Suporte do PostgreSQL](https://www.postgresql.org/support/versioning/) | 18.x tem suporte até novembro de 2030. A escolha pode ser reavaliada se o provedor futuro exigir outra versão ou houver necessidade demonstrada de um recurso específico. |
| Driver | **Psycopg 3.3.x** com `psycopg[binary]` para desenvolvimento e testes. A documentação do driver inclui Python 3.14 e PostgreSQL 17 na faixa de suporte, e o pacote binário vem com bibliotecas cliente. Conferir a disponibilidade do pacote para a plataforma ao preparar o ambiente. [Instalação do Psycopg](https://www.psycopg.org/psycopg3/docs/basic/install.html) | `psycopg[c]` é opção para uma plataforma ou política que exija compilação com bibliotecas do sistema. A forma de distribuir o driver em produção será avaliada com a hospedagem. |

Proponho **uv** para preparar o Python do projeto e reproduzir as dependências. Na I01, `pyproject.toml` declara as séries aprovadas, `.python-version` seleciona Python 3.14 e `uv.lock` registra as versões exatas resolvidas. Registrar também a correção de Python, a versão do uv utilizada e a identificação da imagem PostgreSQL validada. Atualizações de correção na mesma série passam pelas verificações da fundação. Uma troca de série volta para revisão de compatibilidade. A alternativa é `venv` com `pip` e dependências direta e indiretamente fixadas, com preparação do interpretador em separado. [Estrutura de projetos do uv](https://docs.astral.sh/uv/concepts/projects/layout/) · [Versões de Python no uv](https://docs.astral.sh/uv/concepts/python-versions/)

No Mac atual, o `python3` do terminal apontava para 3.9.6, o cliente `psql` tinha versão 14.20 e os executáveis do uv e do Compose estavam presentes. O cliente PostgreSQL fornece a versão do executável local. O acesso ao motor Docker ficou sem verificação por falta de acesso ao socket nesta consulta. A compatibilidade acima é documental, e a I01 deve confirmar o interpretador, a instalação do driver, o motor e a versão do servidor por conexão real em ambiente isolado.

## 2. Desenvolvimento e testes

Proponho executar **Django no host via uv** e usar **Docker Compose para o PostgreSQL local**, com instâncias separadas para desenvolvimento e testes. Essa configuração permite que a equipe use a mesma série do banco e controle o descarte dos dados fictícios de teste independentemente do banco de desenvolvimento. A alternativa é PostgreSQL instalado localmente, em instâncias separadas com os mesmos critérios de isolamento, quando a equipe não puder executar o Compose. [Portas publicadas pelo Docker](https://docs.docker.com/engine/network/port-publishing/) · [Banco de testes do Django](https://docs.djangoproject.com/en/5.2/topics/testing/overview/#the-test-database)

| Perfil | Contrato proposto para I01 |
|---|---|
| Desenvolvimento | Selecionar `config.settings.development` explicitamente. Banco e credencial próprios, volume de desenvolvimento separado e porta publicada em `127.0.0.1`. Debug é optativo. |
| Teste | Selecionar `config.settings.test` explicitamente. Instância descartável com porta, credencial e dados próprios. Definir e documentar o destino esperado do teste, validar o destino antes de abrir a conexão e recusar o endpoint de desenvolvimento e destinos fora do ambiente isolado previsto. O papel usado pelo executor tem permissão de criar o banco do teste dentro dessa instância. |
| Produção | Preparar o perfil `config.settings.production` com debug desligado e validação de hosts e configuração externa. Provedor, TLS, credenciais e ambiente operacional ficam para o recorte de operação. |

Usar as variáveis externas da [Spec 0001](specs/0001-fundacao-tecnica.md) e selecionar o perfil de modo explícito. Para desenvolvimento e teste, a preparação pode carregar o arquivo local escolhido com `uv run --env-file`, usando valores próprios em cada perfil. Verificar precedência e valores exigidos no comando efetivo. O Django recebe as variáveis do processo. O `example.env` poderá servir de referência após conferir chaves e valores fictícios na I01. Incluir no versionamento somente o exemplo e excluir os arquivos locais com segredos. Validar configuração ausente ou inválida antes de conectar. O backend escolhido é `django.db.backends.postgresql`. [Referência do uv para o arquivo de ambiente](https://docs.astral.sh/uv/reference/cli/#uv-run--env-file)

## 3. Estrutura da aplicação

Recomendo aceitar o **monólito modular** para o início, conforme o [ADR 0007](adr/0007-monolito-modular.md). Uma aplicação Django atende a primeira entrega, e as responsabilidades de contas e inspeções ficam organizadas por domínio conforme forem implementadas. A I01 começa com `manage.py`, `config/` para URLs, inicialização e perfis de configuração, `contas/` para identidade e `templates/` para a base visual e páginas de erro. A alternativa de separar serviços ou frontend desde a fundação introduziria comunicação, implantação e contratos adicionais sem uma necessidade identificada no recorte. A divisão dos próximos apps depende das respectivas specs.

## 4. Identidade da primeira migração

Proponho **`contas.Usuario` derivado de `AbstractUser`, com `id` interno `BigAutoField`**. Definir `AUTH_USER_MODEL` antes de gerar a migração e criar o modelo em `contas/0001_initial`. As referências de outros apps devem apontar para o modelo de usuário configurado. [Modelo de usuário customizado](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model) · [`BigAutoField`](https://docs.djangoproject.com/en/5.2/ref/models/fields/#bigautofield)

| Item | Escolha proposta |
|---|---|
| Identificador físico | Inteiro autoincrementado de 64 bits para a chave interna. `usuarioId` continua a referência lógica nas specs. A referência UUID do catálogo é candidata e a escolha física deve ser registrada na Spec 0001 após o aceite. |
| Alternativa ao inteiro | UUID como chave primária se surgir necessidade comprovada de gerar identidades em sistemas independentes. Se uma função futura exigir referência externa opaca, avaliar um identificador público próprio no contrato daquela função. A autorização por recurso continua necessária com qualquer formato. |
| Campos iniciais | Preservar os campos herdados de `AbstractUser`, incluindo `username` único, senha pelo mecanismo nativo, `is_active` e flags técnicas. O nome de usuário é a credencial de identificação. A I01 cria a estrutura de identidade e a migração. |
| Campos do cadastro e concessões | A representação do nome de negócio, perfil-base, vínculos e concessão inicial pertence à parte restante de P002 em I03. Designação por ação continua em I05. A primeira migração pode ser feita sem campos adicionais para essas funções, e as flags técnicas seguem o seu papel no Django. |

## Entrega de código que essas escolhas liberam

Com as propostas acima aprovadas e a I01 autorizada, a entrega é a **fundação executável local**. Ela inclui configuração por perfil, dependências reproduzíveis, PostgreSQL isolado e a migração inicial de `contas.Usuario`. Inclui também a estrutura mínima de templates e erros. Login, logout e a escolha do backend de sessão do ADR 0008 pertencem ao recorte I02. [Spec 0001](specs/0001-fundacao-tecnica.md) · [Roteiro](plano-implementacao.md)

O aceite da I01 usa VF01–VF12 conforme o recorte. Reproduzir a preparação, identificar o servidor PostgreSQL real, aplicar a migração em banco isolado, verificar o usuário customizado, provocar configuração inválida, conferir o isolamento do banco de teste e renderizar os erros sem expor segredos. O relatório da I01 deve indicar o resultado observado de cada cenário aplicável e quaisquer verificações pendentes.

## Aceite

As escolhas da I00 foram aplicadas na I01 e registradas em DC023–DC025. O acesso ao Docker e a conexão real foram verificados durante a execução. [Decisões confirmadas](decisoes-confirmadas.md) · [Resultados da I01](entrega-i01.md)
