# Revisão integrada das skills técnicas — Etapa 7

- **Data:** 10/11/2026.
- **Situação:** revisão documental concluída, para revisão do usuário.
- **Escopo:** Python, Django e segurança em conjunto com as três specs existentes. Nenhuma implementação autorizada por esta entrega.

## Referências e resultado

Foram comparadas as instruções locais com a [Spec 0001 de fundação](specs/0001-fundacao-tecnica.md), a [Spec 0002 de autenticação](specs/0002-autenticacao.md), a [Spec 0003 de acesso](specs/0003-acesso-vinculos-supervisao.md), a [arquitetura](arquitetura.md), as [decisões confirmadas](decisoes-confirmadas.md) e as [pendências](pendencias.md). O [PRD](prd/0001-sistema-avaliacao-seguranca-alimentar.md) e a [matriz](matriz-rastreabilidade.md) mantêm os requisitos e a validação futura; não são substituídos pelas skills.

As três skills já preservavam a base do projeto, mas estavam resumidas em relação às specs recentes. As lacunas abaixo foram tratadas como orientação insuficiente, não como defeito comprovado em uma aplicação: ainda não há implementação desses contratos.

| Skill revisada | Lacuna encontrada | Ajuste realizado |
|---|---|---|
| [Python](../.agents/skills/python-boas-praticas/SKILL.md) | Referência genérica à spec e à arquitetura, sem apontar os três recortes ou distinguir dados de entrada/derivados e chaves de referência | Roteamento seletivo por tarefa; tipos sem schema inferido; ator confiável; tratamento de texto/segredo por campo; falhas sem sucesso fictício |
| [Django](../.agents/skills/django-boas-praticas/SKILL.md) | Referência direta apenas à fundação; exceções nativas e detalhes de acesso ainda implícitos | Links para S1/S2/S3; herança direta de View; exceções de ORM e AuthenticationForm; sessão na camada HTTP; consulta filtrada/revogação na efetivação |
| [Segurança](../.agents/skills/seguranca-aplicacao/SKILL.md) | Faltava distinguir backend de sessão recomendado, transporte CSRF necessário, resposta perdida de login e acesso por versão/contagem | Base confirmada versus proposta; segredo fora de mensagens/logs sem remover transporte nativo; controles negativos, vigência, revogação e propostas P014/P020 explícitas |

As instruções foram mantidas em um único SKILL.md por skill, sem scripts, novos módulos, cópias integrais das specs ou diretórios vazios. Nomes e licenças foram preservados. A descrição continua delimitada à especialidade; não ativa revisão de segurança completa ou análise geral para qualquer pergunta do projeto.

## Correspondência com os contratos

| Contrato de referência | Orientação preservada ou explicitada | Limite mantido |
|---|---|---|
| S1: versões/configuração/PostgreSQL | Conferir P001, não criar fallback SQLite nem aceitar indisponibilidade como sucesso; preservar ambiente existente | Versões, driver, ferramenta e valores não escolhidos |
| S1: identidade inicial | AbstractUser confirmado, referências ao modelo configurado e primeira migração condicionada a P002 | `contas.Usuario`, chave, campos/perfis e vínculos físicos continuam candidatos |
| Arquitetura/S2: View, form e services | Views próprias diretamente de View; ORM explícito no service sem HTTP; nativos do framework admitidos | AuthenticationForm com request e login/logout na view não viram autorização de negócio em forms/views |
| S2: credenciais e sessão | Mecanismos nativos; texto de senha preservado conforme campo; encerramento verificado no servidor; falha no middleware considerada | Backend do ADR 0008, prazo, tentativas, recuperação e cookies não aprovados por defaults |
| S2: comunicação ambígua | Não tratar timeout como senha inválida ou resultado confirmado; consultar proposta específica | Reconciliação sem reenvio silencioso de senha continua em P014/P020; não foi aprovada nesta revisão |
| S3: perfil/vínculo/designação | Ator confiável, consultas filtradas e validação atual no caso de uso, inclusive após revogação na mesma sessão | Ação/inspeção, quantidade/vigência, autoridade e autoaprovação continuam em P002–P006 |
| S3: estabelecimento/arquivos | Próprios envios e final liberado, incluindo versão, contagem e URL direta | Janelas de envio, liberação e armazenamento permanecem em P011/P012/P016 |
| S3: concorrência/Admin | Nenhum atalho por flags técnicas, cache, transação isolada ou edição direta; revalidar antes do efeito | Mecanismo físico, restrições e deduplicação dependem da política/spec funcional |
| PRD/matriz: evidência | Diferenciar conferência documental, cenário futuro e teste executado | VF/AU/AC/VR não foram executados como testes de aplicação |

## Revisão guiada de situações

Esta foi uma conferência de decisões no papel, realizada pelo próprio agente revisor. Não é avaliação independente de comportamento, execução dos perfis TOML ou teste de aplicação. Os casos serviram para comparar as instruções revisadas com o contrato de origem.

| Situação examinada | Encaminhamento conferido nas instruções | Referência |
|---|---|---|
| Exemplo externo usa UUID e uma versão fixa para iniciar o projeto | Não adotar tipos/versões por exemplo; resolver a parte aplicável de P001/P002 antes da migração | S1, Python/Django |
| Login nativo parece violar a regra de não receber request em services | Manter a exceção de AuthenticationForm e sessão na view; não criar um AuthService vazio | S2, Django |
| Trocar a view própria por LoginView/FormView | Preservar herança direta de View, sem reescrever componentes internos | Arquitetura/S2, Django |
| Remover token do formulário para impedir sua aparição em qualquer HTML | Preservar transporte CSRF nativo; restringir mensagens, URL e logs | S2, segurança |
| Chamar login retorna, mas o middleware falha ao gravar sessão | Não confirmar só pelo retorno; verificar resposta e reconhecimento no acesso seguinte | S2, Django/Python |
| Fiscal com designação na ação A envia POST para decidir na ação B | Verificar ator/contexto no service, sem autoridade global ou confiança no formulário | S3, Django/segurança |
| Designação ou vínculo revogado enquanto a conta continua conectada | Revalidar acesso atual e efetivação, sem concessão congelada no login | S3, Django/segurança |
| Resposta de login perdida sugere copiar a retentativa automática da inspeção | Tratar a regra específica como proposta ainda aberta, sem armazenar senha ou aprovar comportamento por inferência | S2/P014/P020, segurança |
| Um POST repetido ou uma edição pelo Admin aparenta respeitar a tela | Revalidar o mesmo caso de uso; botão/redirect/atomic não comprovam autorização, deduplicação ou histórico | S3, Django/segurança |

Não foi necessário mudar as specs para acomodar as skills. Na ocorrência de conflito futuro, conferir a decisão vigente e corrigir o artefato adequado, sem deixar a skill aprovar uma política pendente ou alterar o produto silenciosamente.

## Verificações documentais realizadas

- Validação das três skills com o validador oficial disponível: frontmatter YAML, nome, descrição, propriedades e ausência de marcadores de scaffold.
- Conferência dos links locais e dos consumidores em `.codex/agents`: os nomes/caminhos existentes continuam válidos. Perfis não editados ou executados; carregamento automático não foi testado.
- Comparação do inventário de arquivos antes/depois, limitada às três skills e aos registros desta etapa. PRD, três specs, matriz, decisões, pendências, fontes, avisos de terceiros, código, Git e arquivos de ambiente preservados.
- Contagem preservada dos cenários existentes: 12 VF, 32 AU, 36 AC e 58 VR; são planos futuros, não resultados aprovados.

O interpretador usado para validar Markdown/YAML é uma ferramenta já instalada, não a seleção do Python da aplicação. Não houve instalação de pacotes, criação de ambiente, execução de banco/migrações, teste de aplicação ou configuração global.

## Graphify, economia e continuidade

O mapa continua pendente conforme o [registro da Etapa 6](registro-graphify.md). Esta revisão pontual utilizou leitura dirigida das skills e dos contratos; não reiniciou a extração semântica nem tratou um grafo inexistente como concluído. A preferência Caveman continua voltada à concisão da conversa, preservando o conteúdo solicitado nos documentos.

O [catálogo](../.agents/README.md), o [estado](state.md), as [etapas](etapas.md) e o [Trello](acompanhamento-trello.md) apontam para esta entrega. A Etapa 8 foi posteriormente solicitada; [AGENTS](../AGENTS.md), [CLAUDE](../CLAUDE.md), [README da raiz](../README.md) e [revisão final](revisao-final-fundacao.md) consolidam as orientações. A próxima atividade depende da solicitação atual registrada no estado. As specs/ADRs e políticas abertas não foram aprovados pela conclusão desta revisão.
