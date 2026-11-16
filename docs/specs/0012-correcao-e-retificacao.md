# Spec 0012 — Correção autorizada, recálculo e retificação

I11 de demonstração. Abrange RF018 a RF021 e RF023, com RNF04, RS002, RS007, RS010 e RS013. [DC035](../decisoes-confirmadas.md#dc035-correção-e-retificação-na-i11) · [Pontuação](0010-pontuacao-e-conclusao.md) · [Termo e liberação](0011-termo-e-liberacao.md)

## Escopo e autoridade

| Ato | Permissão e efeito |
|---|---|
| Solicitar | Fiscal ativo da equipe da inspeção concluída. Indica um item do checklist original, resposta, observação e irregularidade propostas, e justifica. O pedido registra a revisão e os valores anteriores. |
| Decidir | Outro supervisor ativo e elegível da ação. O Administrador decide quando não existe outro supervisor elegível. Aprovação e rejeição exigem motivo e ficam vinculadas ao pedido registrado. |
| Aplicar | Fiscal solicitante ativo na equipe ou Administrador. O servidor aplica somente os valores aprovados à revisão indicada e recusa base desatualizada. |
| Consultar | Administrador e fiscais da equipe consultam revisões e pedidos. Supervisores elegíveis de outras inspeções da ação podem acessar pedidos no escopo da ação. |

A escolha de um item por solicitação serve à demonstração. A I14 permite vincular à solicitação o parecer de reanálise de um documento complementar. Mudanças em andamento e política sanitária oficial seguem nos seus recortes. [Spec 0015](0015-reanalise-documental.md) A inspeção permanece Concluída. Os registros de campo originais e seus arquivos continuam associados às respostas coletadas em campo.

## Revisões e documentos

Pedidos e decisões são registros separados e imutáveis. Ao aplicar, o servidor cria uma revisão de resultado, preserva checklist e regra originais e registra executor, data e vínculo com a decisão. A nova revisão guarda as respostas confirmadas com o ajuste aprovado. O cálculo da demonstração produz nota e classificação da revisão e permite consultar as anteriores. A revisão inicial existente passa a ter número 1.

Se houver termo emitido e a nova revisão alterar a nota, a classificação, a lista de não conformidades ou as descrições impressas, aplicar gera um termo retificador com versão, código e referência ao PDF anterior. O motivo interno permanece no pedido. Observação de campo que não altera o PDF gera revisão sem nova emissão. A primeira emissão posterior à correção usa a revisão atual quando ainda não havia termo.

O resgate de acesso depende de cada versão liberada. O retificador exige nova liberação por autoridade da I10. A versão já liberada permanece disponível e aparece como anterior quando a mais nova é liberada. O PDF original conserva seus bytes. O recorte mantém `DEMO-<inspeção>-Vnn` e não define vigência jurídica.

## Consistência e verificação

Solicitação, decisão e aplicação usam POST com CSRF, contexto da sessão e UUID. A mesma operação confirmada recupera seu recibo no escopo permitido. A aplicação grava revisão, auditoria e eventual retificador na mesma transação. Concorrência, conflito de revisão ou falha de geração impedem duplicidade ou publicação parcial.

| Método | Caminho relativo a `/inspecoes/` |
|---|---|
| GET | `correcoes/` para fila e `<id>/correcoes/` para revisões e pedidos da inspeção |
| GET | `<id>/correcoes/item/<item>/` para preparar e `<id>/correcoes/<pedido>/` para revisar |
| POST | `<id>/correcoes/item/<item>/solicitar/` |
| POST | `<id>/correcoes/<pedido>/decidir/` e `<id>/correcoes/<pedido>/aplicar/` |
| GET | `<id>/correcoes/conexao/` para recuperar comunicação e `<id>/termo/<termo>/` para consultar uma emissão exata |

Verificar cada autoridade, retirada de designação, autoaprovação, pedido pendente/rejeitado, escopo de item, concorrência, falha de gravação, reenvio, regra original, imutabilidade e disponibilidade das versões no portal. Consultar lista e resultado da correção apenas no fluxo interno. [Transações do Django](https://docs.djangoproject.com/en/5.2/topics/db/transactions/)
