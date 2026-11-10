# Fontes do projeto

Organizado em: 10/11/2026. Entrega da Etapa 1, com fontes disponíveis e decisões recentes registradas. Este índice organiza referências; não é um PRD.

## Ordem de consulta

1. Ler o [estado atual](../state.md) e as [etapas acordadas](../etapas.md).
2. Consultar as [decisões confirmadas](../decisoes-confirmadas.md), as [pendências](../pendencias.md) e F008, que registra escolhas posteriores às fontes antigas.
3. Usar F003/F004 como catálogo detalhado e F005/F006 como visão geral, observando os pontos atualizados por F008.
4. Usar F001/F002 para origem e histórico e F007 como referência de organização documental. F009 é somente referência visual.

## Inventário

| ID | Fonte local | Data documental | Uso e situação |
|---|---|---|---|
| F001 | [Ata de levantamento](arquivos/Ata_Reuniao_Seguranca_Alimentar_Detalhada.docx) | 01/10/2026; revisão de 06/10/2026 | Contexto, inspeção em campo, evidências, termos e ciência das partes. Score ainda complementar na ata. |
| F002 | [Requisitos originais CESMAC](arquivos/Especificacao_Requisitos_CESMAC_2026-10-13.pdf) | 13/10/2026 | Histórico de 11 RF. O RF09 de offline completo foi substituído por decisão posterior. |
| F003 | [Requisitos revisados editáveis](arquivos/Documento_Requisitos_Python_Django_Revisado.docx) | 09/11/2026 | Catálogo de referência com 28 RF, 14 RNF e 16 RS; inclui propostas e definições abertas. |
| F004 | [Requisitos revisados PDF](arquivos/Documento_Requisitos_Python_Django_Revisado.pdf) | 09/11/2026 | Representação em PDF de F003; não é outro catálogo de requisitos. |
| F005 | [Visão geral editável](arquivos/Documentacao_Geral_Projeto_Seguranca_Alimentar.docx) | 09/11/2026 | Objetivos, escopo, ciclo, dados, viabilidade e propostas técnicas anteriores ao planejamento de 10/11. |
| F006 | [Visão geral PDF](arquivos/Documentacao_Geral_Projeto_Seguranca_Alimentar.pdf) | 09/11/2026 | Representação em PDF de F005; não constitui aprovação adicional. |
| F007 | [Análise independente da referência](arquivos/Analise_Projeto_Referencia_Para_Fundacao.md) | 09/11/2026 | Referência de organização de PRD, skills, specs, arquitetura, estado e AGENTS. Suas propostas não eram decisões aprovadas naquele momento. |
| F008 | [Decisões recentes e autorização por etapas](decisoes-conversa-2026-11-10.md) | 10/11/2026 | Resumo das confirmações expressas do usuário e do escopo de execução; complementa e atualiza as fontes anteriores. |
| F009 | [Protótipo de referência](arquivos/Prototipo_RF08_refinado.png) | Artefato de referência anterior às decisões mais recentes | Ilustrativo. A tela de cancelamento ainda não demonstra solicitação e aprovação; textos, números e limites não são regras aprovadas. |

## Como tratar diferenças entre fontes

Uma decisão expressa posterior atualiza somente os pontos a que se refere; ela não aprova automaticamente todo o documento anterior. As cópias de referência são preservadas, sem corrigir seu texto retroativamente. A interpretação atual fica nos registros de decisões e pendências.

- O RF09 do PDF original prevê offline completo; a escolha posterior é online com preservação em tela e confirmação do servidor.
- A escolha antiga de Java e a ADR de SQLite do blog não valem para este projeto: Python, Django e PostgreSQL estão confirmados.
- A análise de 09/11 ainda chama MVT, templates, View e autenticação de propostas ou escolhas abertas. F008 confirma o padrão arquitetural e a base de usuário/senha e sessão Django.
- Cancelamento agora exige autorização antes da efetivação. A tela 10 do protótipo ainda mostra confirmação apenas com justificativa; ela não substitui a regra atual.
- Ter um requisito no catálogo não significa que suas prioridades, metas, campos e políticas abertas foram aprovados. RF027 possui fluxo pendente; RF028 é proposta de reanálise.

## Catálogo e rastreabilidade de origem

O [catálogo de origem](catalogo-requisitos-origem.md) transcreve somente identificadores e títulos de F003: 28 RF, 14 RNF e 16 RS, totalizando 58 entradas. F004 é a versão em PDF desse mesmo documento. Não contar as duas versões como requisitos diferentes.

Os IDs do PDF original e os da referência de blog têm numeração própria. Não renumerar o catálogo alimentar por semelhança de título. O catálogo não é o PRD da Etapa 2 nem a matriz de rastreabilidade da Etapa 6.

## Preservação e atualização

Os oito arquivos copiados mantêm seu conteúdo original. O nome do PDF CESMAC foi normalizado para facilitar o uso local; o nome e caminho de origem estão no [manifesto de fontes](manifesto-fontes.json), junto de tamanho e SHA-256. F008 é um resumo novo da conversa e está identificado como tal.

Novas revisões devem ser adicionadas e identificadas antes de substituir referências usadas por decisões. Os caminhos de origem no manifesto documentam procedência; a leitura do pacote usa links relativos e não depende de Downloads ou do chat.

Não foram consultadas ou alteradas contas externas nem sincronizado o Trello nesta etapa. Nenhum arquivo do blog foi modificado.
