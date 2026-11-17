# Interface web baseada no protótipo RF-08

**Escopo.** Revisão solicitada em 16/11/2026 para todo o frontend. O protótipo RF-08 guiou a barra azul, a marca do acesso, os cartões, as abas, os estados de envio e a organização do fluxo do fiscal. As telas de gestão, do estabelecimento e de erro usam os mesmos componentes. [Protótipo de referência](referencias/README.md) · [Trello](https://trello.com/c/pNg9DDKy)

## Fluxos da demonstração

| Parte do protótipo | Comportamento na aplicação |
|---|---|
| Acesso, lista e detalhe | Acesso com exibição opcional da senha. Inspeções com abas, busca por unidade ou número e filtros. Detalhe com equipe, versão do checklist e atalhos. |
| Checklist, resposta e irregularidade | Progresso calculado com as respostas confirmadas. A tela preserva a resposta e a irregularidade entre as duas abas. O título da versão identifica o conjunto de itens. |
| Estados, resumo e falta de conexão | Legenda de Pendente, Enviando, Salva e Falha. O resumo distingue respostas confirmadas dos envios desta aba. Durante uma falha de comunicação, preserva o preenchimento, bloqueia o envio e tenta confirmar ao reconectar. A sondagem também pode ser acionada por botão. |
| Observações gerais | Fiscal da equipe registra texto de até 1.000 caracteres durante o andamento autorizado. A gravação gera recibo idempotente e evento de auditoria. Os registros confirmados ficam disponíveis em leitura após conclusão ou cancelamento. |
| Galeria | Fotos confirmadas com miniaturas e download restritos à equipe. Arquivos do estabelecimento aparecem em uma aba separada e conservam origem e autorização próprias. |
| Cancelamento | Tela de justificativa e solicitação. A decisão continua reservada ao supervisor elegível ou ao Administrador na ausência de outro elegível, segundo DC032. |

A observação do item segue opcional no recorte local. A captura de foto usa a opção disponibilizada pelo navegador. O resumo mantém o bloqueio de conclusão com respostas obrigatórias ausentes ou envios pendentes ou falhos na aba. [Spec de campo](specs/0007-campo-evidencias-e-reenvio.md) · [Spec de conclusão](specs/0010-pontuacao-e-conclusao.md)

## Layout desktop

A tela de acesso põe a marca e o formulário em duas áreas. A partir de 1.024 px na escala padrão do navegador, as telas internas usam navegação lateral por perfil e a lista de inspeções organiza os dados em colunas. A partir de 1.184 px, o detalhe da inspeção, o registro com evidências, as observações e o resumo passam a aproveitar duas colunas. Em telas menores, o menu compacto e as abas do item mantêm o fluxo do protótipo. Redimensionar a janela preserva os valores digitados. [Trello](https://trello.com/c/I9hMFnXg)

## Verificação

Django e as migrações conferidos. A suíte de 123 testes passou no PostgreSQL isolado. O Chromium foi exercitado a 360, 390, 820 e 1280 px. O ensaio cobriu acesso, listagem, checklist, resposta, retentativa sem duplicação, upload, miniaturas, observações, estado final do cancelamento, conclusão, gestão e portal do estabelecimento. Câmera em dispositivo físico e validação em outros navegadores seguem em P019. [Pendências](pendencias.md#p019-compatibilidade-e-acessibilidade)

A adaptação desktop foi verificada no Chromium a 1.024, 1.280, 1.440 e 1.920 px. O ensaio nos tamanhos móveis e no tablet foi repetido.
