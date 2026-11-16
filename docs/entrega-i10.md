# Entrega I10 — Termo em PDF e liberação ao estabelecimento

Verificada em ambiente de demonstração em 16/11/2026. [Spec 0011](specs/0011-termo-e-liberacao.md) · [DC034](decisoes-confirmadas.md#dc034-emissão-e-liberação-do-termo-na-i10) · [Trello](https://trello.com/c/hRPoPeN7)

## Fluxo entregue

O fiscal da equipe ou o Administrador emite o PDF após a conclusão confirmada. O Administrador ou o supervisor ativo da ação revisa o termo emitido e libera o resultado em uma ação separada. Cada operação gera seu próprio evento de auditoria.

O arquivo inclui identificação da inspeção e da unidade, versão, resultado, itens não conformes e descrições das irregularidades registradas nas revisões confirmadas. As observações gerais, fotos e deliberações internas ficam restritas ao fluxo autorizado de fiscalização.

O estabelecimento consulta a lista de resultados, abre os detalhes e baixa a versão liberada. Cada solicitação confere o vínculo atual com a unidade. O arquivo baixado mantém os bytes gravados na emissão.

## Verificação

| Cenário | Resultado |
|---|---|
| Emissão e conteúdo | O PDF identifica a versão e contém a pontuação, o resultado e as descrições da revisão usada. A inspeção continua concluída com falha de geração. |
| Autorização | Fiscal da equipe emite. Administrador e supervisor ativo da ação liberam. Fiscal sem designação e supervisor de outra ação recebem negativa. Revogação tem efeito na mesma sessão. |
| Portal | Bloqueia acesso antes da liberação, entre unidades e após perda de vínculo. Contas ativas da mesma unidade podem consultar e baixar. |
| Consistência | Pedidos concorrentes produziram uma emissão e uma liberação. Falha na auditoria reverte o ato. O banco protege os registros contra alteração e exclusão. |
| Navegador móvel | Chromium a 360 px recuperou a confirmação da emissão e da liberação após perda de resposta. O download do portal correspondeu aos bytes armazenados. |
| PDF | Conferência de texto com pypdf e revisão visual do exemplo baixado e de quatro páginas de descrições longas. |

**102 testes** passaram no PostgreSQL, incluindo seis de emissão, liberação e acesso ao PDF. O check do Django e a verificação de migrações passaram. [Como demonstrar](../README.md#demonstrar-emissão-e-liberação)

## Limites da demonstração

O termo inicial usa numeração `DEMO-<inspeção>-V01`. A geração usa ReportLab, em uma solicitação após a conclusão, e o servidor guarda o PDF no PostgreSQL. Política oficial de modelos, numeração, vigência, assinatura, ciência e armazenamento de produção segue em P012/P013/P016. Correção, recálculo e retificação ficam na I11. [Pendências](pendencias.md) · [Plano](plano-implementacao.md)
