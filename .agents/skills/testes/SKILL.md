---
name: testes
description: Planejar, executar e revisar verificações de comportamento do sistema alimentar, incluindo serviços, PostgreSQL, HTTP e navegador. Use nas alterações autorizadas ou ao especificar cenários; registrar separadamente testes futuros, escritos e executados.
license: Consulte ../../third-party/NOTICE.md e os avisos MIT e Apache-2.0 indicados ali.
---

# Testes e evidências

Partir da spec e dos requisitos afetados. Conferir [estado](../../../docs/state.md), [arquitetura](../../../docs/arquitetura.md), ambiente e dados disponíveis. Enquanto o trabalho for documental, descrever cenários sem criar aplicação para executá-los e sem marcá-los como aprovados.

Escolher verificações proporcionais ao risco e ao comportamento alterado. Evitar teste de detalhe interno que apenas reproduza a implementação e teste novo para mudança reversível de baixo impacto sem justificativa. Não impor percentual de cobertura ou suíte adicional que não tenha decisão no projeto.

Quando houver função implementada e execução autorizada, verificar caminho válido, entrada inválida, acesso negado, estado incompatível e falha pertinente. Em operações críticas, incluir duas ações/estabelecimentos distintos, designação revogada, conflito e gravação confirmada com resposta perdida, conforme a spec.

Usar PostgreSQL isolado nos cenários de banco, verificando destino e credenciais antes de qualquer preparação. Não usar produção, apagar banco existente ou trocar por SQLite para obter um resultado verde. Testes de transação e concorrência precisam representar os limites reais; mock não prova integridade do banco ou atomicidade com arquivos.

No navegador, usar ferramentas disponíveis e elementos observados. Aguardar a condição que comprova o resultado, como resposta confirmada ou estado de envio, em vez de espera fixa ou ociosidade de rede como único critério. Validar rótulos, teclado, telas móveis e estados com texto quando pertinentes. Ferramenta de teste não escolhe framework da aplicação; não instalar Playwright ou dependências automaticamente.

Dados de teste devem ser mínimos, fictícios e independentes. Capturas, console e logs não devem expor credenciais ou dados reais de estabelecimentos. Encerrar servidores/processos temporários iniciados pelo próprio teste sem interromper processos do usuário.

Relatar comando ou ferramenta, ambiente, escopo, resultado e limitações. Distinguir não executado, escrito e executado com sucesso; ausência de ferramenta não é teste passado. Só marcar `[x]` com evidência de execução pertinente. Depois dos testes adequados passarem, repetir ou ampliar apenas se houver mudança, falha ou dúvida que justifique.

Registrar o resultado no [Trello](../../../docs/acompanhamento-trello.md). Origem e adaptações: [registro da curadoria](../../../docs/curadoria-skills-agentes.md).
