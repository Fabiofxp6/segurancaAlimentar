# Pendências e propostas

Atualizado em: 10/11/2026. Registro iniciado na Etapa 1, com detalhamentos até a Etapa 5.

As pessoas responsáveis nominalmente e os prazos ainda não foram definidos. A coluna de encaminhamento identifica o papel que precisa participar, sem atribuir uma decisão a alguém que não a assumiu. Todas as pendências abaixo estão abertas.

Elas não impedem preparar o PRD e a arquitetura com o que já está confirmado. Cada uma precisa ser resolvida antes da spec ou implementação indicada, ou continuar explicitamente bloqueada. Pendência não autoriza preencher uma regra por inferência. As [decisões confirmadas](decisoes-confirmadas.md) não serão reabertas por estarem descritas como propostas em fontes antigas.

## P001 Versões e preparação do ambiente

Escolher versões compatíveis e suportadas de Python, Django e PostgreSQL e a preparação do ambiente. Não herdar as versões do blog. A [Spec 0001](specs/0001-fundacao-tecnica.md) propõe a separação de configuração e os contratos externos; versões, driver e ferramenta de preparação permanecem sem escolha, bloqueando a execução correspondente.

Encaminhamento: Decisão técnica da equipe.

Quando precisa estar resolvida: 4, antes de implementar a fundação.

Origem: F007; contexto técnico. F008; pendências.

## P002 Identidade e vínculos

Definir campos adicionais, estratégia de identificador, representação dos perfis e vínculos de usuários com estabelecimentos. Não presumir UUID físico ou múltiplos perfis porque aparecem como exemplos. A [Spec 0001](specs/0001-fundacao-tecnica.md) propõe o nome contas.Usuario para a identidade mínima; nome, identificador e campos iniciais devem ser validados antes da primeira migração. Perfis e vínculos continuam no recorte da Etapa 6.

Encaminhamento: Equipe, com validação do responsável pelo produto.

Quando precisa estar resolvida: 4 a 6, antes de consolidar modelos e migrações.

Origem: F003; RF001, RF002 e RF003.

## P003 Ação e inspeção

Determinar se uma ação equivale a uma inspeção ou pode reunir várias.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: 6, antes do contrato de supervisão e do modelo de relacionamento.

Origem: F003; RF002. F005; seção 5.

## P004 Designação do supervisor

Definir quem designa, substitui e encerra, quantos supervisores existem por ação e sua vigência.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: 6, antes de implementar supervisão.

Origem: F003; RF002 e RS002.

## P005 Autoridade aprovadora

Definir quem aprova alteração/cancelamento, substituição na ausência e tratamento da solicitação do próprio supervisor. Não conceder esse poder ao administrador por inferência.

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

Escolher referência sanitária, itens, obrigatoriedade, opções de resposta e responsáveis por publicar versões.

Encaminhamento: Equipe e profissionais que validam a avaliação.

Quando precisa estar resolvida: Antes de implementar checklist e aceitar seu conteúdo.

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

Definir recuperação de conta, senha, MFA/SSO, limitação de tentativas, expiração, sessões simultâneas e revogação. A base Django de usuário e senha já está confirmada. A [Spec 0002](specs/0002-autenticacao.md) detalha contratos candidatos e 32 cenários futuros, sem encerrar a política.

Pontos de revisão: validar o backend de sessão em banco recomendado no [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md); escolher duração e renovação por atividade/fechamento do navegador, concorrência, efeitos de mudança de senha e revogação global; validar cookies com a implantação. Definir política de credenciais e medidas contra tentativas abusivas sem inventar números. Decidir também o tratamento de resposta perdida de login/logout e de dados abertos ao sair/expirar/trocar conta, em conjunto com P020. As rotas, o form, o destino inicial e a conferência de sessão sem reenvio silencioso de senha são propostas, não escolhas já aceitas.

Encaminhamento: Responsável pelo produto com a equipe técnica.

Quando precisa estar resolvida: 5 a 7, antes da implementação dos controles e da operação real.

Origem: F003; RS003 e RS004. F008; autenticação.

## P015 Hospedagem e operação

Escolher provedor, domínio, ambientes, acompanhamento de falhas e responsáveis operacionais. Para autenticação, validar TLS/proxy, origens, cookies, preparação do backend de sessão escolhido e manutenção dos registros expirados; a Spec 0002 e o ADR 0008 não contratam infraestrutura ou rotina operacional.

Encaminhamento: Responsável pelo projeto e equipe técnica.

Quando precisa estar resolvida: Antes da preparação da operação real.

Origem: F005; seções 8 e 10.

## P016 Arquivos e PDF

Definir armazenamento, entrega privada, coordenação com banco, biblioteca de PDF, formatos, limites e validação dos arquivos.

Encaminhamento: Equipe técnica, após requisitos operacionais.

Quando precisa estar resolvida: Antes das specs e implementação desses recursos.

Origem: F003; RF009, RF015, RS008 e RS010.

## P017 Proteção e retenção

Definir classificação de dados, retenção, acesso à auditoria, proteção em repouso e eliminação conforme a política aprovada.

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
- Criar um app para cada área da visão conceitual não foi decidido. As áreas lógicas foram detalhadas como proposta na [arquitetura](arquitetura.md); o [ADR 0007](adr/0007-monolito-modular.md) recomenda monólito modular, ainda sem aprovação. A estrutura física será detalhada nas specs pertinentes.
- O backend nativo de sessão no servidor com PostgreSQL do [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md) e os contratos da [Spec 0002](specs/0002-autenticacao.md) permanecem Propostos; prazo, tentativas, recuperação e revogação global não foram escolhidos.
- Metas de desempenho, tamanhos, máscaras, fórmulas, identificadores físicos e prazos ainda não aprovados não devem ser tratados como definitivos.

O uso de MVT com services, templates, views derivadas de View e a base de login por usuário/senha deixaram de ser propostas após F008. O registro dessas escolhas está no documento de decisões confirmadas.

## Como encerrar uma pendência

Registrar a resposta, sua origem e data e atualizar as decisões confirmadas e os documentos afetados na etapa correspondente. Preservar o histórico da pergunta sem marcar como decidida apenas porque uma sugestão técnica foi escrita.
