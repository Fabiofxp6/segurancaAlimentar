---
name: prd
description: Criar ou revisar PRDs do Sistema de Avaliação de Segurança Alimentar, incluindo requisitos, perfis, escopo e critérios de conclusão. Use em mudanças de comportamento do produto; detalhes de implementação pertencem às specs.
---

# PRD do sistema alimentar

## Consultar antes de escrever

- Ler [estado](../../../docs/state.md), [etapas](../../../docs/etapas.md) e o PRD afetado, se existir.
- Consultar [decisões confirmadas](../../../docs/decisoes-confirmadas.md), [pendências](../../../docs/pendencias.md) e o [índice de fontes](../../../docs/referencias/README.md).
- Usar o [catálogo de origem](../../../docs/referencias/catalogo-requisitos-origem.md) para preservar identificadores e conferir o documento revisado quando houver dúvida de conteúdo. As decisões posteriores atualizam os pontos correspondentes das fontes antigas.
- Respeitar a etapa e o trabalho solicitados. Escrever ou revisar um PRD não autoriza implementar software ou avançar para outra etapa.

## Conteúdo e localização

Criar em `docs/prd/NNNN-titulo-em-kebab-case.md`, com o próximo número de quatro dígitos disponível. Alterar o PRD existente quando a mudança pertencer ao mesmo produto e objetivo. Criar outro quando houver um objetivo ou versão de produto distinto que justifique separação.

O documento deve informar status, data, objetivo, perfis, escopo, requisitos funcionais, requisitos não funcionais, requisitos de segurança, limites e critérios de conclusão. Identificar fontes e specs relacionadas; se uma spec ainda não existe, registrar sua etapa prevista sem criar link quebrado.

Preservar o detalhamento funcional das fontes: quem faz o quê, condições de uso, dados, regras de preenchimento, fluxos, caminhos de falha, alteração, exclusão, consulta e critérios de aceite. Não reduzir um requisito completo a uma descrição e uma frase de verificação.

Campos, tipos e máscaras já presentes nas fontes podem e devem aparecer no PRD como referência de dados quando necessários à compreensão. Identificar o que é confirmado, sugerido ou pendente e não converter UUID, Enum, UploadedFile ou estrutura de informação em escolha física aprovada. Preservar todos os dados pertinentes da fonte, explicando quando são calculados, verificados pelo servidor, condicionais ou ainda sem obrigatoriedade definida.

As specs detalham contratos de implementação, métodos, rotas, models, relacionamentos físicos, índices, migrações e decisões técnicas validadas. ADRs guardam as razões estruturais. A separação entre documentos não deve apagar do PRD o detalhe de produto existente no documento de requisitos; não criar specs antecipadamente apenas para deslocar informação para outro lugar.

## Identificação e situação dos requisitos

- Preservar `RF001` a `RF028`, `RNF01` a `RNF14` e `RS001` a `RS016` do catálogo alimentar. Não importar a numeração do blog ou do PDF antigo como se fosse a atual.
- Não renumerar nem reutilizar identificadores. Requisitos novos recebem o próximo ID da sua família, após verificar o catálogo e o PRD atual. Registrar sua origem e atualizar a rastreabilidade na etapa pertinente.
- Não apagar requisito retirado de escopo sem preservar o ID e a razão da retirada. Não criar IDs novos apenas para subdividir os critérios de um requisito existente.
- Separar comportamento definido, detalhamento pendente e proposta a validar. A presença no catálogo não aprova políticas em aberto. RF027 tem fluxo pendente; RF028 é proposta de reanálise.
- Manter prioridades, metas, fórmulas e limites ainda não aprovados como pendentes, com referência à pergunta correspondente. Não transformar números de protótipo em regras.

## Regras de redação

- Usar português direto e os termos Fiscalização, Administrador, Estabelecimento e Supervisor. Cliente é o estabelecimento; Supervisor é fiscal designado por ação.
- Para RF, incluir ID, comportamento, participantes, condições, dados de referência, fluxo, regras, manutenção/consulta, critérios de aceite e pendências aplicáveis. Omitir apenas o que não se aplicar, explicando o limite.
- Para RNF, preservar alcance, parâmetros/unidades de medição, regras, procedimento de verificação e metas ainda abertas. Para RS, preservar risco, dados, controles, manutenção, verificação e políticas pendentes.
- Usar critérios observáveis de sucesso e de falha. Quando o aceite depender de decisão, explicitar a dependência; não tratar um parâmetro sem meta aprovada como teste de aceite completo.
- Preservar as decisões de operação online, confirmação do servidor, autorização, histórico e versões. Não recuperar uma regra antiga de offline ou cancelamento direto.
- Não atribuir poder de aprovação ao administrador, permitir autoaprovação ou definir agrupamento de ações sem decisão correspondente.
- Registrar uma proposta como proposta. Se faltar uma decisão indispensável ao pedido atual, pedir esclarecimento; se ela puder permanecer aberta sem comprometer a entrega, referenciar a pendência e continuar o trabalho autorizado.
- Evitar duplicar políticas e decisões em vários lugares. Referenciar o registro responsável e atualizar os documentos existentes afetados quando o comportamento mudar.

## Status e encerramento

Novo PRD começa como `Proposto`. `Aceito` depende de aprovação expressa do responsável sobre o PRD; a autorização para redigir uma etapa não é essa aprovação. Decisões já confirmadas continuam válidas mesmo com o PRD global proposto.

Ao concluir, conferir:

- Correspondência dos IDs e conteúdos com as fontes e decisões atuais, sem transformar propostas em obrigações aprovadas.
- Cobertura dos campos, formatos, regras, manutenção e verificações da fonte por requisito; qualquer síntese deve preservar o conteúdo relevante e justificar mudança ou exclusão.
- Critérios de aceite e ligações das pendências, sem metas ou permissões inventadas.
- Links locais válidos e ausência de dependências documentais fictícias.
- Coerência com specs e ADRs existentes; indicar o trabalho futuro quando ainda não existirem.
- Estado e etapa atualizados com o resultado real. Não marcar testes ou funções como executados/implementados por haver apenas documentação.

Esta skill é local ao projeto. Sua presença em disco não comprova carregamento automático por uma ferramenta; a leitura é orientada pelo [AGENTS da raiz](../../../AGENTS.md), sem comprovar que uma sessão o carregou automaticamente.
