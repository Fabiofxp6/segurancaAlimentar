# Spec 0001: Fundação técnica

- **Status:** Proposto; elaboração documental, sem implementação.
- **Data:** 10/11/2026.
- **Etapa:** 4, fundação técnica e skill de specs.
- **Produto:** [PRD 0001](../prd/0001-sistema-avaliacao-seguranca-alimentar.md).
- **Arquitetura:** [responsabilidades e limites](../arquitetura.md).
- **Decisões:** [ADR 0001](../adr/0001-python-django-postgresql.md), [ADR 0002](../adr/0002-mvt-com-services-e-templates.md) e [ADR 0003](../adr/0003-usuario-customizado-e-sessao-django.md); [ADR 0007](../adr/0007-monolito-modular.md) permanece recomendação.
- **Fontes:** F003, F007 e F008 no [índice](../referencias/README.md), [decisões confirmadas](../decisoes-confirmadas.md) e [pendências](../pendencias.md).
- **Depende de:** nenhuma spec anterior. As decisões abertas e seus pontos de bloqueio estão abaixo.

## Objetivo e limite da entrega

Especificar a base sobre a qual serão construídos autenticação, acesso e os fluxos de fiscalização: configuração reproduzível, PostgreSQL, identidade inicial, organização e verificações da fundação. Esta entrega cria apenas documentos. Estruturas, configurações, comandos e testes descritos são contratos ou propostas para execução futura autorizada.

A base confirmada é Python/Django, PostgreSQL, MVT, Templates, views próprias derivadas diretamente de `View`, services independentes de HTTP e usuário customizado `AbstractUser` com sessão Django. O desenho físico abaixo é uma proposta para revisão; continuar a etapa não aprova automaticamente o ADR 0007 ou os contratos novos.

Não há versões selecionadas, ambiente instalado ou primeira migração pronta. Esta spec ainda não está pronta para implementação integral: os bloqueios estão identificados por parte da execução, sem impedir sua revisão documental.

## Escopo

Inclui proposta de organização mínima, configurações por ambiente, dependências a declarar, conexão PostgreSQL, base do usuário, regras para primeiras migrações, templates comuns, limites de camadas e plano de aceite.

Não inclui os fluxos de login/logout, recuperação ou gestão de sessão, cujo recorte da Etapa 5 está na [Spec 0002](0002-autenticacao.md); modelos de perfil, vínculos e supervisão da Etapa 6; cadastros de negócio, inspeções, score, uploads, PDF ou auditoria oficial. Não cria um app para cada área lógica nem instala filas, containers, serviços de nuvem, biblioteca de interface ou ferramenta de testes adicional.

## Dependências e bloqueios de execução

| Parte futura | O que precisa estar decidido | Situação atual |
|---|---|---|
| Preparar ambiente e dependências | Versões compatíveis de Python, Django, PostgreSQL e driver; ferramenta de preparação e arquivo de versões | P001 aberta; não copiar o blog nem usar uma versão implícita |
| Criar estrutura física | Validar a recomendação de aplicação única e os nomes candidatos desta spec | ADR 0007 e contratos abaixo propostos |
| Gerar/aplicar a primeira migração de identidade | Escolher identificador e campos iniciais que alterem o schema; confirmar rótulo do usuário customizado | P002 aberta; `contas.Usuario` é candidato |
| Executar testes com banco | Definir PostgreSQL e credenciais exclusivos de teste, com isolamento verificável | P001; detalhes de ambiente em P015, sem usar credenciais reais de operação |
| Colocar em operação | Definir hospedagem, HTTPS, segredos, arquivos, logs, backup e metas pertinentes | P014 a P019; esta spec não aprova a operação real |

P003 a P006 não impedem descrever a identidade mínima, mas impedem fechar seus vínculos de negócio e supervisão. Não escolher sua representação para conseguir antecipar essas funções. P007 a P013 e P020 a P022 continuam nos recortes correspondentes, sem virar pré-requisito artificial de todo o trabalho de fundação.

## Estrutura candidata

Proposta de nomes e responsabilidades; os caminhos abaixo ainda não existem como aplicação. O exemplo pressupõe validação do ADR 0007.

```text
manage.py
config/
  settings/
    base.py
    development.py
    test.py
    production.py
  urls.py
  asgi.py
  wsgi.py
contas/
  apps.py
  models.py
  migrations/
  tests/
templates/
  base.html
  403.html
  404.html
  500.html
```

Os pacotes Python terão os arquivos de inicialização necessários quando forem implementados. `config` reúne configuração e entradas do framework. `contas` começa somente com a identidade mínima aprovada. Não criar services, forms, views ou módulos comuns vazios para simular uma funcionalidade inexistente. Adicioná-los quando o primeiro contrato correspondente for implementado.

Dependências serão declaradas em arquivo próprio com versões reproduzíveis conforme P001. Um arquivo de exemplo de ambiente poderá listar apenas chaves e valores fictícios; o `.env` existente permanece preservado. Exclusão de segredos e artefatos locais deverá ser prevista no controle de versão futuro, sem inicializar Git nesta fase.

## Configuração por ambiente

### Seleção e separação

Proposta: selecionar explicitamente `config.settings.development`, `config.settings.test` ou `config.settings.production` por `DJANGO_SETTINGS_MODULE`. `base` é compartilhamento interno, não um ambiente de execução. Perfil ausente ou desconhecido deve ser rejeitado pela preparação, sem assumir produção ou desenvolvimento silenciosamente.

Manter nomes e contrato de configuração iguais entre ambientes, com valores externos próprios. Não usar a chave, o banco ou as credenciais de produção em desenvolvimento ou testes. O processo recebe as variáveis do ambiente; existir um arquivo `.env` não significa que Django o carregará. Um carregador ou ferramenta adicional só será adotado se escolhido em P001.

### Contrato proposto das variáveis

Os nomes abaixo são candidatos; os valores reais não fazem parte desta spec. Não há máscaras de apresentação para segredos ou conexão. Mensagens de erro identificam somente a chave inválida, sem mostrar seu conteúdo.

| Chave | Tipo após leitura | Presença e validação proposta | Destino |
|---|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `str` | Obrigatória; um dos três perfis declarados | Seleção do settings |
| `DJANGO_SECRET_KEY` | `str` sensível | Obrigatória e não vazia; sem segredo real no exemplo ou fallback público | `SECRET_KEY` |
| `DJANGO_DEBUG` | `bool` | Se ausente, `false`; se presente, aceitar somente `true` ou `false`, sem diferença de caixa e com espaços externos removidos | `DEBUG` |
| `DJANGO_ALLOWED_HOSTS` | `list[str]` | Lista por vírgula, sem entradas vazias; obrigatória para os hosts previstos; em produção rejeitar lista vazia e curinga global | `ALLOWED_HOSTS` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `list[str]` | Opcional, vazia quando não necessária; cada origem com esquema e host; não preencher permissões amplas por conveniência | `CSRF_TRUSTED_ORIGINS` |
| `POSTGRES_DB` | `str` | Obrigatória, não vazia; banco selecionado explicitamente | Nome do banco |
| `POSTGRES_USER` | `str` | Obrigatória, não vazia; conta própria do ambiente | Usuário do banco |
| `POSTGRES_PASSWORD` | `str` sensível | Obrigatória, sem expor em erro/log; preservar caracteres do segredo sem normalização indevida | Senha do banco |
| `POSTGRES_HOST` | `str` | Obrigatória, não vazia; sem assumir endereço de máquina de referência | Host do banco |
| `POSTGRES_PORT` | `int` | Obrigatória; inteiro válido para porta de rede | Porta do banco |

As listas devem remover espaços ao redor dos elementos. Não usar `bool(texto)` para converter uma variável, pois a string `false` não deve ativar debug. Validar as configurações antes de usar a conexão. Expor falta de variável como falha de configuração, não como gravação pendente de inspeção.

### Contrato dos perfis

| Perfil candidato | Contrato |
|---|---|
| Desenvolvimento | PostgreSQL próprio; debug só quando explicitamente habilitado; nenhum segredo real ou exposição pública implícita |
| Teste | PostgreSQL descartável/isolado, valores próprios e rejeição de configuração que aponte para banco operacional; não herdar silenciosamente o banco de outro perfil |
| Produção | Debug obrigatoriamente desligado; hosts definidos; HTTPS e cookies protegidos conforme implantação validada; segredos externos; detalhes de exceção restritos |

Preservar os componentes de segurança, sessão, autenticação e CSRF necessários do Django. A base não fixa prazo de sessão, SameSite, MFA, recuperação ou limitação de tentativas; esses controles permanecem em P014. Configuração de proxy e terminação TLS depende da hospedagem, sem confiar em cabeçalho de proxy sem essa definição.

Propõe-se `LANGUAGE_CODE` em português brasileiro e `USE_TZ` habilitado, com instantes tratados de forma consistente. Fuso padrão de exibição, datas civis e formato de apresentação precisam de validação antes das telas correspondentes; não adotar o fuso do computador do desenvolvedor como regra do produto.

A distinção entre configuração de desenvolvimento e operação e o cuidado com chave, debug, hosts e HTTPS seguem a [lista de implantação do Django](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/). Os nomes externos e a separação de arquivos acima são propostas locais, não exigências do framework. As opções disponíveis devem ser conferidas na versão escolhida. [Referência de settings](https://docs.djangoproject.com/en/stable/ref/settings/).

## PostgreSQL e persistência

Usar `django.db.backends.postgresql` como backend e um driver compatível a definir em P001. Não aplicar fallback para SQLite se faltar variável, driver ou conexão. Configuração inválida falha de forma clara; banco indisponível não é convertido em sucesso, inicialização de outro banco ou criação automática de dados.

Conexão criptografada, certificados, usuário de migração, permissões de execução e gestão de credenciais precisam ser definidos para cada ambiente conforme a implantação. Não usar superusuário do banco como pressuposto de operação. O teste deve verificar o banco efetivamente utilizado, não apenas o nome do arquivo de configuração.

Não criar esquema para fiscalização, checklist ou documentos nesta fundação. As relações futuras usarão o modelo de usuário configurado e as decisões de identidade validadas. A fundação não escolhe estratégia de exclusão histórica, campos de auditoria genéricos ou algoritmo de concorrência para entidades ainda não especificadas.

## Base do usuário customizado

Proposta de nome físico: `contas.Usuario`, derivado de `AbstractUser`, com `AUTH_USER_MODEL` apontando para esse modelo antes das migrações. A derivação e o uso de sessão estão confirmados; nome de app/classe, identificador e campos adicionais continuam sujeitos à revisão. Referências futuras ao usuário devem respeitar o modelo configurado, sem depender diretamente do `User` padrão como se fosse o modelo do projeto.

| Elemento | Tipo/representação | Contrato e limite |
|---|---|---|
| Identificador primário | A decidir em P002 | Não escolher UUID ou inteiro a partir de exemplo; bloqueia a primeira migração |
| `username` | `str`, campo herdado | Nome de acesso confirmado; regras e limites da versão escolhida serão registrados na spec de autenticação, sem máscara nova nesta fundação |
| `password` | `str` com codificação de senha do Django | Usar mecanismos nativos de criação/verificação; não guardar senha legível nem atribuir entrada bruta ao campo |
| `is_active` | `bool` herdado | Situação técnica da conta; aplicação no fluxo de entrada será detalhada na Etapa 5 |
| `is_staff`, `is_superuser` | `bool` herdados | Controle técnico do framework, sem equivalência automática aos perfis do produto ou à autoridade de aprovação |
| Demais campos e relações herdados | Conforme `AbstractUser` da versão escolhida | Não remover ou mudar obrigatoriedade por inferência; não interpretar todo campo herdado como requisito de tela |
| Perfis, vínculos e designação de Supervisor | Ainda sem representação física aprovada | Não criar enum de perfil, booleano global de Supervisor ou relacionamento com inspeção nesta spec; detalhar na Etapa 6 |

Restrições e índices herdados seguem a versão validada. Índices adicionais dependem de consulta real prevista, não de um cadastro antecipado. Não inserir usuários, senhas, grupos ou supervisores por seed nesta fundação.

O modelo customizado precisa ser criado na primeira migração de seu app; a escolha posterior do identificador não pode ser disfarçada como simples ajuste após migrações já aplicadas. Conferir isso antes de gerar o histórico inicial. [Usuário customizado no Django](https://docs.djangoproject.com/en/stable/topics/auth/customizing/).

## Preparação e migrações futuras

Depois de resolver os bloqueios aplicáveis e receber autorização de implementação:

1. Registrar versões, dependências e forma de preparar o ambiente conforme P001; usar os nomes físicos validados.
2. Criar a estrutura mínima e separar configuração, sem copiar o projeto ou o banco do blog.
3. Definir o modelo customizado e sua configuração antes da primeira migração, após P002.
4. Gerar e revisar a migração inicial da identidade e as dependências do framework. Não alterar dependências do Django manualmente para ocultar um ciclo.
5. Aplicar em PostgreSQL novo e isolado e verificar que o modelo configurado é o usuário efetivo. Não apagar um banco existente para simular uma instalação nova.
6. Conferir inicialização, ausência de migrações faltantes e os cenários de aceite. Registrar ambiente e resultado obtido.

`check`, `migrate`, `migrate --check`, `makemigrations --check --dry-run` e a execução de testes são verificações futuras a documentar com o perfil de settings explícito. Distinguir migração existente ainda não aplicada de alteração de model ainda sem migração; uma verificação não substitui a outra. Não foram executadas agora. `check --deploy` será considerado com configuração de implantação real; não prova sozinho segurança ou prontidão operacional. [Comandos administrativos do Django](https://docs.djangoproject.com/en/stable/ref/django-admin/).

Não escolher restauração, reversão destrutiva ou recriação automática como resposta a falha. A aplicação futura em ambiente existente dependerá de plano de migração e recuperação aprovado, sem reutilizar o banco de referência.

## Camadas, rotas, templates e Admin

Esta spec não cria service de negócio, form de autenticação ou rota de fiscalização. Os contratos correspondentes serão definidos nas Etapas 5 e 6 ou em specs funcionais posteriores. A fundação precisa conservar a organização que permita views próprias derivadas de `View` e services sem HTTP, sem criar abstrações vazias para demonstrar essa regra.

Não há endpoint público novo incluído no aceite da fundação. `config/urls.py` é o ponto de composição futuro. Login, logout, painel, consulta do estabelecimento, API e endpoint de saúde não são assumidos por este documento.

Proposta de template base com título, conteúdo principal e pontos de extensão para recursos da tela. Templates de erro 403/404/500 apresentam mensagem em português sem detalhes internos ou dados da requisição. O 500 deve poder renderizar sem depender de consulta ao banco ou de usuário autenticado. Aparência final, telas e homologação seguem P019 e as specs das funções.

Preservar escape de conteúdo e os mecanismos de CSRF conforme a tela futura. Não acrescentar JavaScript de reenvio, cache persistente ou captura de evidência nesta fundação. Operação somente online continua restrição do produto, sem afirmar que seus fluxos foram implementados.

Não registrar modelos críticos para edição livre no Admin. Configuração técnica de usuários, exposição do Admin e suas permissões serão detalhadas nas specs aplicáveis, usando mecanismos nativos de senha. A existência de `is_staff` não cria o perfil Administrador nem autorização sobre inspeções.

## Falhas e registros operacionais

| Situação | Resultado esperado na futura fundação |
|---|---|
| Configuração obrigatória ausente ou inválida | Interromper preparação/inicialização pertinente com a chave identificada, sem mostrar o valor |
| Debug habilitado no perfil de produção | Rejeitar a configuração, em vez de aceitar exposição de detalhes |
| Driver ou PostgreSQL indisponível | Informar falha técnica sem fallback, gravação fictícia ou criação de outro banco |
| Identidade inicial não decidida | Não gerar/aplicar migração que cristalize a escolha pendente |
| Banco de teste confundido com ambiente operacional | Não iniciar execução que possa criar, alterar ou remover dados nesse destino |
| Erro inesperado em requisição futura | Mensagem genérica para o usuário e contexto técnico restrito, sem segredos, corpo sensível ou stack trace público |

Logs técnicos não são trilha oficial de auditoria. Formato, destino, retenção, alertas e responsáveis permanecem em P015 e P017. A base deve permitir diagnóstico sem registrar `SECRET_KEY`, senhas, conteúdo de sessão ou credenciais de conexão. Não serializar toda a configuração ou a requisição como evidência de erro.

## Relação com os requisitos

Esta é uma relação local da fundação, complementar à [matriz completa elaborada na Etapa 6](../matriz-rastreabilidade.md). Indica contribuição futura parcial; nenhum requisito fica implementado por esta entrega.

| Requisitos existentes | Contribuição da fundação | Verificação futura |
|---|---|---|
| RF001 e RF002 | Identidade customizada como pré-requisito; sem login ou gestão de perfis | VF05 e VF06 |
| RNF04 e RNF05 | Banco confirmado, migrações e persistência coerente | VF03, VF04 e VF07 |
| RNF09 e RNF12 | Organização e preparação reproduzível por ambiente | VF01, VF02 e VF12 |
| RNF10 | Diagnóstico técnico com dados protegidos | VF09 e VF10 |
| RS003 e RS004 | Base de senha e sessão do framework; políticas ainda futuras | VF05 e VF06 |
| RS005 | Configuração candidata para operação HTTPS; implantação ainda pendente | VF02; validação de transporte real antes de operar |
| RS009, RS011 e RS012 | Validação de configuração e preservação de segredos | VF02, VF09 e VF10; validação de dados de negócio será posterior |
| RS015 | Dependências e versões declaradas para acompanhamento | VF01 e VF12; processo de vulnerabilidades ainda a definir |

Não se reivindica nesta spec atendimento a salvamento de resposta, autorização por ação, recuperação de envio, auditoria oficial, backup completo ou emissão de PDF.

## Critérios de aceite da implementação futura

Todos os cenários estão planejados e não executados. A evidência deve identificar configuração utilizada sem seus segredos, versões, preparação, passos e resultado. Usar PostgreSQL isolado nos cenários de persistência; verificar o destino antes de executar. O mecanismo de banco de teste do Django não dispensa a configuração correta do ambiente. [Banco de teste no Django](https://docs.djangoproject.com/en/stable/topics/testing/overview/#the-test-database).

| Cenário | Verificação observável |
|---|---|
| VF01 Preparação | Em ambiente separado, reproduzir a preparação com as versões e dependências declaradas, sem copiar arquivos secretos |
| VF02 Configuração | Omitir segredo/banco, usar debug inválido ou ativá-lo em produção e informar hosts inválidos; rejeitar cada caso sem expor valores; verificar que `false` não vira verdadeiro |
| VF03 Conexão | Confirmar que o backend e o banco efetivos são PostgreSQL; interrupção de conexão falha sem criar ou usar SQLite |
| VF04 Migração inicial | Aplicar em banco novo isolado com o usuário customizado na primeira migração; repetir a verificação sem novas alterações pendentes |
| VF05 Identidade | Confirmar que o modelo configurado é o customizado e que senha de teste passa pelos mecanismos nativos, sem persistir o texto original |
| VF06 Limites de identidade | Confirmar campos técnicos herdados sem criação automática de perfil de negócio, Supervisor global, equipe ou concessão de aprovação |
| VF07 Persistência | Executar uma alteração de teste em transação que falhe e verificar preservação do estado anterior no PostgreSQL; não usar isso como prova de atomicidade com arquivos |
| VF08 Isolamento de teste | Verificar que testes usam destino próprio e não leem/escrevem banco operacional; configuração incompatível impede a execução perigosa |
| VF09 Erros e logs | Provocar falha técnica controlada e conferir mensagem sem segredo e contexto restrito; não comparar apenas o texto de uma constante |
| VF10 Templates de erro | Renderizar erros com conteúdo de teste e produção sem debug; o 500 continua legível mesmo sem banco e não expõe stack trace ou dados sensíveis |
| VF11 Fronteiras | Revisar a base criada, as migrações e as entradas técnicas para confirmar respeito à arquitetura, sem módulos de negócio antecipados ou atalhos de permissão |
| VF12 Integridade da entrega | Conferir dependências, instruções, ausência de migrações faltantes, segredos fora do conteúdo distribuído e compatibilidade entre spec e implementação |

- [ ] Bloqueios da parte implementada resolvidos e contratos novos validados, com origem registrada.
- [ ] Fundação preparada e cenários aplicáveis executados, com resultados e limitações reais.
- [ ] Nenhuma etapa posterior considerada implementada por causa da configuração inicial.

## Continuidade

A [spec de autenticação](0002-autenticacao.md) foi elaborada na Etapa 5 e permanece Proposta. Seu [ADR 0008](../adr/0008-sessoes-no-servidor-com-postgresql.md) recomenda backend de sessões em banco, ainda não aprovado; não modifica a configuração real da fundação. A [Spec 0003 de acesso](0003-acesso-vinculos-supervisao.md) e a [matriz completa](../matriz-rastreabilidade.md) foram elaboradas na Etapa 6, também Propostas; não resolvem por si as escolhas físicas de P002. As Etapas 7 e 8 foram elaboradas para revisão; a [revisão final](../revisao-final-fundacao.md) e o [estado](../state.md) registram a passagem à próxima atividade que o usuário solicitar, sem início automático de implementação. Esta spec será revisada conforme as decisões de ambiente e identidade forem efetivamente tomadas; não avançará para Implementado por aprovação do texto.

O [estado](../state.md), as [etapas](../etapas.md) e o [acompanhamento no Trello](../acompanhamento-trello.md) indicam o ponto de retomada. Nesta entrega nenhum código, ambiente, dependência, banco, migração ou configuração real foi criado ou alterado.
