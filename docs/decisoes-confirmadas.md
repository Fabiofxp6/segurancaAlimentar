# Decisões confirmadas

Atualizado em 15/11/2026, com o aceite das escolhas aplicadas na I01.

Este registro consolida decisões já expressas; não constitui PRD, ADR ou implementação. Os documentos futuros serão elaborados nas etapas acordadas. As políticas ainda abertas estão em [pendências](pendencias.md).

As fontes F001 a F009 estão descritas no [índice de referências](referencias/README.md). F008 registra as confirmações mais recentes.

## DC001 Organização do trabalho

A documentação será criada no projeto novo. Trabalhar em oito etapas, uma por vez, e aguardar a solicitação do usuário para avançar. A etapa atual e o ponto de retomada ficam registrados no [estado](state.md). A solicitação de uma etapa não autoriza executar as seguintes.

Origem: F008; seção Organização do trabalho. Etapas relacionadas: Todas.

## DC002 Separação dos artefatos

PRD descreve produto; specs detalham construção; arquitetura define fronteiras; skills orientam tarefas; AGENTS guia a consulta; state guarda a retomada; ADRs registram razões das decisões.

Origem: F007; Organização documental. F008; Escopo aprovado. Etapas relacionadas: 2 a 8.

## DC003 Tecnologias principais

Python com Django e PostgreSQL. Java foi substituído; SQLite pertence ao blog de referência. As versões ainda serão definidas.

Origem: F003; descrição geral. F005; seção 8. F008. Etapas relacionadas: 3 e 4.

## DC004 Forma de acesso e hospedagem

Sistema web em navegador para tablets e celulares, com hospedagem remota ou em nuvem. Provedor e ambientes homologados ainda não escolhidos.

Origem: F003; descrição geral. F005; seção 8. Etapas relacionadas: 3 e 4.

## DC005 Arquitetura de referência adotada

MVT com páginas renderizadas por templates Django; views derivadas diretamente de View, admitindo mixins de acesso; regras e consultas explícitas da aplicação em services; services sem request ou resposta HTTP.

Origem: F008; Padrão arquitetural. Etapas relacionadas: 3, 4 e 7.

## DC006 Limites entre camadas

Forms validam entrada, models descrevem persistência e restrições, templates apresentam dados. Login/logout dependentes de sessão ficam na view. O Admin deve respeitar as regras de negócio. As exceções do framework serão explicitadas na arquitetura.

Origem: F008; Padrão arquitetural e plano aprovado. Etapas relacionadas: 3 a 7.

## DC007 Base de autenticação

Usuário customizado baseado em AbstractUser, login por nome de usuário e senha e sessão Django. Não há escolha aprovada de MFA, SSO ou recuperação de conta.

Origem: F008; Autenticação e plano aprovado. Etapas relacionadas: 4 e 5.

## DC008 Perfis-base

Fiscalização, Administrador e Estabelecimento. Cliente é o estabelecimento avaliado. Não confundir perfil administrativo de negócio com is_staff ou superusuário técnico.

Origem: F003; convenções e RF002. F008. Etapas relacionadas: 2 e 6.

## DC009 Supervisão por ação

Supervisor continua sendo fiscal e é designado para uma ação específica. Pode mudar entre ações; não é quarto perfil nem cargo permanente. Designação para uma ação não concede poder sobre outra.

Origem: F003; RF002 e RS002. Etapas relacionadas: 2 e 6.

## DC010 Início da inspeção

Administrador pode atribuir inspeção; fiscal também pode iniciá-la diretamente. Participar ou iniciar não concede supervisão automática.

Origem: F003; RF005 e RF006. Etapas relacionadas: 2; specs funcionais posteriores.

## DC011 Versão inicial do checklist

Preservar a versão do checklist e das regras desde o início da inspeção. Uma publicação posterior não altera a avaliação já iniciada.

Origem: F003; RF004 e RF007. Etapas relacionadas: 2; specs funcionais posteriores.

## DC012 Cancelamento em andamento

Exigir solicitação, justificativa e autorização antes de efetivar o cancelamento no servidor. Preservar respostas, evidências e histórico. A regra de autoridade e o efeito do pedido pendente foram definidos em DC032.

Origem: F003; RF022. Etapas relacionadas: 2 e 6; spec funcional posterior.

## DC013 Correção posterior à conclusão

Exigir autorização, justificativa e histórico antes de aplicar a correção. Preservar valores anteriores e novos e o vínculo com a decisão. O preenchimento normal em andamento permanece previsto.

Origem: F003; RF018 e RF019. Etapas relacionadas: 2 e 6; specs funcionais posteriores.

## DC014 Score e recálculo

Cálculo automático faz parte do escopo atual. Quando uma correção afetar a avaliação, recalcular pelas regras originais e conservar resultado anterior e novo. DC033 define a regra de demonstração. A regra sanitária oficial segue em P010.

Origem: F002; RF06. F003; RF013 e RF020. Etapas relacionadas: 2; spec funcional posterior.

## DC015 Termos em PDF

PDF pode ser gerado depois do salvamento no servidor. Preservar termo emitido e relacionar nova versão ou termo retificador ao anterior quando necessário. A política documental detalhada está aberta.

Origem: F003; RF015 e RF021. Etapas relacionadas: 2; spec funcional posterior.

## DC016 Identificação e ciência

As fontes preveem identificação do fiscal e do responsável e registro de ciência no termo. Mecanismo de assinatura e validade dependem de definição.

Origem: F001; tópico 2. F002; RF05. F003; RF025. Etapas relacionadas: 2; spec funcional posterior.

## DC017 Acesso do estabelecimento

Estabelecimento envia documentação própria relacionada à inspeção e consulta seus envios e resultados finais liberados. Sem respostas em elaboração, avaliações parciais ou deliberações internas. Envio de anexo não altera a nota automaticamente.

Origem: F003; RF016 e RF017. Etapas relacionadas: 2 e 6; spec funcional posterior.

## DC018 Somente online

Não haverá inspeção completa offline. Ações oficiais dependem do servidor; isso substitui o RF09 do PDF original.

Origem: F003; RF010. F005; seção 7. Etapas relacionadas: 2 e 3; specs funcionais posteriores.

## DC019 Perda de comunicação

Bloquear temporariamente ações dependentes do servidor, preservar o preenchimento na tela aberta e tentar enviar após a reconexão. Só indicar salvo após confirmação do servidor. Retentativas não podem duplicar o efeito oficial.

Origem: F003; RF008 e RF010 a RF012; RS013. Etapas relacionadas: 2 e 3; specs funcionais posteriores.

## DC020 Histórico e segurança

Preservar eventos críticos com autoria e contexto; verificar acesso no servidor, inclusive em arquivos e decisões. O catálogo revisado inclui requisitos de segurança, sem considerar aprovadas as políticas ainda abertas.

Origem: F003; RF023, RS001 a RS016. Etapas relacionadas: 2, 3, 6 e 7.

## DC021 Preservação dos identificadores

Manter RF001 a RF028, RNF01 a RNF14 e RS001 a RS016 ou explicitar qualquer mapeamento futuro. Identificadores e títulos do blog não substituem o catálogo alimentar.

Origem: F003; identificação dos requisitos. F008; plano aprovado. Etapas relacionadas: 2 a 6.

## DC022 Acompanhamento de todas as atividades no Trello

Atualizar o quadro Gestão de Projetos em paralelo a todas as atividades deste projeto: análise, planejamento, documentação, decisões, desenvolvimento, testes e correções. Registrar entregas, verificações, pendências, bloqueios e próximo passo com situação real. A rotina está em [acompanhamento no Trello](acompanhamento-trello.md); não altera a execução de uma etapa por vez.

Origem: solicitação direta do usuário em 10/11/2026, após a entrega da Etapa 2. Etapas relacionadas: Todas.

## DC023 Versões e preparação local da fundação

A base aprovada para desenvolvimento e testes é Python 3.14, Django 5.2 LTS, PostgreSQL 17 e Psycopg 3.3 binário. O uv mantém dependências reproduzíveis. Django roda no host e o PostgreSQL usa instâncias Docker Compose separadas para desenvolvimento e testes. O perfil de produção depende de configuração externa. A hospedagem permanece em P015.

Origem: proposta da I00 e autorização do usuário para seguir com a I01 em 15/11/2026. [I00](decisoes-fundacao-i00.md) · [Verificação da I01](entrega-i01.md)

## DC024 Identidade da primeira migração

O modelo é `contas.Usuario`, baseado em `AbstractUser`, com chave interna `BigAutoField` e campos herdados na primeira migração. `AUTH_USER_MODEL` referencia esse modelo desde o início. O identificador técnico é inteiro, e a referência lógica `usuarioId` continua no catálogo. Perfis, campos de cadastro de negócio, vínculos e autoridades seguem para os recortes correspondentes.

Origem: proposta da I00 e autorização do usuário para seguir com a I01 em 15/11/2026. [I00](decisoes-fundacao-i00.md) · [Spec 0001](specs/0001-fundacao-tecnica.md)

## DC025 Monólito modular na fundação

Uma aplicação Django começa com configuração, identidade e templates. A organização de novas áreas será detalhada à medida que suas specs forem aprovadas.

Origem: proposta da I00 e autorização do usuário para seguir com a I01 em 15/11/2026. [ADR 0007](adr/0007-monolito-modular.md)

## DC026 Sessão no servidor na I02

O backend nativo de sessões do Django usa PostgreSQL. A saída invalida no servidor a sessão corrente. No ambiente local, a I02 usa o prazo e a renovação padrão do framework como configuração técnica. As políticas de expiração, revogação global, segurança das credenciais e operação remota seguem em P014/P015.

Origem da escolha técnica na I02 autorizada pelo usuário em 15/11/2026. [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md) · [Entrega da I02](entrega-i02.md)

## DC027 Perfis e vínculos na I03

A I03 adota um perfil-base por conta. Cada conta de Estabelecimento pode ter um vínculo aberto com uma unidade. Uma unidade pode ter várias contas. Administrador ativo mantém vínculos pelo sistema. O acesso do Estabelecimento é recalculado na sessão atual e exige conta e unidade ativas e vínculo aberto.

A concessão do perfil Administrador é restrita ao procedimento técnico registrado, para uma conta ativa, dedicada, com credencial configurada e sem perfil prévio. Contas abertas pela gestão web começam inativas e recebem credencial em passo separado. O canal de entrega de credenciais reais permanece em P014.

Origem: escolhas conservadoras adotadas no recorte local após autorização do usuário para retomar e concluir a I03 em 15/11/2026. [Entrega da I03](entrega-i03.md)

## DC028 Rascunhos e versões de checklist na I04

O Administrador mantém o checklist e publica versões para demonstração. O servidor copia o conteúdo do rascunho para uma versão com número, autor, data e finalidade identificada. As versões publicadas ficam imutáveis no PostgreSQL. A futura inspeção deve preservar a referência à versão usada.

Origem: escolhas técnicas adotadas na I04 autorizada em 15/11/2026. A governança e o conteúdo oficiais seguem em P009, e a fórmula em P010. [Spec 0005](specs/0005-checklist-e-versoes.md) · [Entrega da I04](entrega-i04.md)

## DC029 Ações e supervisão na I05

Uma ação de fiscalização pode agrupar várias inspeções. O Administrador pode designar simultaneamente fiscais ativos da equipe da ação. A designação é opcional e começa imediatamente. A identidade de Supervisor permanece vinculada à ação. DC032 define a aprovação de cancelamento. A política de correção continua em P005.

Origem: respostas do usuário em 16/11/2026 às perguntas sobre relação ação–inspeção e autoridade, cardinalidade e vigência da designação. [Spec 0006](specs/0006-inicio-equipe-e-supervisao.md) · [Entrega da I05](entrega-i05.md)

## DC030 Confirmação e evidências no recorte local da I06

A demonstração da I06 grava a resposta por item da versão original e registra as fotos no PostgreSQL. A confirmação da operação e o dado são persistidos na mesma transação. A interface conserva na memória da página um envio solicitado e usa a mesma chave ao reenviar após reconexão. A seleção local de JPEG e PNG, os limites e o armazenamento da demonstração permanecem escolhas técnicas do recorte.

Origem: DC018/DC019 e autorização para executar a I06 em 16/11/2026. As escolhas operacionais seguem nas pendências. [Spec 0007](specs/0007-campo-evidencias-e-reenvio.md) · [Entrega da I06](entrega-i06.md)

## DC031 Documentos do estabelecimento na I07

O estabelecimento envia documentos da atribuição ao fim do andamento. Todas as contas ativas vinculadas à unidade podem consultar os documentos da unidade. Para demonstração, os formatos aceitos são PDF, JPEG e PNG.

Origem: respostas do usuário em 16/11/2026 sobre janela, formatos de demonstração e consulta entre contas da mesma unidade. [Spec 0008](specs/0008-documentos-do-estabelecimento.md) · [Entrega da I07](entrega-i07.md)

## DC032 Cancelamento autorizado na I08

Outro supervisor ativo e elegível da ação decide o pedido de cancelamento, inclusive quando o solicitante for supervisor. O Administrador decide quando não houver outro supervisor elegível. Enquanto o pedido estiver pendente, novas respostas, fotos e documentos ficam bloqueados. Após registrar a aprovação, o servidor efetiva o cancelamento automaticamente.

Origem: respostas do usuário em 16/11/2026 sobre autoridade, bloqueio de registros e efetivação. [Spec 0009](specs/0009-cancelamento-e-auditoria.md) · [Entrega da I08](entrega-i08.md)

## DC033 Pontuação, classificação e conclusão na I09

Na demonstração, Conforme ou Sim soma o peso do item, Não conforme ou Não vale zero e Não se aplica sai da base. Sem itens aplicáveis, mostrar Sem pontuação. A nota arredondada a duas casas fica Satisfatória a partir de 80%, Regular a partir de 60% e Insatisfatória abaixo de 60%.

Bloquear a conclusão quando faltar resposta obrigatória ou houver envio pendente ou falho na tela que conclui. Os documentos do estabelecimento são opcionais.

Origem: respostas do usuário em 16/11/2026 sobre cálculo, faixas e bloqueios. [Spec 0010](specs/0010-pontuacao-e-conclusao.md)

## Regras antigas que deixaram de valer

| Informação anterior | Situação atual | Referência |
|---|---|---|
| Java como linguagem | Substituída por Python com Django | DC003 |
| SQLite da referência | Não é escolha para o sistema alimentar; PostgreSQL está confirmado | DC003 |
| Offline completo com sincronização no PDF original | Substituído por operação online com tratamento de interrupção | DC018 e DC019 |
| Fiscal cancela só com justificativa | Agora há solicitação e autorização antes da efetivação | DC012 |
| Supervisor global ou permanente | Função contextual atribuída ao fiscal por ação | DC009 |
| MVT, templates e View ainda eram propostas na análise de 09/11 | Confirmados pelo usuário no planejamento de 10/11 | DC005 e DC006 |
| Método de autenticação ainda inteiramente aberto na visão de 09/11 | Base de usuário/senha e sessão Django confirmada; políticas adicionais seguem abertas | DC007 |

## Temas que não são decisões confirmadas

O fluxo de adiamento, a reanálise após anexos novos e os detalhes de autorização não foram aprovados integralmente. Sua presença no catálogo ou em um protótipo não resolve as perguntas registradas em pendências. Limites e máscaras de exemplo não se tornam regras apenas por aparecerem em uma tela.
