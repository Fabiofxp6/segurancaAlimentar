# Spec 0008 — Documentos do estabelecimento

I07, com RF017, RF010–RF012, RS008, RS010 e RS013–RS014. O estabelecimento envia e consulta seus documentos, vinculados à inspeção da unidade. A equipe fiscal autorizada pode consultá-los. [Decisões confirmadas](../decisoes-confirmadas.md) · [Spec 0007](0007-campo-evidencias-e-reenvio.md)

| Ator | Consulta | Envio |
|---|---|---|
| Conta ativa vinculada à unidade ativa | Lista as inspeções da unidade disponíveis para envio e as que já têm documentos. Consulta a área de documentos. | Da atribuição ao fim do andamento na I07. A I14 inclui complemento após a conclusão. |
| Fiscal ativo responsável ou participante da inspeção | Consulta os documentos recebidos pelo detalhe fiscal. | O envio desta área é exclusivo de Estabelecimento. |
| Outra unidade ou conta desvinculada | A referência direta é recusada. | A referência direta é recusada. |

O fluxo de complemento e parecer depois da conclusão está na [Spec 0015](0015-reanalise-documental.md).

Um documento recebido pode ser consultado enquanto houver vínculo válido. Todas as contas ativas vinculadas à mesma unidade podem consultá-lo. O servidor revalida vínculo, perfil e estado. Uma retentativa de operação confirmada pode recuperar o recibo após o fechamento da janela, enquanto o acesso continuar válido.

## Dados e confirmação

- Inspeção, unidade correspondente, autor da sessão, instante do servidor, nome, formato detectado, tamanho e conteúdo original.
- Descrição opcional de até 1.000 caracteres. A I07 usa categoria comprobatória genérica. Categorias, exigências e regras de complemento ou substituição continuam em P011.
- Na demonstração, PDF, JPEG ou PNG até 5 MiB. PDFs devem abrir no leitor estrutural, ter de 1 a 50 páginas e estar sem senha. Imagens seguem a verificação e o limite de 20 megapixels da I06.
- O PostgreSQL guarda documento e recibo no mesmo registro. Uma chave de operação por inspeção, com autoria, conteúdo e descrição conferidos, garante uma única gravação. Dados divergentes com a mesma chave recebem 409.
- A entrega do arquivo usa anexo com nova checagem de acesso. A área do estabelecimento fornece referência da inspeção, unidade, situação de envio e documentos. Avaliação fiscal, pontuação e termos seguem seus fluxos próprios.

## Reconexão

A página reutiliza o controle da I06, com Pendente, Enviando, Salva e Falha. A confirmação exige retorno do servidor com chave e instante. Durante perda de rede, o arquivo fica em memória na página aberta. Após uma sondagem autorizada, o navegador reenvia a mesma operação. Sessão ou vínculo perdido impede a retentativa. Recarregar ou fechar descarta o envio em memória.

Armazenamento de produção, limites operacionais e retenção continuam em P016/P017/P020. Complementação e regras de substituição permanecem em P011. [Django, respostas de arquivo](https://docs.djangoproject.com/en/5.2/ref/request-response/#fileresponse-objects) · [pypdf, leitor de PDF](https://pypdf.readthedocs.io/en/stable/modules/PdfReader.html)
