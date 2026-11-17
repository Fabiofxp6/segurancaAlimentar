# Pendências e propostas

Atualizado em 16/11/2026, com a fundação I01 e as entregas locais I02 a I12.

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

Resolvida em DC029. Uma ação pode reunir várias inspeções. A I05 persiste a ação e usa sua chave para relacionar inspeções e designações. [Spec 0006](specs/0006-inicio-equipe-e-supervisao.md)

Encaminhamento: Responsável pelo processo de fiscalização.

Evidência: agrupamento de duas inspeções na mesma ação, com vínculo persistido. [Entrega da I05](entrega-i05.md)

Origem: F003; RF002. F005; seção 5.

## P004 Designação do supervisor

Decidida para a I05 em DC029. Administrador designa, substitui e encerra. A ação admite vários fiscais ativos da equipe designados em paralelo, com designação opcional e de efeito imediato. A operação mantém histórico e uma designação aberta por fiscal na ação. A política de aprovação permanece em P005.

Encaminhamento: Responsável pelo processo de fiscalização.

Evidência: designações simultâneas, isolamento por ação e revogação na sessão atual. [Entrega da I05](entrega-i05.md)

Origem: F003; RF002 e RS002.

## P005 Autoridade aprovadora

DC032 definiu a autoridade para RF022. Outro supervisor ativo e elegível da ação decide, com o Administrador na ausência de outro elegível. O solicitante fica impedido de decidir. DC035 aplica a mesma regra de decisão à correção de demonstração. A aplicação cabe ao solicitante ativo na equipe ou ao Administrador. Definir política de correção de produção. [Spec 0012](specs/0012-correcao-e-retificacao.md) [Spec 0009](specs/0009-cancelamento-e-auditoria.md)

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: 6 e specs de autorização, antes da implementação.

Origem: F003; RF018, RF022 e RS002.

## P006 Alterações durante o andamento

DC032 definiu o bloqueio de novas respostas, fotos e documentos durante pedido de cancelamento pendente. A rejeição libera os registros permitidos. DC035 cobre correção após a conclusão de um item por pedido na demonstração. Delimitar as demais mudanças que exigem autorização, alterações em andamento e o alcance dos fluxos documentais.

Encaminhamento: Responsável pelo processo de fiscalização.

Quando precisa estar resolvida: Specs funcionais posteriores.

Origem: F003; RF018 e RF022.

## P007 Adiamento

DC038 resolve o adiamento da demonstração para inspeção Atribuída, com justificativa, data proposta e autoridade por ação. A política de operação real continua em aberto. [Spec 0014](specs/0014-adiamento.md)

Encaminhamento: Responsável pelo produto e pelo processo.

Quando precisa estar resolvida: Antes de detalhar e implementar o fluxo de adiamento.

Origem: F003; RF027.

## P008 Reanálise documental

DC038 define envio de complemento após a conclusão e parecer por fiscal da equipe. Eventual correção segue a I11, sem nova visita no recorte acadêmico. Prazos, obrigatoriedade e política de operação real continuam em aberto. [Spec 0015](specs/0015-reanalise-documental.md)

Encaminhamento: Responsável pelo produto e pelo processo.

Quando precisa estar resolvida: Antes de detalhar e implementar reanálise.

Origem: F003; RF028.

## P009 Checklist e governança

Escolher referência sanitária, itens, obrigatoriedade, opções de resposta e responsáveis por publicar versões oficiais. No ambiente local, a I04 permite ao Administrador editar rascunhos e publicar versões de demonstração com dados fictícios. [Spec 0005](specs/0005-checklist-e-versoes.md) · [Entrega da I04](entrega-i04.md)

Encaminhamento: Equipe e profissionais que validam a avaliação.

Quando precisa estar resolvida: Antes de aceitar conteúdo sanitário oficial ou habilitar sua publicação e uso em inspeções reais.

Origem: F001; tópico 1. F003; RF004 e RF007.

## P010 Pontuação

A I09 usa o percentual ponderado, a exclusão de N/A e as faixas confirmadas em DC033 para a demonstração. A I12 apresenta médias em grupos separados por versão e regra. Definir fórmula, pesos, N/A, arredondamento, faixas de classificação e comparabilidade para uso oficial. [Spec 0010](specs/0010-pontuacao-e-conclusao.md)

Encaminhamento: Responsável pela avaliação, com apoio da equipe.

Quando precisa estar resolvida: Antes de aprovar cálculo sanitário ou indicadores oficiais.

Origem: F003; RF013, RF020 e RF026.

## P011 Documentos do estabelecimento

DC031 definiu envio da atribuição ao fim do andamento, consulta por conta ativa da unidade e PDF/JPEG/PNG para demonstração. Na I09, os documentos são opcionais para concluir a demonstração, conforme DC033. Definir categorias, exigências, limites de produção, complementação e substituição. [Spec 0008](specs/0008-documentos-do-estabelecimento.md)

Encaminhamento: Responsável pelo processo, com apoio técnico.

Quando precisa estar resolvida: antes de habilitar políticas adicionais de documento ou aceitar uso real.

Origem: F003; RF017 e RS008.

## P012 Resultado final e termos

DC034 define emissão e liberação separadas para a demonstração. DC035 exige nova liberação para retificador e mantém as versões já liberadas. Definir liberação oficial, modelos, numeração, vigência, nova versão ou termo retificador e tratamento de inspeção concluída inválida. [Spec 0011](specs/0011-termo-e-liberacao.md)

Encaminhamento: Responsável pelo processo e pela validação documental.

Quando precisa estar resolvida: Antes de publicar termos oficiais, retificar ou anular.

Origem: F003; RF015, RF016, RF021 e RF022.

## P013 Assinatura e ciência

Escolher forma de identificação, assinatura, ciência e tratamento aplicável ao documento oficial.

Encaminhamento: Responsável pelo processo e pela validação documental.

Quando precisa estar resolvida: Antes de implementar RF025.

Origem: F001; tópico 2. F003; RF025.

## P014 Políticas complementares de acesso

Definir recuperação de conta, senha, MFA/SSO, limitação de tentativas, expiração, sessões simultâneas e revogação. A base Django de usuário e senha já está confirmada. O fluxo básico da [Spec 0002](specs/0002-autenticacao.md) foi implementado e verificado localmente na [I02](entrega-i02.md).

O backend nativo de sessão em PostgreSQL foi adotado na I02 conforme o [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md). Falta escolher duração de produto, renovação por atividade, efeito do fechamento do navegador, concorrência e revogação global. Permanecem em aberto a entrega de credenciais reais, os efeitos da reativação sobre sessões antigas, as medidas contra tentativas abusivas e a validação dos cookies na implantação. DC039 permite definir e redefinir senhas de contas gerenciáveis pela web. O mecanismo nativo recusa a sessão anterior do titular após redefinição. O tratamento de resposta perdida e de dados abertos ao sair, expirar ou trocar conta depende de P020.

Encaminhamento: Responsável pelo produto com a equipe técnica.

Quando precisa estar resolvida: 5 a 7, antes da implementação dos controles e da operação real.

Origem: F003; RS003 e RS004. F008; autenticação.

## P015 Hospedagem e operação

Escolher provedor, domínio, ambientes, acompanhamento de falhas e responsáveis operacionais. Para autenticação, validar TLS, proxy, origens, cookies, preparação do backend PostgreSQL em produção e manutenção dos registros expirados. A I02 verificou a configuração local. A I13 ensaiou HTTPS local. DC037 define que a entrega da faculdade roda localmente. Hospedagem, domínio, HTTPS externo e responsáveis ficam para a operação futura. [Roteiro da I13](entrega-i13.md)

Encaminhamento: Responsável pelo projeto e equipe técnica.

Quando precisa estar resolvida: Antes da preparação da operação real.

Origem: F005; seções 8 e 10.

## P016 Arquivos e PDF

Definir armazenamento e entrega privada em produção, coordenação com banco, biblioteca de PDF, formatos, limites e validação de arquivos reais. A I06 usou PostgreSQL para JPEG/PNG de demonstração. A I07 validou PDF/JPEG/PNG de documentos no mesmo banco, em registros próprios e com download por autorização. A I10 usa ReportLab e armazena o PDF emitido no PostgreSQL de demonstração. Armazenamento e entrega de produção permanecem pendentes. [Spec 0011](specs/0011-termo-e-liberacao.md)

Encaminhamento: Equipe técnica, após requisitos operacionais.

Quando precisa estar resolvida: Antes das specs e implementação desses recursos.

Origem: F003; RF009, RF015, RS008 e RS010.

## P017 Proteção e retenção

Definir classificação de dados, retenção, acesso à auditoria, proteção em repouso e eliminação conforme a política aprovada. A I03 grava autoria, data e mudanças de cadastro e vínculos na transação do ato. A I08 reúne a trilha por inspeção para Administrador e fiscais da equipe atual. O banco protege os eventos de inspeção e recibos de campo contra alteração ou exclusão. Retenção, auditoria geral e acesso de produção seguem em aberto. [Spec 0009](specs/0009-cancelamento-e-auditoria.md)

Encaminhamento: Responsável pelo processo e equipe técnica.

Quando precisa estar resolvida: Antes do desenho final e da operação real.

Origem: F003; RS006, RS007 e RS012.

## P018 Metas e recuperação

Levantar usuários, carga, volume de arquivos, disponibilidade, tempos, backup, perda máxima de dados e tempo de recuperação. A I13 restaurou o PostgreSQL com anexos e termos fictícios em outro banco. Os tempos desse ensaio descrevem apenas essa base. Frequência, retenção operacional e metas do piloto seguem abertas. [Evidências da I13](entrega-i13.md#evidências-locais)

Encaminhamento: Responsável pelo produto e equipe técnica.

Quando precisa estar resolvida: Antes dos testes de desempenho e da operação real.

Origem: F003; RNF02, RNF03, RNF06 e RNF11.

## P019 Compatibilidade e acessibilidade

Homologar navegadores, versões, dispositivos, critérios de acessibilidade, captura de foto e alternativa por arquivo. O ensaio da I13 usou Chromium nas larguras de 360 e 820 px. A homologação em dispositivos físicos continua prevista. [Evidências da I13](entrega-i13.md#evidências-locais)

Encaminhamento: Usuários representativos com a equipe técnica.

Quando precisa estar resolvida: Antes de aceitar a interface e os fluxos em campo.

Origem: F003; RNF01, RNF07 e RNF08.

## P020 Pendências na tela e reenvio

A I06 preserva na página aberta um envio solicitado, confirma por chave única, sonda o servidor na reconexão e recupera a mesma operação. A I07 reutiliza o mesmo controle para documentos do estabelecimento. Validação/conflito exigem ação do usuário. Permanecem em aberto a política após fechar ou recarregar, a retenção do histórico de operações, os intervalos de produção e a limpeza em aparelhos compartilhados. [Spec 0007](specs/0007-campo-evidencias-e-reenvio.md)

Na [Spec 0002](specs/0002-autenticacao.md), validar com P014 a proposta específica para credenciais: depois de resposta perdida, conferir a sessão por leitura e permitir nova tentativa explícita quando necessário, sem reenvio silencioso de senha. Isso ainda não aprova uma exceção à retentativa geral. Definir limpeza/proteção de outras abas e de dados pendentes ao sair, expirar ou trocar conta; não presumir salvamento nem descarte desses dados.

Encaminhamento: Equipe técnica com validação do produto.

Quando precisa estar resolvida: Antes de ampliar a recuperação para outros fluxos ou fixar a política operacional.

Origem: F003; RF011, RNF14 e RS014.

## P021 Revisão dos protótipos

A interface local passou a usar o protótipo RF-08 e adaptou o cancelamento ao fluxo de solicitação e autorização. Os limites e campos seguem as specs da demonstração. O artefato original permanece como referência histórica. Validação em dispositivos físicos segue em P019. [Entrega da interface](entrega-interface-rf08.md)

Encaminhamento: Equipe com validação de usuários.

Quando precisa estar resolvida: Antes de usar as telas como especificação de comportamento.

Origem: F009; tela 10 e exemplos. F003; RF022.

## P022 Priorização e estimativas

DC036 define acesso administrativo e indicadores de demonstração para I12. Validar prioridades do catálogo, exportações, escopo da primeira versão e do piloto, responsáveis, esforço, prazo e orçamento. Não há calendário de implementação aprovado.

Encaminhamento: Responsável pelo projeto com a equipe.

Quando precisa estar resolvida: 2 para escopo proposto; antes de comprometer entregas de software.

Origem: F003; prioridades A validar. F005; seções 11 e 12.

## Propostas preservadas como propostas

- O agrupamento por ação foi definido em DC029. O escopo operacional de aprovação e ausências segue em P005.
- A política de adiamento e reanálise para operação real depende de P007 e P008. A demonstração segue DC038.
- Criar um app para cada área da visão conceitual não foi decidido. As áreas lógicas foram detalhadas como proposta na [arquitetura](arquitetura.md); o [ADR 0007](adr/0007-monolito-modular.md) foi aceito para a fundação. A estrutura física será detalhada nas specs pertinentes.
- A retomada assistida da [Spec 0002](specs/0002-autenticacao.md) permanece proposta. Prazo de expiração, tentativas, recuperação e revogação global ainda dependem de decisão.
- Metas de desempenho, tamanhos, máscaras, fórmulas, identificadores físicos e prazos ainda não aprovados não devem ser tratados como definitivos.

A [matriz de rastreabilidade](matriz-rastreabilidade.md) liga as 58 entradas às fontes, relações e validação futura; não encerra P001 a P022. Os dados/rotas/services da Spec 0003 são Propostos e não implementam acesso.

O uso de MVT com services, templates, views derivadas de View e a base de login por usuário/senha deixaram de ser propostas após F008. O registro dessas escolhas está no documento de decisões confirmadas.

## Como encerrar uma pendência

Registrar a resposta, sua origem e data e atualizar as decisões confirmadas e os documentos afetados na etapa correspondente. Preservar o histórico da pergunta sem marcar como decidida apenas porque uma sugestão técnica foi escrita.
