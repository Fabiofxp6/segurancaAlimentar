# Sistema de Avaliação de Segurança Alimentar

Fundação documental de um sistema web para organizar inspeções de segurança alimentar: checklist, respostas, evidências, avaliação, termos e alterações autorizadas com histórico. A Fiscalização executa a inspeção; o Estabelecimento envia documentação própria e consulta resultados finais liberados; o Administrador atua na gestão conforme suas permissões.

## Situação atual

As oito etapas de documentação foram elaboradas e conferidas para revisão do usuário. O catálogo contém **28 RF, 14 RNF e 16 RS**, preservando os 58 IDs. Há três specs e oito ADRs, além da matriz, das skills e dos perfis de agentes.

O PRD, as specs e os ADRs permanecem Propostos. Os ADRs 0001–0006 registram bases já confirmadas; 0007/0008 trazem recomendações novas ainda sem aceite. Entrega documental não equivale a aplicação funcionando, contrato aprovado ou teste de aplicação executado. O [estado](docs/state.md) informa a retomada e as [pendências](docs/pendencias.md) delimitam as decisões que faltam.

## Base confirmada

| Tema | Escolha ou regra |
|---|---|
| Tecnologias | Python com Django e PostgreSQL; versões e preparação ainda abertas |
| Interface e operação | Navegador em tablets/celulares, hospedagem remota e operação somente online |
| Arquitetura | MVT/Django Templates; views próprias diretamente de View; regra/ORM explícito em services sem HTTP, com exceções nativas documentadas |
| Identidade | Usuário customizado AbstractUser, nome de usuário/senha e sessão Django; políticas complementares abertas |
| Perfis | Fiscalização, Administrador e Estabelecimento; Supervisor é fiscal designado por ação, sem quarto perfil |
| Início | Administrador pode atribuir inspeção e fiscal pode iniciá-la diretamente, sem supervisão automática |
| Confirmação | Queda de comunicação preserva a página aberta, bloqueia ações dependentes do servidor e permite recuperação sem salvamento fictício ou efeito duplicado |
| Revisão | Correção após conclusão e cancelamento em andamento exigem autorização, justificativa e história; checklist/regras, resultados e termos anteriores são preservados |
| Estabelecimento | Consulta apenas próprios envios e resultados/documentos finais liberados; anexo não altera nota automaticamente |

Os contratos completos e as decisões abertas estão nos documentos abaixo. Fórmula, limites, tipos físicos, autoridades e prazos ilustrativos não são aprovados por aparecerem em uma tabela ou protótipo.

## Guia de leitura

| Documento | Uso |
|---|---|
| [AGENTS.md](AGENTS.md) e [CLAUDE.md](CLAUDE.md) | Orientações de trabalho e entrada comum para os agentes |
| [Estado](docs/state.md) e [etapas](docs/etapas.md) | Retomada e histórico das oito entregas |
| [Decisões confirmadas](docs/decisoes-confirmadas.md) e [pendências](docs/pendencias.md) | O que foi escolhido e o que ainda depende de resposta |
| [PRD 0001](docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md) | Produto, dados, regras, manutenção e critérios dos 58 requisitos |
| [Arquitetura e ADRs](docs/arquitetura.md) | Responsabilidades, limites e razões das escolhas/propostas |
| [Spec 0001 — fundação](docs/specs/0001-fundacao-tecnica.md) | Estrutura candidata, configuração, PostgreSQL e identidade inicial |
| [Spec 0002 — autenticação](docs/specs/0002-autenticacao.md) | Entrada, saída, sessão, campos, falhas e 32 cenários AU futuros |
| [Spec 0003 — acesso](docs/specs/0003-acesso-vinculos-supervisao.md) | Vínculos, papéis, supervisão, revogação e 36 cenários AC futuros |
| [Matriz de rastreabilidade](docs/matriz-rastreabilidade.md) | Fontes, relações e cobertura documental das 58 entradas; 58 validações VR futuras |
| [Skills e agentes](.agents/README.md) | Onze skills locais e seis perfis, com escopo de uso |
| [Revisão das skills](docs/revisao-skills-tecnicas.md) | Conferência integrada de Python, Django e segurança |
| [Revisão final](docs/revisao-final-fundacao.md) | Coerência do conjunto, verificações e limites de prontidão |
| [Fontes](docs/referencias/README.md) | Ata, PDFs/DOCX, decisões, análise de referência e protótipo, com procedência |
| [Acompanhamento no Trello](docs/acompanhamento-trello.md) | Regra contínua de atualização do quadro e links das atividades |

## Preparação futura

Não há procedimento de instalação/execução da aplicação aprovado nesta entrega. Escolher as versões, o driver e a preparação (P001), os campos/chave do usuário (parte aplicável de P002) e validar os contratos candidatos antes da fundação executável. Não copiar os comandos ou o banco do blog de referência.

Antes de cada funcionalidade, resolver as pendências que a afetam: ação/inspeção, designação e aprovadores; checklist/score; documentos/liberação/ciência; autenticação/recuperação; armazenamento, operação e metas. Não é necessário resolver toda a lista para continuar revisando documentação, mas uma pergunta aberta não pode virar regra implementada por suposição.

`example.env` é um arquivo existente, preservado nesta etapa. Sua presença não certifica valores, ausência de segredos ou carregamento automático; este README não instrui copiá-lo para produção. Nenhum valor real de ambiente integra esta documentação.

## Uso das ferramentas de apoio

As respostas da conversa seguem a preferência de concisão Caveman, enquanto os documentos mantêm o detalhe solicitado. Graphify teve uma tentativa de extração sem retorno completo; o [mapa permanece pendente](docs/registro-graphify.md). Não há economia de tokens ou grafo pronto comprovados. Os perfis TOML foram conferidos, sem comprovação de execução/carregamento automático.

A próxima atividade deve ser solicitada e delimitada pelo usuário: revisar/aprovar documentos, responder decisões ou iniciar um recorte de implementação. A conclusão da Etapa 8 não começa uma nova fase automaticamente.
