---
name: revisao-codigo
description: Revisar alterações implementadas do sistema alimentar por correção, acesso, integridade, regressão e manutenção. Use quando houver pedido de revisão ou mudança substancial a avaliar; não confundir revisão de código com aprovação de requisito ou implementação de correção.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Revisão de alterações

Identificar o recorte, a spec e a mudança real. Ler [arquitetura](../../../docs/arquitetura.md), decisões/pendências pertinentes e o contexto necessário ao redor dos arquivos alterados. Se ainda não existe implementação, informar o limite da análise e revisar apenas o artefato efetivamente solicitado.

Priorizar defeitos com consequência concreta: acesso fora de ação/estabelecimento, autorização contornada no Admin, alteração retroativa, duplicação, perda de preenchimento, cálculo pelas regras erradas e exposição de dados. Verificar também transação, concorrência, versões e falhas de arquivos quando alcançadas pela mudança.

Conferir se os testes pertinentes existem e o que foi realmente executado. Não inventar cobertura, nota de qualidade ou resultado de ferramenta. Executar uma verificação apenas quando ela for útil, disponível e compatível com o escopo de revisão.

Cada achado deve indicar arquivo/linha quando aplicável, condição que o dispara, impacto e correção sugerida. Distinguir defeito demonstrável, risco condicionado e política não decidida. Evitar comentários puramente de estilo, relatórios com pontuações arbitrárias e exigência de elogios para preencher um modelo.

Revisão não autoriza corrigir, publicar comentário em PR, fazer commit, merge ou implantação. Prosseguir com correções se já tiverem autorização no pedido; preservar alterações do usuário e limitar a mudança ao problema. Não disparar especialistas automaticamente.

Entregar os achados mais importantes primeiro ou registrar que não houve achado relevante, com as limitações da verificação. Atualizar o [Trello](../../../docs/acompanhamento-trello.md) sem declarar a função concluída só por haver uma revisão.

Origem e adaptações: [registro da curadoria](../../../docs/curadoria-skills-agentes.md).
