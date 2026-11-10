---
name: seguranca-aplicacao
description: Revisar ou especificar controles de acesso, sessão, entradas, arquivos e proteção de dados do sistema alimentar. Use em mudanças sensíveis ou revisão de segurança solicitada; não aprova políticas legais, MFA ou criptografia ainda pendentes.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Segurança da aplicação

Consultar os RS e RF relacionados no [PRD](../../../docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md), a [arquitetura](../../../docs/arquitetura.md), a spec afetada e [pendências](../../../docs/pendencias.md). Delimitar os dados, o ator, as entradas e o efeito analisado. Não executar varredura de serviço externo ou ação destrutiva como parte de revisão documental.

Verificar acesso no servidor para consultas, alterações e downloads, por identidade, perfil, vínculo e ação. Supervisor não é permissão global; administrador técnico não é autoridade sanitária. Revisar revogação, pedido próprio e aprovações conforme a política realmente definida, sem preencher lacunas por inferência.

Manter os mecanismos do Django para senha, sessão, CSRF e escape da apresentação. Não criar autenticação paralela, implementar criptografia própria ou inserir tokens JWT por conveniência. Recuperação, limites de tentativa, MFA, prazos e revogação continuam em P014 até decisão expressa.

Revisar validação de entrada e referências, acesso direto a arquivos, formato/tamanho/conteúdo de anexo e origem dos dados. Distinguir documento do estabelecimento de evidência fiscal e de termo emitido. Não apresentar arquivo pendente como recebido ou confiar apenas no nome e tipo declarado.

Conferir separação dos ambientes, segredos, tráfego protegido e registros sem credenciais ou conteúdo sensível desnecessário. Retenção, acesso à auditoria, chaves e proteção em repouso dependem das políticas abertas; não declarar conformidade legal ou certificação a partir de uma lista de controles.

Para operações oficiais, analisar confirmação perdida, reenvio, concorrência, correção autorizada e preservação do histórico. `atomic`, log técnico e botão oculto não substituem os controles correspondentes.

Relatar achados com evidência, condição de exploração, impacto e correção proporcional. Separar problema confirmado, hipótese e decisão pendente. Não inventar nota de segurança, teste executado ou vulnerabilidade sem caminho demonstrável. Correções seguem o escopo autorizado; avaliações de ameaça completas só entram quando solicitadas.

Atualizar o [Trello](../../../docs/acompanhamento-trello.md) com o trabalho efetivamente realizado. Origem e adaptações: [registro da curadoria](../../../docs/curadoria-skills-agentes.md).
