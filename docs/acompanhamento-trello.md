# Acompanhamento das atividades no Trello

Orientação do usuário registrada em 10/11/2026: atualizar o Trello em paralelo às atividades realizadas. Isso vale para todo o trabalho deste projeto, incluindo análise, planejamento, documentação, decisões, desenvolvimento, testes, revisões e correções.

## Quadro e referências

- [Gestão de Projetos](https://trello.com/b/ef0pgmBq/gest%C3%A3o-de-projetos).
- [Documentação e Requisitos](https://trello.com/c/GW9NBziI): índice do acompanhamento e das oito etapas.
- [Etapa 1 — fontes, decisões e pendências](https://trello.com/c/JSWWzphR).
- [Etapa 2 — revisão do PRD e da skill](https://trello.com/c/H44CSxOh).
- [Etapa 3 — arquitetura e ADRs](https://trello.com/c/WbAWIfPP).
- [Etapa 4 — fundação técnica](https://trello.com/c/kn7QsDsL).
- [Etapa 5 — autenticação e sessão](https://trello.com/c/kF7sqMXq).
- [Etapa 6 — acesso, supervisão e rastreabilidade](https://trello.com/c/9Yigryhy).
- [Etapa 7 — revisão integrada das skills](https://trello.com/c/9Rq9Timr).
- [Etapa 8 — orientações e revisão final](https://trello.com/c/UcDLoJk1).
- [Commit e push da fundação documental](https://trello.com/c/kAHJeqGs).
- [Roteiro de implementação aprovado](https://trello.com/c/Ok3dpbjJ).
- [I00 — decisões da fundação aceitas](https://trello.com/c/ChWnlfZ8).
- [I01 — fundação Django verificada](https://trello.com/c/hR9CIEZn).
- [I02 — autenticação e sessão](https://trello.com/c/DpZG5hth).
- [I03 — cadastros, perfis e vínculos](https://trello.com/c/di9RwaAR).
- [I04 — checklist e versões](https://trello.com/c/hRV4arE6).
- [I05 — atribuição, início e supervisão](https://trello.com/c/OfaYG9v0).
- [I06 — checklist em campo, evidências e rede](https://trello.com/c/bvM4tCUH).
- [I07 — documentos do estabelecimento](https://trello.com/c/tgD8DFk1).
- [I08 — cancelamento autorizado e auditoria](https://trello.com/c/7sUzslD1).
- [I09 — pontuação, classificação e conclusão](https://trello.com/c/BENAuj0o).
- [I10 — termo em PDF e liberação ao estabelecimento](https://trello.com/c/hRPoPeN7).
- [I11 — correção autorizada, recálculo e retificação](https://trello.com/c/agcLQc1S).
- [I12 — consultas e indicadores](https://trello.com/c/SAjKk3dG).
- [Curadoria de skills e agentes](https://trello.com/c/1P8kWrmm).

O projeto local fica em `Documents/segurancaAlimentar`. Os cartões registram o acompanhamento; as fontes, o PRD, as decisões e as pendências permanecem nos documentos correspondentes. Citar um arquivo local no cartão não significa que ele foi anexado ao Trello.

## Como manter o acompanhamento

1. Consultar o cartão existente antes de criar outro. Reaproveitar o cartão da atividade e preservar seu histórico.
2. Ao iniciar trabalho autorizado, registrar o escopo e a situação. A existência de um cartão planejado não autoriza começar a atividade.
3. Atualizar o cartão nos avanços relevantes e no encerramento: o que foi realizado, arquivos ou entregas, verificações feitas, decisões, pendências, bloqueios e próximo passo.
4. Ajustar a situação de acordo com o resultado real. Distinguir redação concluída de documento aprovado e implementação de teste executado.
5. Conferir a gravação no Trello e manter o [estado](state.md) coerente com a entrega. Se a atualização falhar, registrar o que falta sincronizar e comunicar a pendência ao usuário.

Usar as listas existentes: referências em Recursos para Projetos; trabalho futuro em A fazer; validação ou revisão aguardada em Pendente; impedimento real em Bloqueio; tarefa efetivamente terminada em Concluído. Para requisitos, manter as listas da família correspondente e só registrar conclusão de implementação quando houver evidência desse trabalho.

Essa rotina acompanha todas as etapas. Continua válida a execução de uma etapa por vez e o avanço somente quando solicitado pelo usuário.

## Versionamento solicitado

O usuário solicitou commit e push da fundação documental em 10/11/2026. O [cartão da publicação](https://trello.com/c/kAHJeqGs) registra andamento, destino, verificações e confirmação do resultado/hash. Versionar os documentos não aprova os contratos Propostos ou inicia implementação.

## Planejamento de implementação — 15/11/2026

O usuário aprovou o [roteiro I00–I14](plano-implementacao.md) em 15/11/2026 e autorizou a I00. A [entrega documental](decisoes-fundacao-i00.md) detalha as propostas de versão, preparação e identidade da fundação. Depois da autorização para seguir, a [I01](entrega-i01.md) aplicou as escolhas aceitas e foi verificada em PostgreSQL local. Após nova autorização, a [I02](entrega-i02.md) entregou autenticação com verificação em PostgreSQL e Chromium. Após autorização, a [I03](entrega-i03.md) entregou a manutenção local de contas e estabelecimentos, o vínculo por unidade e a concessão técnica de Administrador. O cartão está em Concluído. O canal de entrega de credenciais reais segue em P014. A [I04](entrega-i04.md) entregou rascunhos e versões imutáveis de demonstração. As regras de checklist oficial seguem em P009/P010. A [I05](entrega-i05.md) entregou atribuição, início, versão vinculada, equipes e supervisão por ação. A autoridade de aprovação permanece em P005. A [I06](entrega-i06.md) entregou respostas, fotos de demonstração e retentativa online verificada. A [I07](entrega-i07.md) entregou documentos de demonstração da unidade, com consulta privada e reenvio verificado. A [I08](entrega-i08.md) verificou cancelamento com aprovação, bloqueio de novos registros durante a análise e auditoria por inspeção. A [I09](entrega-i09.md) verificou a pontuação de demonstração com regras originais, a conclusão confirmada e o resultado interno. A [I10](entrega-i10.md) verificou emissão, liberação separada e download privado do termo. A [I11](entrega-i11.md) verificou correção em revisão, recálculo original e retificador com liberação própria. A [I12](entrega-i12.md) verificou filtros, paginação, escopo e painel de demonstração.

## I13 e I14 — 16/11/2026

O usuário definiu execução local para a faculdade. O [cartão da I13](https://trello.com/c/y1hVzQze) acompanha o [ensaio local concluído](entrega-i13.md). O [cartão da I14](https://trello.com/c/KL83kx24) registra as escolhas, a execução e a [validação de adiamento e reanálise](entrega-i14.md).

## Interface baseada no RF-08 — 16/11/2026

O [cartão da revisão](https://trello.com/c/pNg9DDKy) registra a aplicação do protótipo ao fluxo do fiscal e da mesma identidade visual à gestão e ao portal. A [entrega](entrega-interface-rf08.md) documenta os comportamentos e a validação local.

A [adaptação desktop](https://trello.com/c/I9hMFnXg) registra a navegação por perfil, a lista em colunas e a validação dos painéis de trabalho com a interface móvel preservada.

## Senhas na gestão web — 16/11/2026

O Administrador pode definir e redefinir senhas de contas gerenciáveis pela web conforme DC039. Foram verificados o fluxo em Chromium e os 128 testes da suíte local. [Cartão](https://trello.com/c/gWdTEHws) · [Entrega](entrega-i03.md#atualização-da-gestão-de-senhas)

## Restauração do acesso — 17/11/2026

O visual anterior do acesso foi recuperado a pedido do usuário e conferido em sete larguras no Chromium, com teclado e verificação automatizada de acessibilidade. [Cartão](https://trello.com/c/RNon82ya/103-restaurar-visual-anterior-da-tela-de-acesso) · [Entrega](entrega-interface-rf08.md#restauração-visual-do-acesso--17112026)

## Revisão global do frontend — 17/11/2026

Revisão de identidade, layout responsivo, acessibilidade, metadados e estados de envio, com a linguagem visual em [DESIGN.md](../DESIGN.md). Os 128 testes passaram e o Chromium percorreu sete larguras de tela. [Cartão](https://trello.com/c/RUDd8LLh) · [Entrega](entrega-interface-rf08.md#revisão-visual-e-de-acessibilidade--17112026)

## Situação em 10/11/2026

Etapa 1 registrada como concluída. Etapa 2 com redação e conferência terminadas, em Pendente para revisão; PRD Proposto. Etapa 3 com elaboração e conferência documentais concluídas, em Pendente para revisão. Etapa 4 com elaboração e conferência documentais concluídas, em Pendente para revisão. Etapa 5 com elaboração e conferência documentais concluídas, em Pendente para revisão; spec e novo ADR Propostos. Etapa 6 com elaboração e conferência documentais concluídas, em Pendente para revisão; spec e matriz Propostas. Etapa 7 com revisão integrada das três skills concluída, em Pendente para revisão do usuário; a curadoria anterior foi preservada como histórico. Etapa 8 com orientações da raiz e revisão final elaboradas/conferidas, em Pendente para revisão; nenhuma implementação iniciada.

O índice, os resumos das decisões e políticas, a tarefa de arquitetura e a tarefa de validação foram atualizados. RF002, RF016, RF017, RF018, RF022 e RNF09 receberam o resumo vigente do PRD, preservando o texto anterior como histórico não vigente. Nenhuma função foi marcada como implementada por causa dessa atualização documental.

Na Etapa 3, o cartão existente de arquitetura foi atualizado durante a elaboração e a entrega. O índice Documentação e Requisitos foi ajustado para a situação atual e os arquivos entregues: arquitetura, sete ADRs e skill de ADR. A recomendação de monólito modular permanece não aprovada; nenhuma função foi marcada como implementada.

Na Etapa 4, o quadro recebeu o cartão da fundação técnica e atualizações durante a elaboração e na entrega. Spec e skill foram salvas; a spec está Proposta, com decisões bloqueantes identificadas e cenários futuros desmarcados. O índice foi atualizado, sem marcar RF/RNF/RS como implementados.

A curadoria adicional recebeu cartão próprio e atualizações durante o trabalho e na entrega: oito skills novas, seis agentes, três skills preservadas e limpeza das duas coleções awesome após conferência. Não há execução dos agentes ou implementação do sistema inferida a partir dessa organização.

Na revisão adicional do PRD, o cartão existente da Etapa 2 foi reutilizado. O detalhamento dos 58 requisitos foi ampliado com comparação à fonte F003: 183 entradas de dados dos RF, regras, formatos, fluxos e critérios; RNF e RS com parâmetros, controles e verificações. A skill de PRD foi ajustada. O cartão e o índice registram redação concluída para revisão, sem considerar aprovação do PRD ou implementação.

Na Etapa 5, o cartão de autenticação foi atualizado durante a elaboração e a entrega. A Spec 0002 detalha dados, forms/views, rotas, mensagens, sessão, segurança, falhas e 32 cenários futuros. O ADR 0008 recomenda sessões no servidor com PostgreSQL, ainda sem aprovação. O índice e o cartão RF001 foram atualizados, preservando o texto antigo como histórico não vigente. As pendências continuam abertas; não foram executados testes da aplicação nem iniciada a Etapa 6.

Na Etapa 6, o quadro foi atualizado durante a elaboração e na entrega da Spec 0003, da matriz das 58 entradas e da tentativa de mapa documental Graphify. A extração não retornou fragmentos completos; os agentes foram encerrados e o mapa permanece pendente, conforme o [registro](registro-graphify.md). O índice e RF002 foram ajustados ao contrato atual, preservando o histórico. AC01–AC36 e VR01–VR58 são cenários futuros; não houve teste da aplicação, implementação ou avanço de etapa.

Na Etapa 7, o cartão próprio e o índice receberam o andamento e a entrega da revisão de Python, Django e segurança com as três specs. Formato/links/consumidores e integridade foram conferidos; nove situações foram analisadas no papel, sem teste de aplicação ou avaliação independente de agentes. Specs, PRD, matriz e pendências preservados; Graphify continua pendente. A Etapa 8 não foi iniciada.

Na Etapa 8, AGENTS, CLAUDE, README da raiz e revisão final receberam cartão próprio e atualização do índice. Pontos de retomada foram corrigidos sem alterar o conteúdo dos requisitos, contratos, cenários ou decisões abertas. A revisão documental não executou a aplicação, os perfis ou descoberta automática; nenhuma fase posterior foi iniciada.

Outros cartões técnicos antigos ainda contêm propostas de tipos, prioridades ou políticas anteriores. Sua presença e eventuais marcas antigas de conclusão não aprovam as pendências atuais. Ao trabalhar nesses temas, conferir as [decisões](decisoes-confirmadas.md), as [pendências](pendencias.md) e o [PRD](prd/0001-sistema-avaliacao-seguranca-alimentar.md), atualizando o cartão afetado.
