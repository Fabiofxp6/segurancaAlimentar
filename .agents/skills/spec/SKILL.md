---
name: spec
description: Criar e revisar especificações técnicas do Sistema de Avaliação de Segurança Alimentar em docs/specs/, com contratos de dados, comportamento, acesso, falhas e validação. Use antes de implementar uma funcionalidade ou ao alterar seu contrato; decisões estruturais pertencem aos ADRs.
---

# Especificações técnicas

Consultar [estado](../../../docs/state.md), [etapas](../../../docs/etapas.md), [arquitetura](../../../docs/arquitetura.md), [PRD](../../../docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md), [decisões](../../../docs/decisoes-confirmadas.md) e [pendências](../../../docs/pendencias.md). Ler os ADRs e specs afetados e conferir as fontes quando necessário. Atualizar o [Trello](../../../docs/acompanhamento-trello.md) durante o trabalho e na entrega.

## Escopo e arquivo

Criar ou atualizar a spec antes da implementação do contrato. Corrigir a documentação quando uma mudança autorizada alterar o comportamento; uma correção que apenas cumpra a spec não exige reescrever o contrato.

Usar `docs/specs/NNNN-titulo-em-kebab-case.md`, com próximo número livre de quatro dígitos, sem renumerar ou reutilizar IDs. Relacionar dependências reais e evitar ciclos; numeração não autoriza execução nem substitui a sequência acordada. Specs futuras devem ser indicadas por etapa/tema, sem link para arquivo inexistente.

Respeitar o recorte solicitado. Uma spec de fundação não deve antecipar contratos completos de autenticação, supervisão ou inspeção. Autorização para documentar não autoriza implementar, instalar dependências ou avançar de etapa.

## Conteúdo aplicável

Omitir seções que não se apliquem, mas declarar os limites relevantes. Registrar:

- Status, objetivo, escopo, fontes, RF/RNF/RS existentes e ADRs relacionados.
- Dependências, escolhas confirmadas, propostas e decisões que bloqueiam cada parte da execução.
- Estrutura afetada e contratos concretos de configuração ou integração.
- Para dados: campo, tipo, obrigatoriedade, origem, formato/máscara quando aplicável, validação, relações, restrições e índices necessários.
- Para services: entrada/saída, ator confiável, autorização, invariantes, transação, falhas e efeitos; não escolher classe ou DTO sem necessidade.
- Para HTTP: rota, nome, método, view, acesso, resposta e caminhos de erro; explicar quando não há rota no escopo.
- Forms, templates e Admin conforme a função; nenhuma entrada pode contornar a regra do caso de uso.
- Consistência, concorrência, repetição, versões e arquivos quando pertinentes.
- Critérios de aceite e cenários futuros, ligados ao requisito ou contrato que verificam.

Não preencher número, tipo de identificador, fórmula, limite, máscara ou poder de aprovação por suposição. Propor um contrato revisável quando houver base; marcar o que está pendente e o ponto exato que não pode ser executado antes da decisão. Uma spec com lacunas bloqueantes não está pronta para implementação integral.

## Regras do sistema

Preservar os IDs do catálogo alimentar e distinguir atendimento parcial de atendimento completo. Não criar RF para cada configuração interna nem marcar um requisito como implementado por existir uma spec. Se o produto mudar, atualizar o PRD com a decisão real antes de especificar a mudança como obrigação.

Seguir MVT e os limites da arquitetura: views próprias derivam de `View`; services concentram regras e ORM explícito da aplicação sem depender de HTTP; forms validam entrada; models representam persistência; templates apresentam. As exceções do framework/Admin estão na arquitetura.

Separar autenticação, perfil-base e designação de Supervisor por ação. Manter operação online, confirmação do servidor, autorização, histórico e versões. Não importar campos Java, prioridades antigas ou regras do blog como contratos atuais.

Se uma escolha estrutural nova for necessária, registrar a proposta em ADR, sem apresentá-la como aprovada. Usar a [skill de ADR](../adr/SKILL.md) quando esse trabalho fizer parte do pedido; não abrir outra frente documental apenas para preencher um link.

## Situação e entrega

Nova spec começa como `Proposto`; aprovação documental deve ter origem e data registradas e não equivale a implementação. Usar `Implementado` somente quando código e verificações necessárias cumprirem o escopo aplicável, com evidências e limitações reais. Não considerar contratos bloqueantes concluídos enquanto dependerem de decisão.

Deixar cenários não executados desmarcados. Marcar `[x]` apenas com execução bem-sucedida e evidência correspondente; comandos descritos ou testes apenas escritos não são testes passados.

Conferir contratos, dependências, IDs, links e coerência com arquitetura e requisitos. Ligar a spec no PRD e atualizar estado, etapas e Trello. A presença local desta skill não comprova descoberta automática; o AGENTS será preparado na etapa prevista.
