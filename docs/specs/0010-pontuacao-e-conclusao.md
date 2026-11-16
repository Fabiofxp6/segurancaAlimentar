# Spec 0010 — Pontuação e conclusão

I09. Implementação da demonstração para RF013/RF014, com RNF04, RF023 e RS013. [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md) · [DC033](../decisoes-confirmadas.md#dc033-pontuação-classificação-e-conclusão-na-i09) · [Plano](../plano-implementacao.md)

## Regra de demonstração

A versão original do checklist identifica a regra `demonstracao-1`. As versões de demonstração existentes recebem essa referência ao aplicar a migração da I09. A versão mantém seus itens, opções e pesos originais.

| Entrada | Efeito |
|---|---|
| Conforme ou Sim | Soma o peso ao numerador e ao denominador. |
| Não conforme ou Não | Soma o peso ao denominador. |
| Não se aplica ou N/A | Exclui o peso do cálculo e conta como resposta para uma pergunta obrigatória. |
| Item opcional sem resposta | Fica fora do cálculo. |
| Item obrigatório sem resposta | Bloqueia a conclusão. |

O percentual corresponde à soma dos pesos conformes dividida pela soma dos pesos aplicáveis, multiplicada por 100. A nota usa duas casas decimais e desempate na metade para cima. A nota arredondada classifica como Satisfatória a partir de 80%, Regular a partir de 60% e Insatisfatória abaixo de 60%. Sem peso aplicável, o resultado é Sem pontuação.

Peso omitido vale 1 no recorte local. Peso zero não contribui, e peso negativo em resposta aplicável ou opção confirmada sem mapeamento impedem o cálculo. O mapeamento de rótulos ignora diferença de maiúsculas. A regra sanitária oficial e a comparabilidade entre versões permanecem em P009/P010.

## Conclusão

Fiscal ativo da equipe atual revisa o checklist e solicita concluir uma inspeção em andamento. A tela aponta itens obrigatórios sem resposta. Novos envios de campo pendentes ou falhos detectados na aba impedem a ação. O armazenamento de sessão do navegador guarda somente identificadores de item e tipo de envio sem confirmação, no escopo da aba, da sessão e da inspeção. O bloqueio do navegador não alcança formulários em outro dispositivo ou aba independente. Documentos do estabelecimento e fotos são opcionais. O servidor só considera registros confirmados e bloqueia a conclusão com pedido de cancelamento pendente.

O servidor revalida o acesso, o estado e a revisão das respostas quando recebe o POST. Se outro envio confirmar resposta depois da abertura da revisão, a tela precisa voltar a conferir os dados. A transação bloqueia a inspeção e grava o resultado, o estado Concluída e um evento oficial. O resultado registra versão, regra, pontuação decimal, classificação, revisões das respostas, autor e data. Se falhar, a transação não confirma a conclusão. A mesma operação confirmada pode recuperar o recibo com acesso atual.

A equipe fiscal e o Administrador consultam o resultado interno. Após concluir, respostas, evidências e documentos já confirmados permanecem acessíveis no escopo anterior. A gravação de campo e o recebimento documental são encerrados. Emissão e liberação ao estabelecimento ficam na I10. Correção e recálculo ficam na I11.

## HTTP e verificação

| Rota | Método | Contrato |
|---|---|---|
| `/inspecoes/<id>/conclusao/` | GET | Revisão para fiscal da equipe. Resultado confirmado para a equipe e Administrador. |
| `/inspecoes/<id>/conclusao/confirmar/` | POST | UUID da operação e revisão das respostas. Exige fiscal da equipe, contexto de sessão e CSRF. Retorna recibo após confirmação. Entrada inválida retorna 400. Mudança de estado, revisão ou dados impeditivos retorna 409. |
| `/inspecoes/<id>/conclusao/conexao/` | GET | Sondagem de reconexão no escopo da inspeção e da sessão. |

Verificar pesos e limites de faixa, N/A e opcionais, ausência de peso aplicável, preservação de versão, acesso negativo, cancelamento pendente, resposta alterada em outra tela, concorrência e falha durante a gravação. Verificar a confirmação recuperada em tela após perda da resposta e o bloqueio local por envio não confirmado.
