# I07 — Documentos do estabelecimento

Entrega local em 16/11/2026. O estabelecimento pode enviar documentos da atribuição ao fim do andamento. Todas as contas ativas vinculadas à unidade ativa podem consultar e baixar os documentos da unidade. O fiscal ativo da equipe consulta os documentos recebidos. [DC031](decisoes-confirmadas.md#dc031-documentos-do-estabelecimento-na-i07) · [Spec 0008](specs/0008-documentos-do-estabelecimento.md)

## Fluxo entregue

- A área do estabelecimento lista as inspeções disponíveis para documentos. A avaliação interna fica no fluxo fiscal.
- O documento é registrado separado da evidência fiscal, com autor, data, referência da inspeção e formato detectado. Seu recebimento preserva a inspeção e as respostas. Pontuação e termos serão tratados nas etapas previstas.
- O navegador usa a mesma chave ao reenviar após perda de comunicação. A confirmação permanece ligada ao registro original. Outros dados com a mesma chave geram conflito. O download revalida vínculo ou equipe, inclusive após revogação em sessão aberta.

## Verificações

- **77 testes** passaram no PostgreSQL isolado, incluindo 9 da I07. Os testes cobrem envio na atribuição e em andamento, arquivo inválido, acesso direto por terceiro, revogação, conflito, concorrência e recuperação de recibo.
- O bloqueio de novos envios após a janela foi testado com fechamento simulado. A transição real de conclusão faz parte da I09.
- No Chromium a 360 px, o servidor gravou um PDF e a confirmação foi interrompida. O navegador recuperou o recibo com a mesma chave. Outra conta da unidade baixou o mesmo arquivo. O banco conservou um único documento e o checklist permaneceu intacto. Também foi verificada a regressão do fluxo de respostas e fotos da I06.

## Escolhas do recorte local

O usuário decidiu a janela, os formatos de demonstração e a consulta por unidade. A implementação usa PostgreSQL para o conteúdo original e limite de 5 MiB por arquivo. PDF passa por verificação estrutural com pypdf 7.1.0, com 1 a 50 páginas e sem senha. JPEG e PNG seguem os limites de imagem da I06. A descrição é opcional. [pypdf 7.1.0](https://pypi.org/project/pypdf/7.1.0/)

Categorias, complementar ou substituir documentos, retenção e armazenamento de produção continuam em P011/P016/P017. A retentativa de um envio pendente usa a memória da página aberta. Fechar ou recarregar descarta essa cópia temporária.

[Como testar](../README.md#demonstrar-documentos-do-estabelecimento) · [Cartão da I07](https://trello.com/c/tgD8DFk1)
