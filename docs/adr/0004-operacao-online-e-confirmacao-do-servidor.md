# ADR 0004: Operação online e confirmação do servidor

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** registro de restrição de produto já confirmada; mecanismo técnico pendente.
- **Origem:** DC018 e DC019 nas [decisões confirmadas](../decisoes-confirmadas.md); F003 e F005 no [índice de fontes](../referencias/README.md).

## Contexto

O sistema será utilizado em campo, sujeito à interrupção de comunicação. O usuário descartou inspeção completa offline e confirmou preservação do preenchimento na tela aberta, bloqueio temporário de ações dependentes do servidor e retentativa após reconexão.

## Decisão registrada

O servidor é a fonte oficial. Só indicar dados salvos depois de sua confirmação. A interface distingue Pendente, Enviando, Salva e Falha e conserva o conteúdo atual ao perder comunicação. Repetição da mesma operação não pode produzir outro efeito oficial.

A situação de envio é distinta da situação da inspeção e da decisão sobre uma solicitação. Em especial, a confirmação pode ter sido perdida depois de a gravação acontecer. O mecanismo deve lidar com essa ambiguidade e com concorrência; não basta testar dois envios sequenciais.

## Alternativas e razões

- Inspeção completa offline com sincronização: contradiz a decisão posterior que substituiu o requisito antigo.
- Mostrar salvo antes da confirmação: apresenta como oficial um conteúdo ainda incerto.
- Impedir somente o segundo clique: não trata reenvio após resposta perdida nem solicitações concorrentes.
- Garantir recuperação após fechar/recarregar usando cache persistente: exige decisão ainda não tomada.

As limitações das soluções de retentativa são análise técnica, sem algoritmo ou biblioteca selecionados.

## Consequências

O trabalho depende da disponibilidade do servidor e da rede. A página precisa de interação e mensagens coerentes, além de reconhecimento de operações no servidor. Há custo de coordenação e validação de falhas; a preservação da tela não garante recuperação depois de seu fechamento.

## Pendências e verificação futura

P020 trata de identificação/repetição, intervalo, conflitos, limpeza e eventual persistência no navegador; P019 dos dispositivos. Nas specs pertinentes, prever falha antes do envio, durante o envio, depois da gravação com resposta perdida e em retentativas concorrentes. Não há mecanismo implementado ou teste executado nesta entrega.

Relacionados: RF008, RF010 a RF012, RNF04, RNF14, RS013 e RS014 no [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md); [arquitetura](../arquitetura.md).
