---
name: adr
description: Criar e revisar decisões de arquitetura do Sistema de Avaliação de Segurança Alimentar em docs/adr/. Use em escolhas estruturais, alternativas com impacto relevante ou substituição de decisão anterior; contratos de funcionalidades ficam nas specs.
---

# Decisões de arquitetura

Consultar o [estado](../../../docs/state.md), as [etapas](../../../docs/etapas.md), a [arquitetura](../../../docs/arquitetura.md), as [decisões confirmadas](../../../docs/decisoes-confirmadas.md) e os ADRs relacionados. Conferir o [PRD](../../../docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md) e as [pendências](../../../docs/pendencias.md) afetadas. Atualizar o [acompanhamento no Trello](../../../docs/acompanhamento-trello.md) durante o trabalho e na entrega.

## Quando registrar

Usar ADR para uma escolha estrutural que afete várias áreas, tenha alternativas relevantes ou seja custosa de reverter. Uma mudança local e reversível pode ser descrita na spec; um ADR não substitui requisitos, contratos ou instruções de implementação.

Respeitar a etapa solicitada. Elaborar um ADR não autoriza criar código, instalar dependências, contratar serviços ou avançar para outra etapa.

## Arquivo e conteúdo

Criar em `docs/adr/NNNN-titulo-em-kebab-case.md`, usando o próximo número livre de quatro dígitos. Não renumerar nem reutilizar IDs. Tratar uma decisão por arquivo e registrar:

- Status, data e natureza: registro de escolha já confirmada ou proposta nova.
- Contexto e origem: decisões, requisitos, pendências e fontes pertinentes.
- Decisão, ou proposta quando ainda não aprovada.
- Alternativas consideradas, com razões e limites concretos.
- Consequências, incluindo pelo menos um custo ou risco.
- Pontos ainda abertos e verificação futura proporcional à escolha.

Escrever em português direto. Distinguir razão técnica inferida de justificativa expressa pelo usuário. Não inventar histórico de avaliação, prova de desempenho ou decisão da equipe.

## Situação das decisões

Novo documento começa como `Proposto`. Se registrar uma escolha anterior confirmada, citar sua origem e deixar explícito que o status documental não reabre essa escolha. Uma recomendação nova continua proposta; autorizar a etapa ou redigir o arquivo não a aprova.

Usar `Aceito` quando houver aprovação expressa do ADR, com origem e data registradas. Usar `Rejeitado` ou `Substituído por ADR NNNN` quando essa for a decisão real. Preservar o arquivo e seu identificador.

Não reescrever silenciosamente a decisão de um ADR aceito. Para contrariá-la, apresentar um novo ADR que exponha a mudança e suas consequências; aguardar a decisão necessária antes de executar trabalho dependente. Prosseguir com o trabalho independente já autorizado. Quando a substituição for aprovada, ligar os dois registros e atualizar a arquitetura e as specs afetadas.

## Regras do projeto a preservar

- Python/Django, PostgreSQL, MVT, Templates, views derivadas de `View`, services independentes de HTTP e autenticação de base já têm confirmação registrada. Não recuperar escolhas do blog como se fossem nossas.
- Supervisor é fiscal designado por ação. Não aprovar autoridade, autoaprovação, agrupamento de ações ou representação física de perfis por inferência.
- Operação online, confirmação do servidor, autorização, histórico e preservação das versões são restrições do produto.
- Versões, hospedagem, armazenamento, PDF e políticas abertas continuam no registro de pendências. Exemplos de tipos, máscaras e números não resolvem essas escolhas.

## Conferência e encerramento

Conferir links, IDs, origem da escolha, alternativas, custos e coerência entre decisão e proposta. Relacionar os requisitos existentes sem criar IDs para cada detalhe técnico. Não criar specs ou outras skills apenas para completar links.

Atualizar os documentos de continuidade e o Trello com o resultado real. Verificações documentais não são testes executados da aplicação. Esta skill é local; sua existência não comprova carregamento automático, e o [AGENTS da raiz](../../../AGENTS.md) orienta a retomada conforme o estado atual.
