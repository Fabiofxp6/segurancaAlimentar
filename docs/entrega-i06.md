# I06 — Checklist em campo, evidências e rede

Entrega local em 16/11/2026. O fiscal ativo da equipe pode abrir a inspeção em andamento, responder itens da versão vinculada, informar observação, registrar irregularidade e anexar fotos. A página exibe a situação da resposta e da foto separadamente.

## O que foi verificado

- A gravação e o registro de confirmação ocorrem na mesma transação. Resposta de outra versão, opção inválida, alteração com revisão antiga e anexos inválidos são recusados.
- O download de evidências valida o escopo no servidor. A mesma operação pode ser recuperada sem duplicar dados, inclusive quando duas tentativas correm em paralelo. Perda de sessão impede o reenvio automático daquela página.
- **68 testes** passaram no PostgreSQL isolado, com 9 novos testes da I06. Foram verificados idempotência, concorrência, rollback, validação de arquivos, controle de acesso, conflito e vínculo com a versão original.
- No Chromium a 360 px, a simulação de rede desligada manteve o texto na página e bloqueou a ação. Foram interrompidas as respostas de rede depois da gravação de um item e de uma foto. As duas retentativas foram confirmadas com as chaves originais. O banco ficou com uma resposta e uma foto. Uma tentativa de foto inválida exibiu falha sem alterar a confirmação da resposta.

## Escolhas do recorte e limites

A demonstração aceita imagens JPEG e PNG estáticas, uma por envio, até 5 MiB e 20 megapixels. As fotos ficam no PostgreSQL com os bytes originais. A biblioteca Pillow 12.3.0 valida o conteúdo. PDFs, HEIC, formatos definitivos, armazenamento de produção e testes de câmera em aparelho real seguem em P016/P019. [Pillow 12.3.0](https://pypi.org/project/pillow/12.3.0/)

Um envio solicitado permanece em memória na tela aberta. A reconexão exige uma resposta da sondagem ao servidor. A proteção de página usa a sessão atual e a retentativa só mantém o pacote enquanto a página permanece aberta. A recuperação após fechar/recarregar e a política de dados em aparelhos compartilhados continuam em P020.

A validação sanitária oficial depende de P009. Documentos enviados pelo estabelecimento ficam na I07. Pontuação e conclusão da inspeção ficam na I09.

[Spec 0007](specs/0007-campo-evidencias-e-reenvio.md) · [Como testar](../README.md#demonstrar-preenchimento-e-evidências) · [Cartão da I06](https://trello.com/c/bvM4tCUH)
