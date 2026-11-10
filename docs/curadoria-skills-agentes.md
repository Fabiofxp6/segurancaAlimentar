# Curadoria de skills e agentes

Realizada em 10/11/2026, por solicitação do usuário após a Etapa 4: examinar as duas pastas awesome, aproveitar o material pertinente, descartar o restante e organizar as instruções locais. É uma atividade adicional autorizada; não inicia a spec de autenticação ou a implementação.

## Resultado

O projeto passa a ter **11 skills locais**: as três de PRD, ADR e specs preservadas, mais oito adaptadas. Também recebe **seis agentes especializados** no formato do Codex. O [catálogo de uso](../.agents/README.md) liga todos os arquivos e indica quando consultar cada um.

| Coleção examinada | Inventário | Aproveitamento |
|---|---|---|
| Awesome Codex Skills | 880 skills: 48 gerais e 832 de integrações | Três fontes para planejamento, testes web e referência conceitual de atas |
| Awesome Claude Agents | 33 agentes | Nove fontes adaptadas, consolidadas nas skills e em seis perfis locais |

A revisão usou o catálogo, metadados e leitura dirigida dos candidatos e suas orientações, incluindo exemplos quando afetavam a compatibilidade. Não foram executados instaladores, scripts, comandos de exemplos ou agentes da coleção. O [manifesto](curadoria-skills-agentes.json) registra revisões, fontes selecionadas, seus hashes, destinos e os descartes gerais; as 832 integrações são registradas como grupo.

## Seleção e adaptação

| Fonte aproveitada | Destino principal | Adaptação ao projeto |
|---|---|---|
| create-plan | planejamento | Etapa e autorização atuais, plano salvo quando solicitado e Trello |
| meeting-notes-and-actions | atas-reuniao, com redação local própria | Separar decisão/proposta e não inventar prazo ou responsável |
| webapp-testing | testes | Ferramentas disponíveis e resultado observado; sem instalação automática ou espera de rede como prova universal |
| python-expert | python-boas-praticas e especialista_django | Retirar FastAPI/SQLAlchemy, versão fixa e exemplos alheios |
| django-backend-expert | django-boas-praticas e especialista_django | View, services, sessão e limites do Admin conforme arquitetura |
| django-orm-expert | django-boas-praticas e revisor_dados | PostgreSQL, integridade, versões, concorrência e consultas demonstráveis |
| security-expert | seguranca-aplicacao e revisor_seguranca | Acesso contextual; sem JWT, MFA ou política legal impostos |
| testing-expert | testes e revisor_qualidade | Sem cobertura percentual arbitrária ou ferramenta adicional obrigatória |
| code-reviewer | revisao-codigo e revisor_qualidade | Achados com evidência, sem notas artificiais ou delegação automática |
| documentation-specialist e project-analyst | analista_documentacao e apoio ao planejamento | Preservar fontes, IDs, propostas e separação entre documentos |
| frontend-developer | interface-web e especialista_interface | Django Templates, dispositivos móveis, acessibilidade e confirmação do servidor |

Os agentes de revisão não editam arquivos por suas instruções. Os perfis de documentação, Django e interface seguem o tipo de trabalho recebido: análise, documento, protótipo ou implementação expressamente autorizada. Nenhum deles transforma o estado documental atual em autorização para criar código.

## Material descartado

- As 832 automações específicas de integrações via Composio/Rube: o projeto não adotou essa camada e já possui acesso ao Trello. Não foram importadas conexões, credenciais ou ferramentas alternativas.
- Especialistas de React/Next, Vue/Nuxt, Laravel, Rails, FastAPI, aprendizado de máquina e scraping: não correspondem à base confirmada do sistema.
- Agentes de API e dependências para frontend independente: API pública, DRF, GraphQL, JWT e outro frontend não foram aprovados como base.
- Orquestradores automáticos, configuradores de equipe e especialistas redundantes: evitam impor delegação, reescrever CLAUDE ou instalar toda a coleção para um trabalho delimitado.
- Skills de marketing, vendas, currículo, finanças, mídia, comunicação genérica e serviços não adotados: não ajudam o recorte atual.
- Duplicatas de instalador/criador de skills e ferramentas de GitHub já disponíveis na sessão: não foi criada outra cópia local sem necessidade. Deploy, triagem e monitoramento específicos de fornecedor ficam fora enquanto o ambiente não for escolhido.

Essa seleção não proíbe adoção futura. Uma nova necessidade pode justificar outra avaliação, com origem e escopo próprios; não manter centenas de instruções ativas antecipadamente.

## Organização e limites

As skills ficam em `.agents/skills`. Os agentes foram convertidos do Markdown de Claude para arquivos TOML em `.codex/agents`, conforme o formato local documentado do Codex. Não foram criados modelos ou permissões de execução próprios nem alterada configuração global. [Formato oficial de agentes](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

A conferência cobre metadados, TOML, referências e compatibilidade das instruções com os documentos atuais. Não houve execução dos perfis, teste da aplicação ou comprovação de carregamento automático nesta sessão. AGENTS, CLAUDE e o README da raiz continuam no trabalho previsto da Etapa 8; o README de `.agents` é apenas o catálogo deste material.

As skills técnicas antes previstas na Etapa 7 foram preparadas agora pelo pedido explícito de curadoria. A revisão integrada com as specs de autenticação e acesso continua pendente; a etapa não é marcada integralmente concluída por antecipação. O próximo passo do plano continua sendo a Etapa 5 quando solicitada.

## Limpeza e preservação

As pastas awesome completas são retiradas da raiz após publicar e conferir o material selecionado. Cópias compactadas de recuperação foram criadas fora do projeto, preservando inclusive os arquivos locais encontrados. Não houve alteração nas fontes, no `.env`, na aplicação, no blog de referência ou nas três skills já existentes.

Os avisos e licenças aproveitados estão em [NOTICE](../.agents/third-party/NOTICE.md). As referências do levantamento alimentar continuam em seu [índice](referencias/README.md), sem alteração dos originais. O [estado](state.md), as [etapas](etapas.md) e o [Trello](acompanhamento-trello.md) registram esta atividade adicional.
