# Pendências e propostas

Atualizado em 15/11/2026, com a fundação I01 e as entregas locais I02 a I04.

As pessoas responsáveis nominalmente e os prazos ainda não foram definidos. A coluna de encaminhamento identifica o papel que precisa participar, sem atribuir uma decisão a alguém que não a assumiu. P001 foi resolvida para a fundação local. P002 foi resolvida em parte e as demais pendências seguem abertas.

Elas não impedem preparar o PRD e a arquitetura com o que já está confirmado. Cada uma precisa ser resolvida antes da spec ou implementação indicada, ou continuar explicitamente bloqueada. Pendência não autoriza preencher uma regra por inferência. As [decisões confirmadas](decisoes-confirmadas.md) não serão reabertas por estarem descritas como propostas em fontes antigas.

## P001 Versões e preparação do ambiente

Resolvida para a I01 em DC023. A entrega fixou as dependências e verificou os ambientes locais. A estratégia operacional segue em P015. [Decisões confirmadas](decisoes-confirmadas.md#dc023-versões-e-preparação-local-da-fundação) · [Entrega I01](entrega-i01.md)

Encaminhamento: Decisão técnica da equipe.

Origem: F007; contexto técnico. F008; pendências.

## P002 Identidade e vínculos

Definir campos adicionais, estratégia de identificador, representação dos perfis e vínculos de usuários com estabelecimentos. Não presumir UUID físico ou múltiplos perfis porque aparecem como exemplos. DC024 resolveu a primeira migração com `contas.Usuario`, chave interna `BigAutoField` e os campos herdados de `AbstractUser`. A [Spec 0001](specs/0001-fundacao-tecnica.md) registra essa entrega. A I03 adotou um perfil por conta, vínculo aberto de uma unidade por conta de Estabelecimento, gestão de vínculos por Administrador e concessão administrativa pela equipe técnica com autoria registrada. Tipo, máscara, unicidade de documento, regras de contato e procedimento operacional de revogação de Administrador seguem em revisão. [Entrega I03](entrega-i03.md) · [Spec 0004](specs/0004-cadastro-estabelecimentos.md)

Encaminhamento: Equipe, com validação do responsável pelo produto.

Quando precisa estar resolvida: as regras restantes de cadastro, perfis e vínculos antes dos recortes que dependem delas.

Origem: F003; RF001, RF002 e RF003.

## P003 Ação e inspeção

Determinar se uma ação equivale a uma inspeção ou pode reunir várias. A Spec 0003 usa contexto como referência lógica, sem criar entidade, FK ou relação física definitiva. Resolver antes de materializar os vínculos e as rotas de supervisão.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: 6, antes do contrato de supervisão e do modelo de relacionamento.

Origem: F003; RF002. F005; seção 5.

## P004 Designação do supervisor

Definir quem designa, substitui e encerra, quantos supervisores existem por ação e sua vigência. Na Spec 0003 permanecem candidatos os critérios de elegibilidade, sobreposição, período aberto, agendamento/retroatividade e intervalo com fim exclusivo. Não foi criada unicidade de supervisor por ação ou autoridade administrativa automática.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: 6, antes de implementar supervisão.

Origem: F003; RF002 e RS002.

## P005 Autoridade aprovadora

Definir quem aprova alteração/cancelamento, substituição na ausência e tratamento da solicitação do próprio supervisor. Não conceder esse poder ao administrador por inferência. A matriz de papéis da Spec 0003 mantém essas células pendentes; propõe não conceder a operação enquanto a política estiver indefinida, sem aprovar uma regra definitiva de autoaprovação.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: 6 e specs de autorização, antes da implementação.

Origem: F003; RF018, RF022 e RS002.

## P006 Alterações durante o andamento

Delimitar mudanças que exigem autorização além do preenchimento normal; decidir se pedido pendente bloqueia novas edições.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: Specs funcionais posteriores.

Origem: F003; RF018 e RF022.

## P007 Adiamento

Validar condições, justificativa, eventual aprovação, data, estado da inspeção e retomada. Aprovação semelhante ao cancelamento ainda é proposta.

Encaminhamento: Responsável pelo produto e pelo processo.

Quando precisa estar resolvida: Antes de detalhar e implementar o fluxo de adiamento.

Origem: F003; RF027.

## P008 Reanálise documental

Decidir quando documento novo exige reanálise, quem analisa/aprova, prazos e necessidade de nova visita.

Encaminhamento: Responsável pelo produto e pelo processo.

Quando precisa estar resolvida: Antes de detalhar e implementar reanálise.

Origem: F003; RF028.

## P009 Checklist e governança

Escolher referência sanitária, itens, obrigatoriedade, opções de resposta e responsáveis por publicar versões oficiais. No ambiente local, a I04 permite ao Administrador editar rascunhos e publicar versões de demonstração com dados fictícios. [Spec 0005](specs/0005-checklist-e-versoes.md) · [Entrega da I04](entrega-i04.md)

Encaminhamento: Equipe e profissionais que validam a avaliação.

Quando precisa estar resolvida: Antes de aceitar conteúdo sanitário oficial ou habilitar sua publicação e uso em inspeções reais.

Origem: F001; tópico 1. F003; RF004 e RF007.

## P010 Pontuação

Definir fórmula, pesos, N/A, arredondamento, faixas de classificação e comparabilidade entre versões.

Encaminhamento: Responsável pela avaliação, com apoio da equipe.

Quando precisa estar resolvida: Antes de implementar e validar cálculo e indicadores.

Origem: F003; RF013, RF020 e RF026.

## P011 Documentos do estabelecimento

Definir categorias, obrigatoriedade, prazos, formatos, limites, complementação, substituição e envio após conclusão.

Encaminhamento: Responsável pelo processo, com apoio técnico.

Quando precisa estar resolvida: Antes de detalhar e implementar os envios.

Origem: F003; RF017 e RS008.

## P012 Resultado final e termos

Definir momento de liberação ao estabelecimento, modelos, numeração, vigência, nova versão versus termo retificador e tratamento de inspeção concluída inválida.

Encaminhamento: Responsável pelo processo e pela validação documental.

Quando precisa estar resolvida: Antes de implementar publicação, termos e anulação.

Origem: F003; RF015, RF016, RF021 e RF022.

## P013 Assinatura e ciência

Escolher forma de identificação, assinatura, ciência e tratamento aplicável ao documento oficial.

Encaminhamento: Responsável pelo processo e pela validação documental.

Quando precisa estar resolvida: Antes de implementar RF025.

Origem: F001; tópico 2. F003; RF025.

## P014 Políticas complementares de acesso

Definir recuperação de conta, senha, MFA/SSO, limitação de tentativas, expiração, sessões simultâneas e revogação. A base Django de usuário e senha já está confirmada. O fluxo básico da [Spec 0002](specs/0002-autenticacao.md) foi implementado e verificado localmente na [I02](entrega-i02.md).

O backend nativo de sessão em PostgreSQL foi adotado na I02 conforme o [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md). Falta escolher duração de produto, renovação por atividade, efeito do fechamento do navegador, concorrência, efeitos de mudança de senha e revogação global. Também permanecem em aberto a criação e a entrega de credenciais, os efeitos da reativação sobre sessões antigas, as medidas contra tentativas abusivas e a validação dos cookies na implantação. A I03 cria contas comuns inativas, com configuração interativa de credencial em etapa separada no ambiente de demonstração. O canal de entrega real segue aberto. O tratamento de resposta perdida e de dados abertos ao sair, expirar ou trocar conta depende de P020.

Encaminhamento: Responsável pelo produto com a equipe técnica.

Quando precisa estar resolvida: 5 a 7, antes da implementação dos controles e da operação real.

Origem: F003; RS003 e RS004. F008; autenticação.

## P015 Hospedagem e operação

Escolher provedor, domínio, ambientes, acompanhamento de falhas e responsáveis operacionais. Para autenticação, validar TLS, proxy, origens, cookies, preparação do backend PostgreSQL em produção e manutenção dos registros expirados. A configuração da I02 foi verificada no ambiente local.

Encaminhamento: Responsável pelo projeto e equipe técnica.

Quando precisa estar resolvida: Antes da preparação da operação real.

Origem: F005; seções 8 e 10.

## P016 Arquivos e PDF

Definir armazenamento, entrega privada, coordenação com banco, biblioteca de PDF, formatos, limites e validação dos arquivos.

Encaminhamento: Equipe técnica, após requisitos operacionais.

Quando precisa estar resolvida: Antes das specs e implementação desses recursos.

Origem: F003; RF009, RF015, RS008 e RS010.

## P017 Proteção e retenção

Definir classificação de dados, retenção, acesso à auditoria, proteção em repouso e eliminação conforme a política aprovada. A I03 grava autoria, data e mudanças de cadastro e vínculos na transação do ato. A política operacional e a consulta de histórico seguem em aberto.

Encaminhamento: Responsável pelo processo e equipe técnica.

Quando precisa estar resolvida: Antes do desenho final e da operação real.

Origem: F003; RS006, RS007 e RS012.

## P018 Metas e recuperação

Levantar usuários, carga, volume de arquivos, disponibilidade, tempos, backup, perda máxima de dados e tempo de recuperação. Não inventar metas numéricas.

Encaminhamento: Responsável pelo produto e equipe técnica.

Quando precisa estar resolvida: Antes dos testes de desempenho e da operação real.

Origem: F003; RNF02, RNF03, RNF06 e RNF11.

## P019 Compatibilidade e acessibilidade

Homologar navegadores, versões, dispositivos e critérios de acessibilidade; definir captura de foto e alternativa por arquivo.

Encaminhamento: Usuários representativos com a equipe técnica.

Quando precisa estar resolvida: Antes de aceitar a interface e os fluxos em campo.

Origem: F003; RNF01, RNF07 e RNF08.

## P020 Pendências na tela e reenvio

Decidir se existirá armazenamento persistente no navegador; intervalo de tentativa, recuperação e limpeza, especialmente em aparelho compartilhado. Preservação da página aberta já está confirmada. Detalhar identificação da operação, conteúdo diferente na repetição, concorrência, prazo de reconhecimento e recuperação do resultado sem duplicidade; esses pontos foram explicitados na arquitetura da Etapa 3, sem escolher um mecanismo.

Na [Spec 0002](specs/0002-autenticacao.md), validar com P014 a proposta específica para credenciais: depois de resposta perdida, conferir a sessão por leitura e permitir nova tentativa explícita quando necessário, sem reenvio silencioso de senha. Isso ainda não aprova uma exceção à retentativa geral. Definir limpeza/proteção de outras abas e de dados pendentes ao sair, expirar ou trocar conta; não presumir salvamento nem descarte desses dados.

Encaminhamento: Equipe técnica com validação do produto.

Quando precisa estar resolvida: Antes de implementar recuperação de envio.

Origem: F003; RF011, RNF14 e RS014.

## P021 Revisão dos protótipos

Alinhar cancelamento à solicitação/autorização e revisar limites, textos, imagens, dados e obrigatoriedade ilustrativos. Não alterar o protótipo nesta etapa.

Encaminhamento: Equipe com validação de usuários.

Quando precisa estar resolvida: Antes de usar as telas como especificação de comportamento.

Origem: F009; tela 10 e exemplos. F003; RF022.

## P022 Priorização e estimativas

Validar prioridades do catálogo, escopo da primeira versão, responsáveis, esforço, prazo e orçamento. Não há calendário de implementação aprovado.

Encaminhamento: Responsável pelo projeto com a equipe.

Quando precisa estar resolvida: 2 para escopo proposto; antes de comprometer entregas de software.

Origem: F003; prioridades A validar. F005; seções 11 e 12.

## Propostas preservadas como propostas

- Representar uma ação como agrupamento de inspeções depende de P003.
- Exigir autorização para adiamento semelhante ao cancelamento depende de P007.
- Abrir uma reanálise a partir de documento novo depende de P008; anexo não muda resultado automaticamente.
- Criar um app para cada área da visão conceitual não foi decidido. As áreas lógicas foram detalhadas como proposta na [arquitetura](arquitetura.md); o [ADR 0007](adr/0007-monolito-modular.md) foi aceito para a fundação. A estrutura física será detalhada nas specs pertinentes.
- A retomada assistida da [Spec 0002](specs/0002-autenticacao.md) permanece proposta. Prazo de expiração, tentativas, recuperação e revogação global ainda dependem de decisão.
- Metas de desempenho, tamanhos, máscaras, fórmulas, identificadores físicos e prazos ainda não aprovados não devem ser tratados como definitivos.

A [matriz de rastreabilidade](matriz-rastreabilidade.md) liga as 58 entradas às fontes, relações e validação futura; não encerra P001 a P022. Os dados/rotas/services da Spec 0003 são Propostos e não implementam acesso.

O uso de MVT com services, templates, views derivadas de View e a base de login por usuário/senha deixaram de ser propostas após F008. O registro dessas escolhas está no documento de decisões confirmadas.

## Como encerrar uma pendência

Registrar a resposta, sua origem e data e atualizar as decisões confirmadas e os documentos afetados na etapa correspondente. Preservar o histórico da pergunta sem marcar como decidida apenas porque uma sugestão técnica foi escrita.
