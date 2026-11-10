# Análise do projeto de referência para nossa fundação

Data: 09/11/2026. Referência: blog Django `labiv20262`.

Arquivo independente para guardar e consultar antes de iniciar o Sistema de Avaliação de Segurança Alimentar. O foco principal é a organização de PRD, skills, specs, arquitetura, estado e AGENTS, seguida da análise técnica e da memória das decisões do nosso sistema. As propostas permanecem identificadas; a fundação ainda não foi implementada.

Conteúdo: [organização documental](#organizacao-documental), [análise técnica](#analise-tecnica) e [memória para a fundação](#memoria-para-fundacao).


<a id="organizacao-documental"></a>

## Organização documental para iniciar nosso projeto

Data: 09/11/2026. Foco solicitado: PRD, skills, specs, `arquitetura.md`, `state.md` e `AGENTS.md`. Este registro aprofunda a análise desses arquivos no projeto de referência e orienta sua adaptação futura ao Sistema de Avaliação de Segurança Alimentar. Não cria a fundação nem altera as regras vigentes do blog.

### Conclusão da análise

O principal aprendizado da referência é a divisão de responsabilidades entre os documentos. O PRD estabelece o comportamento do produto; as specs transformam esse comportamento em contratos implementáveis; a arquitetura define as fronteiras do código; as skills orientam como executar cada tipo de trabalho; o AGENTS indica o que consultar; e o state preserva o ponto de retomada.

O usuário definiu esse conjunto como prioridade para o início do nosso projeto. Vamos preservar essa organização como referência de trabalho. As regras técnicas particulares do blog, os números de versão e os exemplos de posts continuam sujeitos à adaptação e não se tornam decisões do sistema alimentar apenas por constarem nesses arquivos.

### Mapa de responsabilidades

| Artefato | Pergunta que responde | Deve conter | Evitar |
|---|---|---|---|
| `AGENTS.md` | Como trabalhar neste repositório? | Regras essenciais, ordem de leitura, caminhos e condições de uso das skills | Duplicar todas as regras de negócio e toda a arquitetura |
| `docs/prd/` | O que o produto faz, para quem e com qual objetivo? | Objetivos, perfis, RF/RNF verificáveis, limites e critérios de conclusão | Classes, colunas, métodos e detalhes de bibliotecas |
| `.agents/skills/` | Como executar um tipo de tarefa com consistência? | Instruções reutilizáveis, gatilhos de uso, formato de entrega e verificações pertinentes | Misturar pendências temporárias com instruções permanentes |
| `docs/specs/` | Como construir e verificar uma funcionalidade? | Requisitos atendidos, dependências, dados, services, permissões, rotas, erros e testes | Inventar regras de produto ou repetir a justificativa inteira de uma ADR |
| `docs/arquitetura.md` | Onde cada responsabilidade deve ficar? | Camadas, dependências permitidas, acesso a dados, contratos e exceções | Cronograma, histórico de tarefas e regras locais de uma única tela |
| `docs/state.md` | De onde a próxima tarefa deve continuar? | Trabalho atual, próximo passo concreto e pendências ainda abertas | Histórico completo, duplicação dos requisitos e status de todos os documentos |
| `docs/adr/` | Por que uma decisão estrutural foi tomada? | Contexto, decisão, alternativas relevantes, consequências e status | Detalhes pequenos e fáceis de trocar |
| `CLAUDE.md` | Como localizar as mesmas instruções em outra ferramenta? | Na referência, apenas `@AGENTS.md` | Manter outra cópia divergente das instruções |

As ADRs complementam os seis itens priorizados: a arquitetura diz a regra atual, enquanto a ADR preserva a razão da escolha. `CLAUDE.md` não substitui `AGENTS.md`; a referência evita duplicação usando um apontamento.

### AGENTS como ponto de entrada

Na referência, o AGENTS reúne três regras centrais: MVT com services, views derivadas de `View` e services sem dependência de HTTP. Depois aponta para o estado, a arquitetura, as specs e as skills aplicáveis. Essa concisão facilita ler o arquivo antes de iniciar uma tarefa.

O que preservar na adaptação:

- Instruir a leitura do estado atual e da arquitetura antes de alterar o projeto.
- Relacionar cada tipo de mudança ao documento ou skill correspondente.
- Exigir leitura da spec da funcionalidade antes de implementá-la.
- Indicar como encerrar uma tarefa e atualizar o estado.
- Manter links e caminhos válidos em vez de copiar grandes blocos dos documentos referenciados.

O que ainda depende de escolha: a adoção exata de MVT com services, a restrição a classes `View`, o uso de templates e as exceções de acesso ao ORM. O usuário priorizou a organização documental; isso não resolve automaticamente essas escolhas técnicas.

### PRD como referência de produto

O PRD do blog apresenta objetivo, perfis, requisitos agrupados por área, requisitos não funcionais, itens fora do escopo e critérios de conclusão. Ele aponta para as cinco specs relacionadas. O texto descreve comportamentos observáveis, como o rascunho não aparecer na página pública.

A skill de PRD acrescenta regras úteis: um comportamento por requisito, identificadores estáveis, ausência de decisões técnicas de implementação e atualização das specs afetadas quando o produto muda. Os status da referência são `Proposto` e `Aceito`.

Para nosso sistema:

- Usar as decisões alimentares atuais como base, preservando Fiscalização, Administrador e Estabelecimento e a supervisão por ação.
- Distinguir regras confirmadas das propostas de adiamento e reanálise.
- Preservar a identificação dos requisitos já existentes ou registrar um mapeamento explícito. Não trocar `RF001` por `RF-01` silenciosamente apenas para imitar o blog.
- Manter os requisitos de segurança rastreáveis, seja por seção própria ou por referência clara ao catálogo detalhado; o exemplo de PRD do blog não possui um catálogo RS separado.
- Levar campos, tipos, máscaras, limites, rotas e métodos para a spec correspondente. O documento acadêmico detalhado continua sendo uma fonte; não precisa ser transcrito inteiro no PRD.
- Registrar o offline completo como exclusão atual, pois foi substituído por operação online com tratamento de falha de comunicação.

Ao criar um PRD futuro, o status e o registro de aprovação devem refletir a decisão real do responsável. Não transformar um documento recém-gerado em `Aceito` por conveniência nem reabrir decisões já confirmadas como se estivessem desconhecidas.

### Skills como instruções de trabalho

A referência possui seis skills locais. São instruções em Markdown para orientar quem trabalha no repositório; não são bibliotecas instaladas no sistema nem regras executadas automaticamente pelo Django.

| Skill encontrada | Quando é consultada | Conteúdo útil para levar como referência |
|---|---|---|
| `prd` | Criar ou alterar requisitos e escopo de produto | Estrutura do PRD, verificabilidade e estabilidade dos identificadores |
| `spec` | Especificar funcionalidade ou preparar implementação | Contratos de dados e comportamento, dependências e critérios de teste |
| `adr` | Registrar ou substituir decisão estrutural | Contexto, decisão, consequências e preservação das decisões antigas |
| `python-boas-praticas` | Escrever ou revisar Python | Nomes, tipagem, exceções, responsabilidades e testes |
| `django-boas-praticas` | Trabalhar com as partes Django | Views, services, forms, modelos, migrações, ORM e Admin |
| `seguranca-owasp` | Trabalhar com acesso, entrada, configuração e segurança | Verificações de autorização, validação, sessão, logs e falhas |

O cabeçalho `name`/`description` informa o propósito e o gatilho de cada skill. No corpo ficam as instruções aplicáveis, modelos de documento e verificações. O AGENTS funciona como índice para consultá-las no momento adequado.

Na adaptação futura, será preciso revisar as versões declaradas, exemplos, comandos e limites. As skills técnicas atuais citam Python 3.12 e Django 6.1; isso é contexto do blog. Nenhuma dessas versões foi escolhida para nosso projeto por esta análise.

Também será preciso conferir se as instruções e os mecanismos da ferramenta usada reconhecem esses caminhos. Um arquivo presente em `.agents/skills/` não comprova que será carregado sem uma orientação ou integração correspondente.

O conjunto atual é um ponto de partida suficiente para organizar o trabalho. Instruções especializadas de auditoria, versionamento e arquivos podem ser acrescentadas quando houver repetição ou necessidade clara; regras específicas de uma fiscalização continuam no PRD, nas specs e na arquitetura, conforme sua natureza.

### Specs como contratos de implementação

As cinco specs da referência tratam de fundação, autenticação, posts, comentários e dados iniciais. A numeração organiza a sequência; as dependências apontam para specs anteriores. A spec de fundação define configurações, estrutura, layout-base, rotas e critérios de aceite antes dos fluxos de produto.

A skill determina que a spec seja escrita antes da implementação e que suas partes técnicas contenham detalhe suficiente para evitar decisões adivinhadas. O status é `Proposto` ou `Implementado`; os testes só recebem `[x]` quando há teste correspondente e a suíte está passando.

Os status `Implementado` encontrados nas specs do blog são declarações anteriores do repositório. Nesta análise não houve reexecução da suíte; eles não foram alterados nem usados como prova de aprovação atual.

Para uma spec futura de fundação do sistema alimentar, os assuntos mínimos a discutir são:

1. Versões e preparação do ambiente, configuração e PostgreSQL.
2. Usuário customizado e extensão necessária para perfis e vínculos.
3. Convenções dos módulos, das rotas e dos templates, se essa forma de interface for escolhida.
4. Contratos de validação, autorização e exceções.
5. Fronteiras de transação, auditoria e preservação de versões exigidas pelos próximos fluxos.
6. Política de escrita administrativa para não contornar as regras dos services.
7. Critérios verificáveis de inicialização e de testes.

Não é necessário implementar inspeção, score ou emissão de termos para apenas estruturar o projeto. É necessário evitar uma fundação que obrigue a refazer identidade, permissões e relacionamentos quando essas funções forem introduzidas.

As specs seguintes devem corresponder aos fluxos aprovados e manter a ligação com os requisitos. Não copiar a sequência posts/comentários nem definir antecipadamente a ordem definitiva de todas as funcionalidades alimentares.

### Arquitetura como referência das fronteiras

O arquivo de arquitetura da referência define quem pode fazer o quê: view coordena HTTP, form trata entrada, service aplica regras e consulta o ORM, model descreve persistência e template apresenta dados. O Admin também precisa respeitar as regras dos services.

O valor desse arquivo está em tornar essas fronteiras explícitas. Para nosso sistema, ele precisará explicar onde ficam autorização por ação, transições de inspeção, cálculo, revisão, acesso a arquivos e registro da auditoria, sem transformar todas essas operações em código de view.

Há duas nuances importantes na referência:

- Login/logout nas views são uma exceção documentada por dependerem da sessão HTTP.
- A regra ampla de que toda consulta ORM fica no service precisa distinguir consultas internas do framework, validação de `ModelForm` e consultas administrativas explícitas. A análise anterior identificou `queryset.values_list` no Admin. A regra futura deve ser precisa para ser verificável.

O teste de arquitetura existente valida herança e vínculo das rotas com `as_view()`. Não verifica todas as fronteiras descritas. Ao adotar a arquitetura, decidir quais regras terão testes automatizados e quais exigem revisão, evitando afirmar que um único teste garante toda a arquitetura.

As skills técnicas da referência dizem que `docs/arquitetura.md` prevalece sobre suas orientações genéricas quando houver divergência. Isso organiza os documentos locais; não permite ignorar instruções do usuário, nem torna aceitável uma regra de produto contraditória.

### State como memória curta de continuidade

O estado da referência pede cerca de 30 linhas, com trabalho em andamento, próximos passos e pendências. O status dos documentos fica nos próprios arquivos; o histórico completo fica no Git.

Para nosso projeto, usar esse arquivo para informar o ponto de retomada real: por exemplo, “falta definir quem designa o supervisor antes de fechar a spec de acesso”. O requisito completo continua no lugar correto e o state apenas aponta para ele.

Uma atualização útil ao concluir uma tarefa deve:

- Retirar o que foi resolvido.
- Informar o próximo passo concreto.
- Registrar bloqueios ou verificações que não foram possíveis quando forem relevantes à continuidade.
- Apontar para a análise, spec ou decisão que reúne o detalhe.
- Não registrar uma implementação ou aprovação que ainda não aconteceu.

Esta análise é um documento independente, guardado fora do repositório. No projeto futuro, o state deve apenas apontar para o material de referência que estiver disponível. As pendências de produção e interface do blog continuam sendo daquele projeto e não são uma lista automaticamente herdada pelo sistema alimentar.

### Fluxo de trabalho a preservar

1. Ler `AGENTS.md` e `docs/state.md` para entender as instruções e o ponto de retomada.
2. Consultar o PRD do produto e a arquitetura vigente.
3. Consultar as skills aplicáveis ao tipo de mudança e as specs/ADRs relacionadas.
4. Se mudar comportamento, atualizar o PRD e refletir a mudança nas specs; se mudar decisão estrutural, registrar a decisão e suas consequências.
5. Detalhar a spec com permissões, erros e critérios de verificação antes do código.
6. Implementar somente no momento em que isso for solicitado, respeitando a spec e as decisões já tomadas.
7. Executar as verificações pertinentes, registrar o resultado real e atualizar documentos e estado.

Essa é uma sequência de consulta e manutenção, não uma exigência de produzir todos os documentos novamente a cada tarefa. Se a regra já existe e continua válida, basta consultá-la e executar o trabalho autorizado.

### Exemplo de rastreabilidade para nosso domínio

O exemplo usa a regra já definida de cancelamento autorizado. Não cria novos requisitos nem resolve a identidade do aprovador.

| Artefato | O que registraria |
|---|---|
| PRD | Fiscal solicita cancelamento com justificativa; efetivação exige autorização e preserva os registros |
| ADR, se necessária | Razão da estrutura escolhida para representar designação e escopo de aprovação |
| Arquitetura | A verificação da autoridade e a mudança oficial ficam na camada de negócio; a tela não decide autorização |
| Spec | Dados do pedido e da decisão, operações, permissões, estado pendente, erros, confirmação e testes |
| Skills | Como escrever a spec e revisar acesso, transação e testes de acordo com os padrões |
| AGENTS | Quais documentos e skills ler ao trabalhar nesse fluxo |
| State | Pendência concreta de decidir a autoridade aprovadora ou indicação da próxima tarefa após a entrega |

### Cuidados para não perder coerência

- O PRD do blog marcado como aceito não aprova um PRD alimentar futuro.
- Uma decisão nossa já confirmada, como PostgreSQL, não volta a ser desconhecida por existir SQLite na referência.
- Copiar o formato não implica copiar todos os requisitos, exclusões e limitações.
- Um checklist marcado como concluído não substitui evidência real de teste.
- Mudança de requisito exige revisar specs dependentes; mudança arquitetural exige revisar arquitetura, ADRs e instruções afetadas.
- Regras de produto, padrões técnicos e estado temporário devem permanecer distinguíveis para que uma atualização não produza três versões conflitantes da mesma decisão.

### Referências analisadas

- `AGENTS.md:1-24` e `CLAUDE.md`.
- `docs/prd/0001-blog.md`.
- `docs/specs/0001-fundacao.md` a `0005-publicacoes-iniciais.md`.
- `docs/arquitetura.md:20-51` e `docs/state.md`.
- `.agents/skills/prd/SKILL.md:8-64`.
- `.agents/skills/spec/SKILL.md:8-69`.
- `.agents/skills/adr/SKILL.md:8-57`.
- `.agents/skills/python-boas-praticas/SKILL.md`, `django-boas-praticas/SKILL.md` e `seguranca-owasp/SKILL.md`, lidas na análise anterior e conferidas quanto a propósito e contexto.

As referências são localizadores textuais do repositório analisado. Este aprofundamento foi reunido neste arquivo separado; os arquivos originais do projeto de referência permanecem preservados.


<a id="analise-tecnica"></a>

## Análise do projeto labiv20262

Data: 09/11/2026. Escopo: análise de referência para a futura fundação do Sistema de Avaliação de Segurança Alimentar. Nenhuma implementação foi solicitada ou realizada.

### Conclusão

O projeto é um blog Django organizado e útil como referência de estrutura, documentação e testes. A separação entre interface e regras de negócio pode orientar nosso sistema. O domínio de publicações, as permissões por autor e o armazenamento em SQLite atendem a outro produto e precisam ser substituídos por decisões próprias do sistema de fiscalização.

A recomendação é preservar os padrões úteis e elaborar a fundação do sistema alimentar a partir dos requisitos aprovados. Não há decisão nesta análise de converter este repositório, copiar sua implementação ou iniciar um novo projeto.

### Referência e limites da verificação

- Repositório analisado: `/Users/fabiomarques/Documents/labiv20262`.
- Arquivo indicado no editor: `docs/prd/0001-blog.md`.
- Revisão Git: `e529c4028ba86add646336ad52f18fcae959ee1c`.
- Situação inicial: sem alterações indicadas por `git status --porcelain`.
- Inventário inicial: 86 arquivos versionados, 54 arquivos Python e 93 métodos de teste declarados em nove arquivos.
- Fontes lidas: AGENTS, CLAUDE, estado, arquitetura, PRD, cinco especificações, quatro ADRs, orientações locais, configurações, modelos, migrações, services, views, formulários, rotas, Admin, templates, CSS, comando de dados iniciais e testes.
- Análise estática: leitura e comparação entre código e documentos. Não houve navegação no sistema, instalação de dependências, alteração de banco, geração de migrações ou execução de comandos de escrita da aplicação.
- Limitação de ambiente: o Python encontrado no terminal é 3.9.6 e não possui Django. O runtime auxiliar consultado também não possui Django. Não foi encontrado `.venv/bin/python` no projeto. A orientação local declara Python 3.12; o arquivo de dependências declara Django 6.1.3. Essas declarações não comprovam a existência de ambiente compatível instalado.
- Não foram executados a suíte Django, `check`, `check --deploy` nem validação de migrações. Os 93 testes foram identificados no código; não há resultado de aprovação desta execução.
- Não foi feita auditoria de vulnerabilidades das versões das dependências nem consulta a serviços externos.

Um inventário de integridade foi usado para conferir a revisão de referência e a preservação dos arquivos. As contagens e a revisão analisada estão registradas neste documento.

### O produto encontrado

O PRD aceito descreve um blog com três formas de uso: visitante, autor e administrador. Visitantes leem publicações e enviam comentários. Usuários autenticados mantêm seus próprios posts, inicialmente em rascunho. Administradores gerenciam contas e moderam comentários pelo Django Admin.

Existem listagem paginada, URLs por slug, edição, publicação, retorno a rascunho, exclusão confirmada, comentários pendentes de aprovação e um comando para criar publicações iniciais. A exclusão física de posts e comentários é parte do escopo do blog.

API REST, envio de imagens, implantação em produção, recuperação de senha na interface e limitação automática de tentativas ficaram fora do PRD dessa versão. Essas exclusões pertencem ao blog e não se transferem para nosso projeto.

### Estrutura e responsabilidades

| Área | Organização observada | Uso como referência |
|---|---|---|
| `core/` | Configuração Django, URLs de entrada, ASGI e WSGI | Organização do projeto e pontos de configuração |
| `contas/` | Usuário customizado, login, logout, Admin e testes | Início do módulo de identidade, sujeito ao desenho dos nossos perfis |
| `posts/models/` | Post e comentário, relacionamentos, índices e constraint | Exemplos de persistência e integridade, sem reaproveitar o domínio |
| `posts/services/` | Consulta, escrita, publicação, moderação e dados iniciais | Organização por caso de uso, sem dependência de HTTP |
| `posts/views/` | Classes derivadas de `View`, formulários e respostas HTTP | Padrão explícito de interação entre tela e service |
| `posts/forms/` | Campos de entrada declarados e validação de formulário | Separação da entrada permitida e dos dados controlados pelo servidor |
| Templates e CSS | Páginas renderizadas no servidor, herança, mensagens e paginação | Referência de composição; não comprova adequação visual ao uso em inspeções |
| `docs/` | PRD, especificações numeradas, ADRs, arquitetura e estado | Padrão de documentação e continuidade do trabalho |

O fluxo documentado e predominante no código é URL → view → formulário/service → ORM/model → template ou redirecionamento. O formulário trata entrada, a view coordena HTTP e o service concentra as operações de negócio. Login e logout são executados nas views por dependerem da sessão HTTP, conforme exceção registrada na ADR 0002.

Essa organização mantém o projeto pequeno e compreensível. Sua adoção no sistema alimentar é uma recomendação a validar, com atenção às operações que coordenam vários registros e arquivos.

### Tecnologias declaradas e configuração observada

| Item | Evidência | Situação da análise |
|---|---|---|
| Python | Orientação local de boas práticas declara 3.12 | Versão de referência documental; ambiente do projeto não demonstrado |
| Django | `requirements.txt`: `Django==6.1.3` | Dependência declarada; instalação não verificada |
| Dependências adicionais | `asgiref==3.13.0` e `sqlparse==0.6.1` | Fixadas no arquivo, sem auditoria de segurança nesta tarefa |
| Banco | `core/settings.py:81`: SQLite em `db.sqlite3` | Escolha expressa na ADR 0004 do blog |
| Interface | Django Templates, HTML e CSS local | Sem cliente JavaScript ou API separado identificado nos arquivos versionados |
| Usuário | `AUTH_USER_MODEL = 'contas.Usuario'` | Modelo baseado em `AbstractUser` |
| Idioma e tempo | `pt-br`, `America/Maceio`, `USE_TZ = True` | Configurações alinhadas ao contexto local |
| Segredo | Variável `DJANGO_SECRET_KEY` e fallback temporário em desenvolvimento | `.env.example` informa que o carregamento é manual |
| Produção | `DEBUG = True`, `ALLOWED_HOSTS = []` | Configuração de desenvolvimento, coerente com o escopo declarado do blog |

Não foram identificados README de preparação do ambiente, declaração executável da versão de Python, pipeline em `.github/`, contêiner ou configuração PostgreSQL no inventário versionado. A ausência foi verificada neste repositório, não em toda a máquina ou em outros serviços.

### Pontos que podemos aproveitar

#### Documentação antes e junto da implementação

O PRD informa objetivo e escopo; as especificações detalham fluxos e critérios; as ADRs justificam decisões; `docs/arquitetura.md` define responsabilidades; e `docs/state.md` mantém pendências de continuidade. O `AGENTS.md` aponta a ordem de leitura.

Esse conjunto é especialmente útil para nosso sistema, pois evita que decisões antigas de offline ou de cancelamento prevaleçam sobre as regras atuais. Recomenda-se adotar a organização, com documentos próprios e identificadores vinculados aos requisitos alimentares.

#### Services independentes de HTTP

Os services consultados não recebem `request` nem retornam resposta HTTP. As views traduzem falhas de domínio para respostas, preservando a causa da exceção. O comando de dados iniciais também usa services.

No sistema alimentar, esse padrão pode concentrar autorização, conclusão, cancelamento, correção, cálculo e emissão. O contexto de autorização deverá chegar ao service por dados explícitos, com ator e escopo confiáveis.

#### Autorização sobre o objeto

`PostService.obter_do_autor`, em `posts/services/post.py:49`, filtra por identificador e autor. As operações de edição, publicação e exclusão passam por essa busca. Os testes incluem visitante, dono e outro autor.

O princípio é aproveitável, mas nosso caso exige mais dimensões: estabelecimento vinculado, participação na equipe, designação vigente de supervisor e ação específica. Autenticação isolada não representa essas permissões.

#### Proteções de entrada e apresentação

Os formulários declaram campos aceitos. O autor e o estado inicial do post são controlados pelo servidor. Templates exibem textos com autoescape e formulários POST contêm CSRF. O login valida o destino de redirecionamento e a saída usa POST.

Esses são controles identificados no código e em testes declarados, não uma certificação de segurança. O sistema alimentar adiciona upload de arquivos e documentos privados, que não existem no blog.

#### Integridade e testes orientados a comportamento

O modelo Post exige data quando publicado, mantém slug único e define índice para listagem. Há testes de constraint, autorização, paginação, limite de entrada, escape, moderação e fluxos por rotas. A consulta de publicações usa `select_related` e possui teste de quantidade de consultas.

O padrão de verificar invariantes é útil para preservar checklist inicial, vincular aprovação ao pedido, impedir alteração de resultado sem autorização e manter relações entre correção e termo.

### Pontos de atenção encontrados

Os itens abaixo distinguem limitações aceitas pelo blog, divergências pontuais de organização e lacunas para o sistema alimentar. Não são apresentados como explorações comprovadas.

| Item | Evidência | Consequência e encaminhamento futuro |
|---|---|---|
| Configuração de desenvolvimento | `core/settings.py:26`, `:30`, `:32`; pendência em `docs/state.md` | Antes de qualquer operação real, decidir configuração por ambiente, chave estável, hosts, cookies, HTTPS e verificações de implantação. Não copiar os valores de desenvolvimento para produção. |
| Banco diferente do aprovado para nosso projeto | `core/settings.py:83`; ADR 0004 | SQLite é decisão do blog. PostgreSQL continua confirmado para segurança alimentar; preparar ambiente e testes para o banco real desde a fundação futura. |
| Identidade sem perfis de domínio | `contas/models/usuario.py:4`; PRD do blog | O modelo apenas estende `AbstractUser`. `is_staff` e `is_superuser` não representam nossos três perfis nem supervisão por ação. |
| Moderação sem contexto próprio de aprovação | `posts/services/comentario.py:21` | A aprovação recebe IDs; a permissão é verificada no Admin. Para fiscalização, o próprio caso de uso precisa verificar ator, pedido, escopo e designação, mesmo quando chamado fora da interface. |
| Edição e exclusão destrutivas previstas | `posts/services/post.py:65`, `:93`; `posts/models/comentario.py:7` | Adequadas ao escopo do blog. Não transportar para inspeções concluídas, evidências ou termos, que exigem histórico e preservação. |
| Concorrência de slug reconhecida | `posts/services/post.py:14`; Spec 0003 | A consulta antes de criar pode disputar o mesmo slug; o banco impede duplicação, mas a spec aceita `IntegrityError`. Não é um tratamento suficiente para confirmação/reenvio de operações oficiais. |
| Teste de arquitetura cobre parte das regras | `posts/tests/test_arquitetura.py:29` | Verifica herança e rotas por `as_view()`. Não prova ausência de ORM fora de services, cobertura das permissões ou atomicidade dos fluxos. |
| Consulta explícita fora de service | `posts/admin.py:45` | A ação usa `queryset.values_list` antes de chamar o service, apesar da formulação estrita de “toda consulta ao ORM nos services”. É uma divergência pontual a esclarecer na arquitetura futura, sem afirmar falha de acesso. |
| Validações de entrada apoiadas no formulário | `posts/forms/comentario.py`; `posts/services/comentario.py:16` | O fluxo web valida tamanho e campos. Não presumir que toda chamada direta a um service valida as mesmas entradas; definir contratos e invariantes para comandos, Admin e futuras integrações. |
| Login sem limitação e registros de segurança pendentes | PRD, seção fora do escopo; `docs/state.md` | Riscos já reconhecidos pelo projeto. Definir tratamento conforme os requisitos de segurança do nosso sistema, antes de operação real. |
| Ausência dos mecanismos específicos da inspeção | Inventário de modelos, services e arquivos | Upload privado, trilha de domínio, checklist versionado, cálculo, PDF versionado e recuperação de envio precisarão de desenho próprio. |

#### Observações sobre segurança

A configuração de desenvolvimento se relaciona à categoria de configuração insegura quando exposta em produção; não foi constatada exposição pública. Os pontos de autorização por ação e auditoria são necessidades do novo domínio, não falhas de isolamento demonstradas no blog. Nenhum segredo real foi lido ou reproduzido nesta análise.

A proteção existente na rota de comentários possui teste com `Client(enforce_csrf_checks=True)`. Não se deve generalizar esse único teste como comprovação de CSRF em todas as rotas, nem tratar a existência de testes de escape como auditoria completa de XSS.

### Testes identificados

| Arquivo | Métodos `test_*` declarados |
|---|---:|
| `contas/tests/test_autenticacao.py` | 18 |
| `contas/tests/test_admin.py` | 2 |
| `posts/tests/test_post_service.py` | 21 |
| `posts/tests/test_post_views.py` | 20 |
| `posts/tests/test_comentarios.py` | 16 |
| `posts/tests/test_admin.py` | 8 |
| `posts/tests/test_arquitetura.py` | 2 |
| `posts/tests/test_fluxos.py` | 2 |
| `posts/tests/test_publicacoes_iniciais.py` | 4 |
| **Total identificado por análise estática** | **93** |

Os testes de fluxo usam o cliente de teste Django, não um navegador real. Não foram identificados testes de perda de rede, uploads, PDFs, PostgreSQL ou supervisão por ação, que não pertencem às funções implementadas deste blog. Contagem de testes não é percentual de cobertura.

### Comparação com o sistema de segurança alimentar

| Tema | Blog analisado | Sistema alimentar |
|---|---|---|
| Usuários | Visitante, autor e administrador; autenticação Django | Fiscalização, Administrador e Estabelecimento; supervisor designado por ação |
| Dados | Post e comentário | Estabelecimento, inspeção, checklist, resposta, evidência, pedido, decisão, resultado e termo |
| Persistência | SQLite | PostgreSQL confirmado |
| Mudanças | Autor edita e exclui seus posts | Correção concluída exige autorização, justificativa e histórico |
| Aprovação | Comentário marcado como aprovado no Admin | Pedido e decisão vinculados à ação e à mudança solicitada |
| Conteúdo externo | Texto simples de visitantes | Documentação do estabelecimento e evidências fiscais com acesso protegido |
| Versões | Slug preservado; conteúdo do post editável | Checklist inicial, resultados anteriores e PDFs emitidos preservados |
| Rede | Formulários POST e redirecionamentos | Operação online com preservação em tela, reenvio e confirmação oficial sem duplicação |
| Interface | Páginas públicas e painel de autoria | Fluxo de fiscalização em tablet/celular e visão restrita do estabelecimento |

### Recomendações para a fundação futura

1. Usar o padrão de documentação do blog como referência, criando PRD, especificação da fundação e ADRs próprios do sistema alimentar.
2. Validar MVT com services e páginas renderizadas no servidor como proposta inicial. Um cliente separado ou API permanece uma opção, não uma exigência aprovada.
3. Planejar usuário customizado antes das primeiras migrações do novo projeto e modelar perfis, vínculos e supervisão separadamente.
4. Preparar PostgreSQL e configuração de ambiente sem importar a ADR de SQLite do blog.
5. Definir desde o desenho os contratos de autorização, auditoria, transação, preservação de versões e idempotência. Não implementar todos os módulos apenas para criar a estrutura.
6. Impedir caminhos de escrita administrativa que contornem regras de inspeção, mesmo que o Django Admin seja utilizado como apoio.
7. Especificar e testar um primeiro fluxo de negócio pequeno após a fundação; não confundir a tela genérica de CRUD com inspeção concluída e emitida.

A referência prática de retomada é [base-futura-fundacao-seguranca-alimentar.md](#memoria-para-fundacao). Ela reúne decisões confirmadas, propostas e o que precisa ser definido antes de implementar.

O foco prioritário solicitado depois da análise inicial está aprofundado em [organização documental para a fundação](#organizacao-documental): PRD, skills, specs, arquitetura, estado e AGENTS, com seus papéis, conexões e cuidados de adaptação.

### O que foi salvo e o que não foi realizado

Esta entrega reúne somente a análise e a memória para a fundação futura em um arquivo independente. O repositório de referência permanece preservado.

Nenhum módulo foi criado ou adaptado, nenhum PRD/spec/ADR aceito foi modificado, nenhuma dependência foi instalada, nenhum banco foi migrado e nenhum commit ou publicação foi feito.


<a id="memoria-para-fundacao"></a>

## Memória para a futura fundação do sistema

Atualização: 09/11/2026. Projeto: Sistema de Avaliação de Segurança Alimentar. Situação: análise concluída; fundação ainda não implementada.

### Como usar este registro

Antes de planejar a fundação, ler esta memória, a [análise da referência](#analise-tecnica) e os requisitos revisados do sistema alimentar. Depois conferir se houve decisões posteriores. Este registro preserva contexto; não aprova tecnologias adicionais nem resolve políticas que continuam em aberto.

Prioridade expressa pelo usuário após a análise inicial: focar especialmente em PRD, skills, specs, `arquitetura.md`, `state.md` e `AGENTS.md`. A análise detalhada dessa organização está em [organização documental para a fundação](#organizacao-documental) e deve ser lida antes de preparar os documentos do novo projeto.

Esses arquivos serão a referência principal de organização do trabalho. O PRD guarda comportamento; a spec, contratos de implementação; a arquitetura, fronteiras e regras técnicas; as skills, instruções por tipo de tarefa; o AGENTS, o roteiro de consulta; e o state, o próximo ponto de retomada. ADRs preservam a razão das decisões. A prioridade documental não aprova automaticamente as escolhas técnicas específicas do blog.

O projeto de referência está em `/Users/fabiomarques/Documents/labiv20262`, revisão `e529c4028ba86add646336ad52f18fcae959ee1c`. Trata-se de um blog com Django, services, templates e SQLite. Sua organização pode orientar o trabalho, mas suas regras de produto não substituem as regras sanitárias.

Os documentos alimentares mais recentes disponíveis nesta análise são:

- `Documento_Requisitos_Python_Django_Revisado.docx` e `.pdf`: 28 RF, 14 RNF e 16 RS, incluindo proposta de reanálise e fluxo de adiamento pendente.
- `Documentacao_Geral_Projeto_Seguranca_Alimentar.docx` e `.pdf`: visão geral, funcionamento, dados, arquitetura proposta, riscos e planejamento.
- Local de consulta: `/Users/fabiomarques/.codex/.chatgpt-projects/g-p-6ae127df829481919e48ee327d3267ea/deliverables/`.

### Decisões já confirmadas do nosso projeto

1. Linguagem Python e framework Django. A escolha anterior de Java foi substituída.
2. Banco PostgreSQL. A opção SQLite do blog não vale para nosso sistema.
3. Sistema web por navegador, utilizável em tablets e celulares, com servidor remoto ou nuvem.
4. Operação somente online; o offline completo descrito no PDF inicial foi substituído.
5. Três perfis-base: Fiscalização, Administrador e Estabelecimento, também chamado cliente.
6. Supervisor é fiscal designado para uma ação, com responsabilidade contextual. Pode mudar entre ações e não constitui quarto perfil nem cargo permanente.
7. Administrador pode atribuir inspeção; fiscal também pode iniciá-la diretamente. O início não concede supervisão automática.
8. No início, preservar a versão do checklist e das regras utilizadas.
9. Cancelamento em andamento exige justificativa e autorização antes de ser efetivado. A regra anterior de cancelamento apenas justificado foi substituída.
10. Correção após conclusão exige autorização, justificativa e histórico. O preenchimento normal em andamento continua previsto; outras mudanças sujeitas a autorização nessa etapa ainda serão delimitadas.
11. Recalcular automaticamente, quando a correção afetar a avaliação, usando as regras originais e registrando resultado anterior e novo.
12. Preservar o termo emitido e gerar nova versão ou termo retificador quando aplicável, com vínculo ao anterior.
13. Estabelecimento envia documentos próprios e consulta seus envios e resultados finais liberados. Não recebe acesso ao checklist em elaboração nem às deliberações internas.
14. Na perda de comunicação, bloquear temporariamente ações dependentes do servidor, preservar o preenchimento atual em tela e tentar enviar após reconexão. Só indicar salvo após confirmação do servidor.
15. PDF pode ser gerado depois do salvamento no servidor. Falha na geração não apaga a inspeção salva.

### Propostas técnicas que continuam sem aprovação

| Proposta | Razão para considerar | Limite da proposta |
|---|---|---|
| Aplicação Django única, organizada por domínio | Menos componentes para a equipe operar e separação compreensível | Não constitui escolha por microserviços ou API separada |
| MVT com services independentes de HTTP | Regras reutilizáveis em telas, Admin e comandos | Requer contrato explícito de autorização, validação e exceções |
| Views de classe derivadas de `View` | Fluxo explícito, igual à referência analisada | É regra do blog; adotá-la no novo projeto exige decisão própria |
| Templates Django e melhoria gradual da interação | Caminho inicial simples para aplicação web | Deve ser validado para formulários extensos, câmera, uploads e perda de rede |
| Usuário customizado desde a primeira migração | Permite planejar identidade e vínculos desde o começo | Campos, identificadores e política de autenticação ainda precisam de definição |
| PRD, specs, ADRs e arquivo de estado | Mantém razões e decisões acessíveis no futuro | Não copiar requisitos e ADRs do domínio do blog como se fossem nossos |

### Organização de módulos a considerar

Nomes e fronteiras abaixo são propostas, não diretórios criados:

| Área | Responsabilidade |
|---|---|
| Configuração do projeto | Ambientes, rotas principais, idioma, fuso e inicialização |
| Contas e acesso | Identidade, perfis-base e vínculos com estabelecimentos |
| Estabelecimentos | Cadastro e situação das unidades avaliadas |
| Fiscalização | Ações, inspeções, equipe e designação de supervisão |
| Checklists | Itens, respostas possíveis, pesos, regras e versões |
| Execução | Respostas, irregularidades e evidências da inspeção |
| Autorizações | Pedidos e decisões de alteração/cancelamento; outros fluxos após validação |
| Documentos | Envios do estabelecimento, arquivos privados e termos versionados |
| Resultados | Pontuação, classificação e recálculo pelas regras originais |
| Auditoria | Eventos de domínio e vínculo entre decisões e mudanças |

A fundação não precisa criar um app vazio para cada área. Primeiro definir o usuário, a configuração, os contratos comuns e o primeiro fluxo; os módulos podem ser introduzidos conforme o escopo aprovado. Ação e inspeção não devem ganhar relacionamento físico definitivo antes de resolver seu significado.

### Contratos que a fundação deverá prever

#### Autorização e isolamento

Os casos de uso devem receber um ator confiável e verificar perfil, vínculo, escopo e designação vigente, conforme a operação. Conhecer o ID de um estabelecimento, inspeção, arquivo ou pedido não concede acesso. Autoridade administrativa de negócio, acesso ao Django Admin e superusuário técnico são conceitos diferentes.

O supervisor não deve ser representado apenas por um booleano global no usuário. O desenho precisa associar sua responsabilidade à ação e manter o histórico de substituição ou revogação.

#### Regra de negócio e acesso HTTP

Se adotado o padrão de services, views tratam HTTP, formulários validam formato e services preservam invariantes de negócio em todas as entradas. Mudanças de estado não devem depender exclusivamente de uma tela, de um formulário ou de uma ação do Admin. Exceções previsíveis devem ser específicas e traduzidas pela camada de apresentação.

#### Consistência e auditoria

Aplicação de correção, resultado associado e evento de auditoria devem ter um desenho consistente de persistência. Operações com múltiplas escritas dependentes precisam de transações; conflitos devem ser tratados, sem sobrescrever silenciosamente o que outro fiscal acabou de alterar.

Uma transação do banco não torna automaticamente atômico o armazenamento externo de arquivos. Prever o que acontece se o arquivo chegar e o vínculo falhar, ou se o banco confirmar e a geração do PDF falhar.

#### Confirmação e repetição de envio

Separar a situação oficial da inspeção, a decisão de autorização e o estado de envio da interface. Um pedido pendente não equivale a cancelamento; um arquivo selecionado não equivale a recebido; a presença de internet não comprova que o servidor confirmou a operação.

Prever identificação de operação e resposta consistente na retentativa. Um simples formulário POST ou um teste que publica duas vezes não comprova idempotência para concorrência, perda de resposta ou reenvio após reconexão.

#### Versões e arquivos

Preservar a referência inicial do checklist, os resultados anteriores e os termos emitidos. Separar evidência fiscal de documento enviado pelo estabelecimento, mantendo origem, autoria e vínculos. Estratégia de armazenamento, acesso privado, validação e retenção ainda serão escolhidos.

### Decisões pendentes antes ou durante o planejamento

| Tema | Pergunta que continua aberta |
|---|---|
| Repositório de destino | Será criado projeto novo ou haverá adaptação explícita do blog? Esta análise não escolhe. |
| Ambiente | Quais versões de Python, Django e PostgreSQL serão usadas e como preparar o ambiente? |
| Perfis e usuário | Como representar os três perfis e o vínculo de usuários aos estabelecimentos? |
| Ação e inspeção | Uma ação corresponde a uma inspeção ou pode agrupar várias? |
| Supervisão | Quem designa, substitui e encerra? Quantos supervisores por ação e qual vigência? |
| Aprovação | Quem decide cancelamento e alteração, quem substitui na ausência e como tratar pedido do próprio supervisor? |
| Mudanças em andamento | Quais operações além do preenchimento normal exigem autorização? |
| Adiamento | Exige aprovação? Existe estado Adiada e como ocorre a retomada? |
| Reanálise | Quais documentos novos a provocam, quem analisa e quando exige visita? |
| Checklist e cálculo | Qual referência sanitária, fórmula, pesos, N/A, arredondamento e classificação? |
| Documentação do cliente | Tipos, formatos, tamanhos, prazos, complementação e substituição de anexos? |
| Resultado e termo | Quando liberar ao estabelecimento, modelos, numeração, assinatura, ciência e retificação? |
| Infraestrutura | Provedor, armazenamento, PDF, autenticação, cópias de segurança e monitoramento? |
| Interface | Templates ou cliente separado, navegadores e dispositivos homologados? |
| Dados e capacidade | Metas de desempenho, volume, retenção, recuperação e orçamento? |

Ausência de resposta não autoriza preencher essas escolhas como fatos. Decisões não bloqueantes podem ficar documentadas para uma fase seguinte; decisões que afetam usuário inicial, autorização e integridade devem ser tratadas antes de consolidar o respectivo modelo.

### Ordem sugerida para uma próxima tarefa

1. Confirmar o destino do código e revisar os documentos atuais do sistema alimentar.
2. Elaborar PRD próprio, especificação da fundação e ADRs das escolhas realmente aprovadas.
3. Definir ambiente, configuração por ambiente, PostgreSQL e usuário inicial antes das primeiras migrações.
4. Especificar perfis, vínculos e o contrato de supervisão por ação, sem assumir políticas de aprovação ainda abertas.
5. Preparar os padrões de validação, autorização, exceções, auditoria e consistência das operações.
6. Definir testes de aceite da fundação e do primeiro fluxo, usando PostgreSQL e dados de teste isolados.
7. Somente após autorização de implementação, criar a fundação e depois o primeiro fluxo vertical de inspeção.

Não foram definidos prazo, orçamento ou cronograma de implementação nesta análise.

### Critérios para avaliar a futura fundação

Estes são critérios propostos para especificação futura, não testes executados agora:

- Ambiente reproduzível, com versões declaradas, segredo externo e ausência de configuração insegura na operação real.
- Inicialização em banco PostgreSQL novo com o modelo de usuário escolhido.
- Separação entre autenticação, perfil de negócio e supervisão contextual.
- Negação de acesso a dados de outro estabelecimento e à ação fora da designação vigente.
- Padrão comum de validação e falhas de domínio, sem caminhos administrativos que contornem autorização.
- Possibilidade de ligar um evento auditável ao ator, ao objeto e à decisão.
- Definição dos contratos de versão e confirmação para os próximos fluxos; testes de rede e PDF na etapa em que essas funções existirem.
- Documentos de arquitetura, decisões e estado coerentes com a implementação efetivamente entregue.

### O que evitar copiar da referência

Não transferir o domínio `posts`, os textos de exemplo, SQLite, o acesso público do blog, a equivalência entre usuário autenticado e autor, o controle só por dono, a aprovação sem ator no contrato, a exclusão em cascata de conteúdo oficial, o `DEBUG` fixo ou a ausência de limites de uso por estarem aceitos no blog.

O que vale preservar como aprendizado é o encadeamento entre documentação, separação de responsabilidades, validações, consultas com escopo e testes de comportamento.

### Limitação desta memória

Ela consolida a análise estática da referência e as decisões do sistema alimentar disponíveis em 09/11/2026. Os 93 testes do blog foram lidos/identificados, mas não executados por falta de Django no ambiente disponível. Nenhuma fundação, migração, dependência ou funcionalidade foi implementada nesta tarefa.
