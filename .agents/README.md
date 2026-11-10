# Skills e agentes do projeto

As skills orientam como executar uma tarefa. Os agentes delimitam uma especialidade para trabalho delegado. Usar o material conforme o pedido atual, as [etapas](../docs/etapas.md) e as decisões do projeto; instalar instruções não inicia a aplicação.

## Preferência de uso e economia de tokens

Orientação do usuário em 10/11/2026: adotar Caveman como padrão das respostas da conversa, com texto curto e direto. Preservar informações necessárias e o detalhamento solicitado nos documentos, requisitos, specs e demais artefatos. A concisão da conversa não autoriza reduzir o conteúdo das entregas.

Usar Graphify nas análises recorrentes de relações entre arquivos, requisitos e arquitetura, consultando primeiro um grafo existente. Na ausência de grafo, buscas pontuais continuam adequadas para perguntas simples; construir o mapa quando sua reutilização ou a análise estrutural justificar o custo inicial. Não reconstruí-lo em toda tarefa. A economia depende da tarefa e não é garantida. A tentativa da Etapa 6 está no [registro do Graphify](../docs/registro-graphify.md); a extração não retornou fragmentos completos e o mapa permanece pendente.

As duas skills estão no catálogo global do ambiente, em `/Users/fabiomarques/.codex/skills/caveman/SKILL.md` e `/Users/fabiomarques/.codex/skills/graphify/SKILL.md`; não são cópias locais das 11 skills listadas abaixo. Aplicar também as skills específicas da tarefa e distinguir sua consulta da execução de agentes. Mantém-se a autorização de uma etapa por vez.

## Skills locais

| Skill | Quando consultar |
|---|---|
| [prd](skills/prd/SKILL.md) | Produto, escopo e requisitos; preservada da fundação |
| [adr](skills/adr/SKILL.md) | Decisões estruturais e suas razões; preservada da fundação |
| [spec](skills/spec/SKILL.md) | Contratos técnicos e verificação futura; preservada da fundação |
| [planejamento](skills/planejamento/SKILL.md) | Plano e dependências de uma mudança solicitada |
| [atas-reuniao](skills/atas-reuniao/SKILL.md) | Notas, decisões, propostas e ações de reunião |
| [python-boas-praticas](skills/python-boas-praticas/SKILL.md) | Código Python, efeitos e tratamento de falhas |
| [django-boas-praticas](skills/django-boas-praticas/SKILL.md) | MVT, services, ORM, PostgreSQL, migrações e Admin |
| [seguranca-aplicacao](skills/seguranca-aplicacao/SKILL.md) | Autorização, sessão, arquivos e proteção de dados |
| [testes](skills/testes/SKILL.md) | Cenários, execução e evidências, inclusive no navegador |
| [revisao-codigo](skills/revisao-codigo/SKILL.md) | Defeitos e regressões em alterações implementadas |
| [interface-web](skills/interface-web/SKILL.md) | Telas em Templates, acessibilidade e comportamento de envio |

## Revisão integrada das skills técnicas

Na Etapa 7, as skills de Python, Django e segurança foram comparadas às três specs e ajustadas para suas exceções, contratos e decisões abertas. O [registro da revisão](../docs/revisao-skills-tecnicas.md) apresenta lacunas tratadas e verificações documentais. Nomes/licenças e os seis perfis TOML foram preservados; a revisão não comprova execução dos agentes, descoberta automática ou implementação.

## Agentes especializados

| Agente | Função | Arquivo |
|---|---|---|
| analista_documentacao | Analisar ou redigir os documentos solicitados | [perfil](../.codex/agents/analista_documentacao.toml) |
| especialista_django | Especificar ou implementar o backend autorizado | [perfil](../.codex/agents/especialista_django.toml) |
| revisor_dados | Revisar ORM, migrações e consistência, sem edição | [perfil](../.codex/agents/revisor_dados.toml) |
| revisor_seguranca | Revisar acesso, sessão e arquivos, sem edição | [perfil](../.codex/agents/revisor_seguranca.toml) |
| revisor_qualidade | Revisar alterações e testes, sem implementar correção | [perfil](../.codex/agents/revisor_qualidade.toml) |
| especialista_interface | Especificar ou implementar a interface autorizada | [perfil](../.codex/agents/especialista_interface.toml) |

Os perfis seguem o formato de agentes locais do Codex em `.codex/agents`, com nome, descrição e instruções. Herdam as permissões e ferramentas da sessão; a orientação de revisão sem edição não cria um isolamento técnico adicional. Não foi alterado modelo ou habilitada execução paralela global. [Documentação oficial de agentes](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

Exemplo de pedido: “Use o revisor_dados para analisar a spec de fundação, sem alterar arquivos.” O agente principal deve fornecer recorte e resultado esperado, sem delegar automaticamente todos os trabalhos. A curadoria validou os arquivos; não comprova que esta sessão já os carregou ou que houve execução dos agentes.

O [registro da curadoria](../docs/curadoria-skills-agentes.md) explica seleção, descartes, origens e adaptações. Avisos de terceiros estão em [NOTICE](third-party/NOTICE.md). O [estado](../docs/state.md) e a [rotina do Trello](../docs/acompanhamento-trello.md) guardam a continuidade. [AGENTS](../AGENTS.md), [CLAUDE](../CLAUDE.md) e [README da raiz](../README.md) foram elaborados na Etapa 8 e apontam para este catálogo. A [revisão final](../docs/revisao-final-fundacao.md) não comprova carregamento automático ou execução dos perfis.
