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

## Revisão visual e de acessibilidade — 17/11/2026

A revisão aplicou o azul do RF-08 à navegação, às ações e aos estados compartilhados entre acesso, fiscalização, gestão e portal. No desktop, o detalhe da inspeção organiza os atalhos e os indicadores usam barras proporcionais ao total da consulta. No portal, os cartões de documentos e resultados funcionam como uma área inteira de acesso. O celular conserva os controles compactos e as abas do item. [DESIGN.md](../DESIGN.md)

Os formulários revisados apresentam um resumo dos erros com foco por teclado. A remoção de item do rascunho pede confirmação, com foco inicial em Voltar. Os títulos de página indicam o contexto e a interface solicita aos buscadores que não indexem suas páginas. A apresentação dos estados de envio evita repetir atualizações iguais no DOM.

O ambiente isolado passou os 128 testes Django. O fluxo RF-08 e as áreas por perfil foram exercitados no Chromium em sete larguras entre 360 e 1.920 px, incluindo navegação por teclado, abertura e fechamento de diálogos, queda de conexão e reenvio sem duplicação. Em 12 telas e estados, o axe-core não reportou violações nas regras WCAG 2.0 e 2.1 de níveis A e AA selecionadas. Navegadores fora do Chromium e dispositivos físicos seguem sem validação nesta revisão. [P019](pendencias.md#p019-compatibilidade-e-acessibilidade) · [Trello](https://trello.com/c/RUDd8LLh)

## Restauração visual do acesso — 17/11/2026

A pedido do usuário, o acesso recuperou o degradê azul, os arcos, a sombra suave e a tipografia da versão a59c033. As mudanças visuais ficam nos blocos do acesso em sistema.css e desktop.css. O Chromium conferiu sete larguras entre 360 e 1.920 px, navegação por teclado, mostrar/ocultar senha e foco nos erros. O axe-core passou nas regras WCAG 2.0 e 2.1 A/AA selecionadas para celular e desktop. [Trello](https://trello.com/c/RNon82ya/103-restaurar-visual-anterior-da-tela-de-acesso)
