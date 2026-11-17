# Spec 0007 — Checklist em campo, evidências e reenvio

I06, com RF008–RF012, RNF14 e os controles aplicáveis de RS008–RS010 e RS013–RS014. A inspeção usa a versão fixa registrada na I05. [Spec 0006](0006-inicio-equipe-e-supervisao.md) · [Pendências](../pendencias.md)

## Resposta do item

| Dado | Tipo | Regra no recorte local |
|---|---|---|
| Inspeção e item | Chave da inspeção e UUID do item | O servidor valida o vínculo com a versão original. Fiscal com conta ativa e membro da equipe, em inspeção em andamento. |
| Resposta | Texto dentre as opções da versão | Obrigatória para gravar. A marca de item obrigatório vem do checklist e será aplicada também na conclusão em I09. |
| Observação | Texto opcional, até 1.000 caracteres | Preservada na tela aberta ao perder comunicação. |
| Irregularidade | Marcação e descrição de até 1.000 caracteres | Marcação exige descrição. A ausência de marcação salva sem descrição. |
| Revisão | Inteiro, zero antes da primeira gravação | O servidor rejeita edição desatualizada. |
| Operação e confirmação | UUID e data/hora do servidor | Recebimentos iguais para a mesma operação retornam a confirmação existente. O mesmo identificador com outro conteúdo recebe conflito. |

A gravação mantém uma resposta atual por item e um registro das operações confirmadas, com autor, dados, revisão e instante. Mudança de equipe e perfil é revalidada. A autorização de correção ou cancelamento continua em P005.

## Evidência

- Uma foto por envio, na resposta já confirmada. Pode vincular ao item ou à irregularidade confirmada na revisão informada. Preserva a descrição que fundamentou o vínculo.
- No ambiente de demonstração, PNG e JPEG estáticos de até 5 MiB e 20 megapixels são decodificados e validados com Pillow. A extensão de download é derivada do formato detectado.
- O PostgreSQL guarda bytes originais, nome, formato, tamanho, vínculo, autoria e data. A confirmação e a evidência são gravadas na mesma transação. O download valida novamente a equipe e o vínculo com a inspeção e envia o conteúdo como anexo privado.
- A aceitação de documentos, a homologação da câmera e a política de armazenamento e retenção reais continuam em P016/P017/P019. O seletor nativo pode oferecer câmera conforme o navegador.

## Observações gerais e galeria

A revisão visual de 16/11/2026 incorpora a tela de observações gerais do RF-08. Um fiscal ativo da equipe pode registrar até 1.000 caracteres por observação enquanto a inspeção estiver em andamento e sem pedido de cancelamento pendente. Gravação, recibo por chave e evento de auditoria são confirmados juntos. A consulta fica disponível para a equipe após conclusão ou cancelamento. Esses textos ficam associados à inspeção, em registro próprio.

A galeria lista as fotos confirmadas, com miniaturas privadas e referência ao item. A aba Arquivos consulta os documentos do estabelecimento pela autorização de RF017. [Entrega da interface](../entrega-interface-rf08.md)

## Comunicação e estados

A tela informa Pendente, Enviando, Salva ou Falha em texto para resposta e foto. Salva exige confirmação do servidor com a chave da operação e o instante de gravação. A resposta confirmada mantém seu estado se uma foto falhar.

No envio, a página guarda uma cópia temporária do formulário, inclusive o arquivo selecionado. Quando a conexão falha, bloqueia novos envios e links dependentes do servidor. O evento de reconexão e uma sondagem autenticada tentam recuperar o acesso. A sondagem confirma comunicação real antes de reenviar os mesmos dados com a mesma chave. A detecção por navegador é apenas um sinal. Erro de validação ou conflito exige ação do usuário. Uma troca de sessão ou perda de acesso bloqueia a retentativa daquela página.

A fila é limitada a um envio já solicitado e vive na memória da página aberta. Fechar ou recarregar a página perde esse estado temporário. A validação de rede e código ocorre no perfil local de inspeções de demonstração.

[Django 5.2, uploads](https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/) · [Pillow, verificação de imagens](https://pillow.readthedocs.io/en/stable/reference/Image.html) · [MDN, sinal de rede do navegador](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine)
