# Entrega I09 — Pontuação, classificação e conclusão

Verificada em ambiente de demonstração em 16/11/2026. [Spec 0010](specs/0010-pontuacao-e-conclusao.md) · [Trello](https://trello.com/c/BENAuj0o)

## Fluxo entregue

O fiscal da equipe abre **Revisar para concluir** no checklist ou no detalhe da inspeção. O servidor confere o estado, o acesso, as respostas obrigatórias e a revisão da base. A tela também bloqueia a conclusão quando um envio de campo da aba está pendente ou falhou. Documentos do estabelecimento são opcionais nessa etapa.

O resultado usa a versão original do checklist. Conforme ou Sim soma o peso e Não conforme ou Não soma zero. Não se aplica sai da base. A nota arredondada a duas casas determina a classificação. A partir de 80%, Satisfatória. De 60% a menos de 80%, Regular. Abaixo de 60%, Insatisfatória. Sem peso aplicável, o resultado é Sem pontuação. [DC033](decisoes-confirmadas.md)

O servidor grava resultado, estado **Concluída** e evento oficial na mesma transação. Depois da conclusão, respostas, fotos e documentos anteriores continuam consultáveis conforme o vínculo. O resultado fica disponível para equipe e Administrador. Emissão de termo e liberação ao estabelecimento são etapas da I10.

## Verificação

| Cenário | Resultado |
|---|---|
| Pesos, limites e versão | Conferidos os limites de 60% e 80% antes e após arredondamento, N/A, base sem peso aplicável e preservação da nota após publicação de outra versão. |
| Estado e acesso | Resposta obrigatória ausente, cancelamento pendente, sessão fora do escopo e base alterada bloqueiam a conclusão. O estabelecimento não acessa o resultado interno. |
| Concorrência e falha | Dois pedidos concorrentes geram um resultado. Falha durante a gravação reverte resultado e estado. O banco protege a conclusão e o resultado gravados. |
| Navegador móvel | Chromium a 360 px confirmou bloqueio por falha de foto, liberação após reenvio, recuperação do recibo perdido, nota de 80,00% e evento na auditoria. No banco ficaram um resultado, um evento e a foto preservada. |
| Compatibilidade | Migração em banco isolado com uma versão publicada antes da I09 preservou itens e regras e registrou o identificador da regra de demonstração. |

**96 testes** passaram na suíte PostgreSQL, incluindo **10** de pontuação e conclusão. A verificação do Django passou e o detector de migrações não encontrou alterações pendentes. [Como demonstrar](../README.md#demonstrar-pontuação-e-conclusão)

## Limites da demonstração

Peso omitido vale 1. Peso zero não contribui e respostas opcionais em branco ficam fora do cálculo. A regra usa arredondamento na metade para cima. O aviso de envio da tela usa o armazenamento de sessão da aba para guardar identificadores dos itens, sem conteúdo de respostas ou fotos. Outras abas e dispositivos têm seus próprios estados. O servidor calcula sobre registros confirmados em todos os casos.

Conteúdo sanitário, fórmula e faixas oficiais, comparabilidade e exigências documentais seguem em P009/P010/P011. [Pendências](pendencias.md) · [Plano](plano-implementacao.md)
