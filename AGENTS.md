# Orientações para trabalhar neste projeto

## Retomada e escopo

Leia [docs/state.md](docs/state.md) e a solicitação atual antes de agir. Consulte [docs/etapas.md](docs/etapas.md) para distinguir a entrega documental de implementação. As oito etapas da fundação foram elaboradas para revisão; isso não aprova automaticamente PRD, ADRs, specs ou políticas abertas.

Trabalhe no recorte autorizado, uma etapa ou mudança por vez. Pedido claro e já autorizado deve ser executado sem pedir confirmação repetida. Um pedido de análise/documentação não autoriza código, ambiente, instalação, migração ou implantação. Antes de implementar, confirme o recorte solicitado e resolva apenas os bloqueios que afetarem essa execução; não transforme todas as pendências do produto em pré-requisito de uma tarefa independente.

## Onde encontrar a informação

| Necessidade | Fonte principal |
|---|---|
| Situação, próximo passo e atividades | [Estado](docs/state.md), [etapas](docs/etapas.md) e [Trello](docs/acompanhamento-trello.md) |
| Escolha confirmada ou pergunta aberta | [Decisões](docs/decisoes-confirmadas.md) e [pendências](docs/pendencias.md) |
| Produto, dados, regras e aceite | [PRD](docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md) e [matriz](docs/matriz-rastreabilidade.md) |
| Camadas, responsabilidades e razões | [Arquitetura e índice dos ADRs](docs/arquitetura.md) |
| Preparação, identidade inicial e configuração | [Spec 0001](docs/specs/0001-fundacao-tecnica.md) |
| Login, logout, credenciais e sessão | [Spec 0002](docs/specs/0002-autenticacao.md) |
| Perfil, vínculo e supervisão contextual | [Spec 0003](docs/specs/0003-acesso-vinculos-supervisao.md) |
| Origem e diferenças entre documentos | [Índice de referências](docs/referencias/README.md) |
| Como executar uma especialidade | [Catálogo de skills e agentes](.agents/README.md) |

Leia os trechos pertinentes; não carregue todo o acervo para uma tarefa pontual. Preserve RF001–RF028, RNF01–RNF14 e RS001–RS016. Decisão expressa posterior atualiza somente o tema a que se refere. Documento Proposto, exemplo, protótipo ou cartão antigo não aprova campo, máscara, limite, papel ou política. Registre uma decisão nova com origem e atualize os documentos afetados, sem corrigir retroativamente as fontes.

## Base do sistema

- Python com Django e PostgreSQL; web em navegador para tablets/celulares e hospedagem remota. Versões, provedor e preparação continuam em aberto.
- MVT e Django Templates. Views próprias herdam diretamente de `View`; services fazem regra e ORM explícito sem `request`/`HttpResponse`. Forms validam entrada; templates apresentam.
- Consultas internas de autenticação, sessão, permissões, ModelForm, Admin e migrações são exceções nativas admitidas. Login/logout de sessão ficam na view; o recebimento de `request` pelo AuthenticationForm candidato não autoriza HTTP em services.
- Usuário customizado `AbstractUser`, nome de usuário/senha e sessão Django confirmados. Chave física/campos e políticas adicionais não estão escolhidos. Monólito modular e backend de sessão em banco continuam recomendações dos ADRs 0007/0008, sem aceite registrado.
- Três perfis-base: Fiscalização, Administrador e Estabelecimento. Supervisor é fiscal designado por ação. Flags técnicas, participação na equipe ou início direto de inspeção não concedem supervisão/aprovação. Autoridades, autoaprovação e relação ação/inspeção continuam abertas.
- Conferir perfil, vínculo, vigência, estado e escopo no servidor e no caso de uso que efetiva a operação, inclusive consultas/downloads e após revogação na sessão atual. O estabelecimento acessa próprios envios e resultados/documentos finais liberados, sem avaliação interna.
- Online, com preservação do preenchimento na página aberta e bloqueio temporário das ações dependentes do servidor na queda de comunicação. Tentar recuperar após reconexão, sem considerar salvo antes da confirmação ou duplicar o efeito. Mecanismo, persistência no navegador e tratamento específico de credenciais permanecem nas specs/pendências.
- Correção concluída e cancelamento em andamento exigem autorização, justificativa e história. Preservar checklist/regras originais, resultados anteriores/novos e termos já emitidos. Admin não contorna o mesmo caso de uso.

Consulte as specs para os contratos completos. Não escolher UUID, relações, cardinalidade de supervisores, fórmula, prazos, biblioteca, armazenamento ou política legal por inferência. Não copiar código, banco ou versões do blog de referência.

## Skills, agentes e economia de contexto

Consulte o SKILL.md da especialidade aplicável antes do trabalho correspondente. Use o [catálogo](.agents/README.md) para escolher PRD, ADR, spec, planejamento, atas, Python, Django, segurança, testes, revisão ou interface; leia só as skills necessárias. Descreva brevemente ao usuário o que está aplicando quando isso ajudar a acompanhar o trabalho.

Os seis perfis em `.codex/agents` delimitam tarefas especializadas, mas sua existência não prova execução nem autoriza delegar tudo. Quando a delegação estiver autorizada e for útil, forneça recorte e saída esperada, confira o retorno e preserve as restrições de revisão sem edição. O agente principal consolida continuidade e Trello. Não alegue agente executado por apenas ler seu TOML.

Responda em português, curto e direto conforme a preferência Caveman; mantenha o detalhamento pedido nos documentos. Graphify deve reaproveitar um grafo existente e atualizado quando pertinente. O mapa atual está [pendente](docs/registro-graphify.md): não o apresente como pronto. Para tarefa pontual sem grafo, use busca dirigida. Uma nova construção precisa justificar o custo e validar fragmentos antes de mesclar; não reconstruir automaticamente nem inventar economia medida.

## Preservação e verificação

Preserve as mudanças do usuário, arquivos de ambiente e configuração global. Não exponha segredos ou o corpo sensível de requisições; não leia valores reais de ambiente sem necessidade. A existência de `.env`/`example.env` não aprova seu conteúdo nem comprova carregamento. Use exemplos fictícios quando a tarefa pedir documentação de configuração.

Mantenha os originais de `docs/referencias/arquivos/` e os arquivos sincronizados de `sources/`, se houver, como referências somente de leitura. Não editar, mover, renomear ou excluir fontes; uma revisão autorizada deve ser adicionada e identificada, preservando a origem. Avisos de terceiros e manifestos históricos também devem manter a procedência.

Em documentação, conferir links, IDs, situação, pendências e coerência; não executar aplicação para simular validação inexistente. Em implementação autorizada, executar as verificações pertinentes ao comportamento real, com PostgreSQL isolado quando houver persistência e ferramentas/versões aprovadas. Não presumir comandos de instalação ou ferramenta de teste ainda não escolhidos. Verificações documentais, cenários escritos e testes executados são evidências diferentes.

Ao concluir, atualize estado (até 30 linhas), documentos afetados e o [Trello](docs/acompanhamento-trello.md), conforme DC022, com resultado, verificações reais, limitações e próximo passo. Não marcar requisito implementado ou documento aprovado pela produção do texto. Se uma atualização externa falhar, registrar a pendência de sincronização e informar; não afirmar que foi concluída.
