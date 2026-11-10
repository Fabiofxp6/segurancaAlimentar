# Etapas da fundação documental

Atualizado em: 10/11/2026. Trabalho organizado conforme pedido do usuário: uma etapa por vez. A aprovação do planejamento não autoriza executar todas em sequência. A implementação do sistema será uma fase posterior.

| Etapa | Escopo | Entrega | Situação nesta revisão |
|---|---|---|---|
| 1 | Organizar fontes e distinguir decisões e pendências | Referências, decisões, pendências e estado inicial | Concluída |
| 2 | Definir produto e escopo | Skill de PRD e PRD do sistema | Concluída para revisão do usuário |
| 3 | Definir arquitetura e escolhas estruturais | Arquitetura, ADRs iniciais e skill de ADR | Concluída para revisão do usuário |
| 4 | Especificar fundação técnica | Spec de fundação e skill de specs | Concluída para revisão do usuário |
| 5 | Especificar autenticação | Spec de autenticação e ADR de backend proposto | Concluída para revisão do usuário; documentos Propostos |
| 6 | Especificar permissões e vínculos | Spec de acesso e matriz de rastreabilidade | Concluída para revisão do usuário; documentos Propostos |
| 7 | Adaptar instruções técnicas | Skills de Python, Django e segurança | Revisão integrada concluída para revisão do usuário |
| 8 | Consolidar orientações e revisar coerência | AGENTS, CLAUDE, README do projeto e revisão final | Elaborada e conferida para revisão do usuário |

## Acompanhamento contínuo

Atualizar o Trello junto de todas as atividades do projeto, incluindo análise, documentação, decisões, implementação e verificações. Registrar resultado, situação e pendências conforme a [rotina de acompanhamento](acompanhamento-trello.md). Essa orientação vale para todas as etapas e não autoriza avançar automaticamente.

As notas de entrega abaixo registram o escopo e a situação no momento de cada atividade. Para a situação vigente, consultar a tabela acima e o [estado](state.md); indicações antigas de etapa não iniciada são históricas.

## Entrega da Etapa 1

- Fontes disponíveis copiadas e identificadas no [índice](referencias/README.md), com manifesto de integridade.
- Catálogo de origem conferido: 28 RF, 14 RNF e 16 RS, mantendo os IDs.
- Decisões anteriores e confirmações de 10/11 consolidadas em [decisões confirmadas](decisoes-confirmadas.md).
- Propostas e perguntas abertas separadas em [pendências](pendencias.md), com indicação de quando interferem no trabalho futuro.
- Estado inicial criado e limitado ao ponto de retomada.

Na Etapa 1 não foram criados PRD, skills, specs, ADRs, arquitetura ou AGENTS. O README dentro de referências é apenas o índice das fontes, não a entrega do README do projeto prevista na Etapa 8.

## Entrega da Etapa 2

- [Skill de PRD](../.agents/skills/prd/SKILL.md) local, com orientação de fontes, IDs, situação dos requisitos e limites entre documentos.
- [PRD 0001](prd/0001-sistema-avaliacao-seguranca-alimentar.md) com objetivo, perfis, restrições confirmadas, escopo e 58 requisitos com critérios de aceite previstos.
- Prioridades e políticas abertas continuam identificadas; adiamento e reanálise seguem para validação. O PRD permanece Proposto.
- [Estado](state.md) atualizado para a revisão desta entrega e a próxima etapa solicitável.

Os IDs e os links locais foram conferidos. Os critérios do PRD descrevem verificações futuras; não são testes executados do sistema. As fontes, o código, o `.env` e o blog de referência foram preservados.

## Entrega da Etapa 3

- [Arquitetura](arquitetura.md) com contexto, responsabilidades, exceções do framework/Admin, áreas lógicas propostas, acesso, confirmação, consistência e arquivos/PDF.
- Sete ADRs ligados no índice da arquitetura: 0001 a 0006 registram base confirmada; 0007 propõe monólito modular. Todos os novos registros estão Propostos para revisão documental.
- [Skill de ADR](../.agents/skills/adr/SKILL.md) com orientações de origem, alternativas, consequências, situação e substituição de decisões.
- PRD ligado à arquitetura; pendências técnicas detalhadas sem encerrar políticas abertas.
- Estado e acompanhamento no Trello atualizados. Links, IDs e integridade dos arquivos conferidos; não foram executados testes de aplicação.

O pedido de continuar a Etapa 3 autoriza sua elaboração; não equivale a aceitar integralmente o PRD ou as recomendações novas. Fontes, código, ambiente e blog permanecem preservados. As specs continuam nas etapas próprias.

## Entrega da Etapa 4

- [Spec 0001 de fundação](specs/0001-fundacao-tecnica.md), Proposta, com estrutura candidata, configuração por ambiente, PostgreSQL, usuário customizado, preparação/migrações futuras, falhas e 12 cenários de validação.
- [Skill de specs](../.agents/skills/spec/SKILL.md) com orientação de contratos, dependências, rastreabilidade parcial, situação e evidências de aceite.
- Bloqueios de ambiente, identidade e validação da estrutura associados à parte da execução que depende deles, sem encerrar pendências por inferência.
- PRD e arquitetura ligados à nova spec; pendências e registros de continuidade atualizados.
- IDs, links, estrutura documental e integridade conferidos; Trello atualizado durante a elaboração e na entrega. Nenhum cenário da aplicação foi executado.

O pedido de seguir a Etapa 4 autoriza sua elaboração, sem aceitar automaticamente o PRD, os ADRs ou os contratos candidatos. A spec não está pronta para implementação integral enquanto seus bloqueios aplicáveis permanecerem abertos. Fontes, código, ambiente e blog foram preservados.

## Entrega da Etapa 5

- [Spec 0002 de autenticação](specs/0002-autenticacao.md), Proposta, com correspondência aos campos do RF001/RS003/RS004; tipos, obrigatoriedade, normalização, limites dependentes do modelo e dados derivados no servidor.
- Contratos candidatos de forms, views diretas, rotas, métodos/respostas, destino de retorno, telas/mensagens, sessão, CSRF, conta inativa, saída, expiração e falhas no middleware.
- [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md), Proposto: recomendação nova de sessões no servidor com PostgreSQL; não aprova backend ou políticas complementares.
- Trinta e dois cenários de aceite futuro e relação local com os requisitos. Credenciais em resposta perdida e dados de outras abas dependem de P014/P020; duração, tentativas, recuperação, concorrência e revogação global continuam sem escolha.
- PRD, arquitetura, fundação, pendências e continuidade ligados à entrega; IDs, links, cobertura e integridade conferidos. Trello atualizado durante a elaboração e na entrega, mantendo revisão pendente.

A Etapa 5 entrega documentação para revisão. Nenhum teste da aplicação foi executado; não foram criados ou alterados código, dependências, ambiente, banco ou migrações. Não se aprovam automaticamente o PRD, os ADRs ou os contratos novos. A Etapa 6 não foi iniciada.

## Atividade adicional: curadoria de skills e agentes

Após a Etapa 4, o usuário solicitou analisar as duas coleções awesome, selecionar o material útil, descartar o restante e organizar os arquivos do projeto. Essa autorização específica antecipa o preparo de parte das instruções técnicas, sem iniciar as demais entregas do plano.

- Oito skills novas e seis perfis locais de agentes; as três skills anteriores foram preservadas.
- [Catálogo de uso](../.agents/README.md), [registro da seleção](curadoria-skills-agentes.md) e manifesto com origens e descartes.
- Perfis convertidos para TOML do Codex e skills adaptadas ao contexto alimentar, com avisos de terceiros preservados.
- Coleções completas retiradas após conferência; cópias compactadas de recuperação fora da pasta do projeto.
- Formatos, referências e integridade verificados; nenhuma execução de agente ou aplicação feita para validar a configuração.

A revisão das skills de Python, Django e segurança em conjunto com as specs das Etapas 5 e 6 continua pendente na Etapa 7. O catálogo em .agents não substitui AGENTS, CLAUDE ou o README da raiz previstos na Etapa 8.

## Revisão adicional do PRD

O usuário solicitou recuperar o detalhamento que havia sido resumido em excesso na versão inicial. O [PRD 0001](prd/0001-sistema-avaliacao-seguranca-alimentar.md) foi comparado a F003 e revisto nos 28 RF, 14 RNF e 16 RS, preservando os IDs.

Foram recuperadas as 183 entradas de dados dos RF com tipos, formatos e condições de referência, além de atores, condições, fluxo, regras de alteração/exclusão/consulta e aceite. RNF e RS preservam parâmetros, regras/controles, verificações e definições abertas. A [skill de PRD](../.agents/skills/prd/SKILL.md) passou a exigir cobertura desse detalhamento, mantendo contratos físicos e implementação nas specs.

Tipos sugeridos, UUID, máscaras, limites e políticas não foram aprovados pela transcrição. As confirmações posteriores sobre usuário/senha e sessão Django prevalecem sobre a fonte mais antiga. RF014 mantém o bloqueio de conclusão como proposta; RF027 e RF028 seguem para validação. PRD continua Proposto, sem código ou testes de aplicação. Revisão acompanhada no Trello.

## Entrega da Etapa 6

- [Spec 0003](specs/0003-acesso-vinculos-supervisao.md), Proposta: matriz de papéis, dados/tipos/referências de RF002/RS001/RS002, vínculos, supervisão, services, rotas, forms, falhas, revogação, concorrência e Admin.
- [Matriz completa](matriz-rastreabilidade.md) com 28 RF, 14 RNF e 16 RS: fontes, decisões, relações entre requisitos, cobertura parcial/futura e 58 cenários VR.
- Trinta e seis cenários AC futuros; autoridade, autoaprovação, agrupamento, cardinalidades e vigência permanecem nas pendências, sem concessão por inferência.
- Skills spec, Django e segurança aplicadas; Graphify executado na detecção e em uma tentativa de extração, conforme seu [registro](registro-graphify.md); mapa pendente por ausência de fragmentos finais. Sem dependências instaladas ou configuração global alterada.
- Documentação de continuidade e Trello atualizados; conteúdo dos 58 requisitos, fontes e arquivos alheios ao recorte preservados. Verificações documentais não são testes de aplicação.

O pedido de avançar autorizou somente a Etapa 6. Não criou software, migrações ou ambiente, não resolveu automaticamente as políticas abertas e não iniciou a revisão integrada da Etapa 7.

## Entrega da Etapa 7

- Skills [Python](../.agents/skills/python-boas-praticas/SKILL.md), [Django](../.agents/skills/django-boas-praticas/SKILL.md) e [segurança](../.agents/skills/seguranca-aplicacao/SKILL.md) revisadas com as três specs, preservando nomes e licenças.
- [Registro da revisão](revisao-skills-tecnicas.md) com lacunas, correspondência aos contratos, nove situações examinadas no papel e verificações de formato, referências e integridade.
- Exceções nativas de ORM/form/sessão, propostas ainda não aprovadas e acesso contextual/revogação ficaram explícitos, sem duplicar as specs ou modificar o produto.
- Catálogo, estado e Trello atualizados. Nenhum perfil TOML ou agente foi executado; não houve instalação, código, ambiente, banco/migração ou teste de aplicação. Graphify permanece pendente, sem nova extração nesta revisão.

## Entrega da Etapa 8

- [AGENTS](../AGENTS.md) com retomada seletiva, fontes, limites, invariantes, skills/agentes, preservação e rotina do Trello.
- [CLAUDE](../CLAUDE.md) como entrada que aponta para AGENTS e estado, sem uma segunda cópia das regras.
- [README da raiz](../README.md) com visão do sistema, situação real, mapa documental e decisões necessárias antes da execução.
- [Revisão final](revisao-final-fundacao.md): coerência do conjunto, pontos de retomada atualizados, links/IDs/formatos e integridade. Requisitos, dados, critérios e políticas preservados.
- Estado, índices e Trello atualizados. Sem código, dependência, ambiente, banco/migração, implantação ou teste de aplicação; Graphify continua pendente e perfis não executados.

## Retomada

As oito etapas da fundação documental foram elaboradas e conferidas para revisão. Aguardar revisão do usuário e a solicitação de uma nova atividade delimitada: decisão, ajuste documental ou recorte de implementação. Nenhuma fase posterior está iniciada. As políticas abertas e os contratos Propostos continuam sem aprovação automática.
