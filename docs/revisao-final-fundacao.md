# Revisão final da fundação documental — Etapa 8

- **Data:** 10/11/2026.
- **Situação:** elaboração e conferência documentais concluídas, para revisão do usuário.
- **Escopo:** consolidar orientações da raiz e revisar a coerência das oito etapas. Não inclui implementação, aceite automático dos contratos ou execução da aplicação.

## Resultado da consolidação

Foram preparados [AGENTS](../AGENTS.md), [CLAUDE](../CLAUDE.md) e [README da raiz](../README.md). AGENTS concentra retomada, fontes, escopo, invariantes e uso seletivo de skills; CLAUDE aponta para a mesma orientação, evitando uma segunda versão das regras; README apresenta o sistema, a situação real e o mapa dos documentos.

Os pontos atuais de continuidade no PRD, arquitetura, specs, matriz, catálogo e skills documentais foram atualizados. Referências que ainda anunciavam as Etapas 7 ou 8 como próximas passaram a apontar ao estado final das entregas. Notas históricas de cada etapa foram preservadas e identificadas; não são substitutas do [estado vigente](state.md).

Não foi necessário mudar regra funcional, campo de referência, prioridade, critério de aceite ou autoridade de negócio. Os 58 requisitos e as 183 entradas de dados RF foram preservados. As oito etapas foram elaboradas, não aprovadas automaticamente; a implementação permanece uma fase posterior a ser solicitada e delimitada.

## Coerência entre os artefatos

| Artefato | Conferência e papel no conjunto | Situação/limite |
|---|---|---|
| [Referências](referencias/README.md) | Nove fontes identificadas, com cópias/representações e decisões posteriores distinguidas | Originais preservados; F003/F004 e F005/F006 não são catálogos duplicados |
| [Decisões](decisoes-confirmadas.md) e [pendências](pendencias.md) | DC001–DC022 preservadas; P001–P022 continuam abertas | Sem escolha nova de versão, autoridade, tipo físico ou política por inferência |
| [PRD](prd/0001-sistema-avaliacao-seguranca-alimentar.md) | 28 RF, 14 RNF e 16 RS, dados/regras e verificações detalhados | Proposto; RF014 mantém bloqueios adicionais como proposta, RF027/RF028 exigem validar fluxo |
| [Arquitetura e ADRs](arquitetura.md) | Camadas e exceções nativas coerentes com as três specs; oito ADRs existentes | 0001–0006 registram base confirmada; 0007/0008 recomendam modularidade/backend de sessão, ainda não aceitos; todos os registros documentais seguem Propostos |
| [Fundação](specs/0001-fundacao-tecnica.md) | PostgreSQL, configuração externa, identidade customizada e migração inicial delimitados | Proposta, 12 VF futuros; versões/chave/campos bloqueiam a parte correspondente da execução |
| [Autenticação](specs/0002-autenticacao.md) | Campos, View/form/sessão, CSRF, destino seguro, falhas e confirmação coerentes | Proposta, 32 AU futuros; backend/configuração e políticas complementares continuam abertos |
| [Acesso](specs/0003-acesso-vinculos-supervisao.md) | Perfil-base, vínculo, supervisão contextual, efetivação e revogação separados | Proposta, 36 AC futuros; nenhuma autoridade automática de aprovação |
| [Matriz](matriz-rastreabilidade.md) | 58 entradas ligadas à origem, outros requisitos, cobertura documental e validação | Proposta, 58 VR futuros; cobertura parcial não é atendimento implementado |
| [Skills/agentes](../.agents/README.md) | Onze skills locais e seis perfis TOML, com referências válidas | Formatos conferidos, sem comprovar execução ou seleção automática |
| [Revisão das skills](revisao-skills-tecnicas.md) | Python, Django e segurança continuam alinhadas às três specs | Nove situações examinadas no papel, sem teste independente de comportamento |
| [Estado](state.md), [etapas](etapas.md) e [Trello](acompanhamento-trello.md) | Situação vigente e histórico distinguidos; oito entregas registradas | Aguardam revisão e nova atividade delimitada; nenhuma etapa de implementação iniciada |

## Invariantes conferidas

- Python/Django/PostgreSQL substituem Java/SQLite; MVT, Templates, View/services e identidade local seguem a base confirmada. O ORM interno de autenticação/form/sessão/Admin permanece uma exceção documentada, sem mover HTTP para services.
- Existem três perfis-base. Supervisor continua fiscal designado por ação; início direto, equipe, perfil administrativo ou flag técnica não concedem designação ou aprovação. Vínculo/escopo/vigência são verificados no servidor, inclusive após revogação.
- Estabelecimento não recebe avaliação interna ao enviar documento. Conclusão não equivale a liberação do resultado; consultas e downloads dependem do vínculo e da versão/documento autorizado.
- Operação online, preservação da página aberta, bloqueio temporário, recuperação e confirmação do servidor não viram inspeção offline. Reenvio precisa evitar outro efeito oficial; o tratamento de credenciais em resposta perdida continua proposta específica em P014/P020.
- Correção concluída e cancelamento em andamento continuam sujeitos a autorização, justificativa e história. Checklist/regras originais, resultados anterior/novo e termos emitidos são preservados; novo anexo não altera a avaliação automaticamente.
- Campos UUID, máscaras, tamanhos, duração, fórmula, cardinalidade de supervisores e regras legais não foram escolhidos pela transcrição ou pela criação das orientações da raiz.

## Verificações documentais

Foram conferidos os links locais ativos do conjunto, os 58 IDs/títulos do catálogo, as 183 entradas de dados RF, os IDs das decisões/pendências e as referências entre documentos. Os textos originais arquivados não foram reescritos para reparar diferenças históricas; sua integridade é conferida pelo manifesto.

Os 138 cenários existentes permaneceram preservados: 12 VF, 32 AU, 36 AC e 58 VR. Seus enunciados não foram convertidos em testes passados ou marcações de implementação. As alterações nas specs/PRD/matriz se restringem à orientação de continuidade e aos links, sem reescrever seus contratos.

As 11 skills foram conferidas pelo validador oficial de formato disponível. Os seis TOML foram lidos com parser e suas referências locais verificadas, sem editar perfis ou executar agentes. A integridade foi comparada por inventário antes/depois: somente os arquivos Markdown definidos para esta entrega foram gravados. Fontes, avisos/licenças, manifestos históricos, decisões, pendências, arquivos de ambiente e metadados Git foram preservados.

Essas são verificações de arquivos e coerência documental. Não foram executados Django, instalação, banco/migração, testes de aplicação, captura de interface, carga, restauração ou implantação. Não há afirmação de desempenho, conformidade legal, validade de assinatura ou funcionamento operacional.

## Instruções de ferramentas e limites de validação

O AGENTS foi preparado na raiz do projeto `Documents/segurancaAlimentar`. A descoberta de instruções do Codex depende do contexto de execução e dos arquivos aplicáveis; a criação de um arquivo nesta sessão não comprova que outra sessão o carregou. A orientação de raiz foi conferida na [documentação oficial OpenAI sobre AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md). Não foram mudadas configurações globais, fallback de nomes ou permissões para forçar esse carregamento.

CLAUDE contém uma orientação de leitura comum; não foi validado por execução em outra ferramenta nem tratado como importação automática. Os perfis TOML continuam disponíveis conforme seu catálogo, sem alegação de terem sido executados. A tarefa seguinte deve começar na raiz correta e retomar o estado, sem confundir o espelho do ChatGPT com o repositório do projeto. O AGENTS do espelho não foi alterado.

O [mapa Graphify permanece pendente](registro-graphify.md). A tentativa da Etapa 6 não produziu fragmentos finais; esta etapa não a reiniciou nem publicou mapa, cache semântico ou economia medida como concluídos. Respostas concisas seguem a preferência Caveman, preservando o conteúdo dos artefatos.

## Prontidão e decisões antes da próxima fase

| Próximo recorte possível | O que precisa de revisão/decisão antes da execução correspondente |
|---|---|
| Preparar fundação executável | Validar a parte aplicável da Spec 0001 e proposta estrutural; resolver P001 e a parte de identidade P002 antes das migrações |
| Implementar autenticação | Validar contratos novos e backend/configuração; resolver a parte pertinente de P014/P015/P020, sem aprovar todas as políticas por existir login |
| Implementar vínculos/supervisão | Resolver P002–P006 na parte aplicável: representação, ação/inspeção, designação, autoridade e pedido próprio; testar revogação e concorrência |
| Checklist, cálculo e execução | Validar P009/P010 e regras de conclusão; preservar versões e definir o mecanismo de confirmação/conflito conforme P020 |
| Documentos, publicação e ciência | Resolver P011–P013/P016 e modelos/regras de liberação, retificação, assinatura e entrega privada |
| Operar remotamente | Resolver hospedagem, logs, proteção/retenção, metas/recuperação e homologação pertinentes a P015/P017–P021; priorização/estimativas em P022 |

Não é necessário resolver todas as pendências para pedir um ajuste documental ou examinar uma decisão. Cada execução futura precisa somente dos bloqueios que realmente a afetam, mas não pode preenchê-los silenciosamente. O protótipo de cancelamento continua sujeito à revisão em P021; sua aparência não prevalece sobre RF022/DC012.

As oito entregas oferecem uma base documental revisável, não um certificado de prontidão integral. O próximo passo é o usuário revisar o conjunto e solicitar uma atividade delimitada; nenhuma instalação, código ou fase seguinte foi iniciada pela conclusão da Etapa 8.
