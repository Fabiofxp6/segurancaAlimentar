---
name: interface-web
description: Especificar, implementar ou revisar telas responsivas e acessíveis em Django Templates para o sistema alimentar, conforme o pedido. Use em formulários, checklist, evidências e estados de envio; não adota React, Vue ou biblioteca visual por inferência.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Interface web do sistema

Consultar o requisito, a spec e o protótipo pertinentes, a [arquitetura](../../../docs/arquitetura.md) e [pendências](../../../docs/pendencias.md). Distinguir desenho ilustrativo de regra aprovada: nomes, limites, percentuais, obrigatoriedade e dados de exemplo não são contratos automaticamente.

Manter Django Templates e HTML semântico como base confirmada, com CSS responsivo e interação complementar conforme a necessidade. Não criar frontend independente, bundler, Tailwind, React ou outra dependência por fazer parte da coleção externa.

Projetar leitura e preenchimento em tablets/celulares, com rótulos, mensagens associadas aos campos, foco visível e estados reconhecíveis além da cor. A homologação de dispositivos, navegadores e critérios formais de acessibilidade continua em P019; não inventar nota ou certificação.

Distinguir estado da inspeção, da solicitação de autorização e do envio. Em perda de conexão, preservar o conteúdo na página aberta, informar pendência, bloquear ações dependentes do servidor e permitir retentativa conforme a spec. Só exibir salvo depois da confirmação. Não acrescentar inspeção offline ou cache persistente sem decisão.

Não calcular resultado oficial, decidir permissão ou efetivar cancelamento apenas na interface. Pedido de cancelamento exige justificativa e autorização antes do efeito; o protótipo antigo precisa ser alinhado. Estabelecimento não recebe dados internos por um controle visual oculto.

Quando o pedido for imagem/protótipo, entregar o artefato solicitado sem criar software como efeito colateral. Quando houver implementação autorizada, validar os fluxos atingidos com a [skill de testes](../testes/SKILL.md), usando ferramentas e ambientes disponíveis e evidência do comportamento observado.

Registrar a entrega e as pendências no [Trello](../../../docs/acompanhamento-trello.md). Origem e adaptações: [registro da curadoria](../../../docs/curadoria-skills-agentes.md).
