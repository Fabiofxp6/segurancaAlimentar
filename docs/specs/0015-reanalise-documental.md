# Spec 0015 — Complementação e reanálise documental

**Escopo confirmado para a I14 local.** Depois da conclusão, a conta ativa do Estabelecimento pode enviar documento próprio. Um fiscal ativo da equipe abre a reanálise e registra parecer. Se o parecer apontar correção, o pedido segue a aprovação, aplicação, pontuação e retificação da I11. O recorte não envolve nova visita. [DC038](../decisoes-confirmadas.md#dc038-adiamento-e-reanálise-na-i14) · [RF028](../prd/0001-sistema-avaliacao-seguranca-alimentar.md#rf028-reanalisar-documentos-após-a-conclusão)

## Contrato local

- A área de documentos recebe complementos com os mesmos formatos, verificação, acesso privado e recuperação da I07. A inspeção concluída própria fica disponível para envio. Na mesma transação do recebimento, o servidor identifica o complemento a partir do estado. O Estabelecimento acompanha o recebimento na área de documentos e consulta resultados apenas nas rotas de liberação da I10.
- O fiscal abre **Reanálise documental** no detalhe da inspeção concluída. Seleciona um complemento desta inspeção e registra parecer textual obrigatório de até 2.000 caracteres e encaminhamento **Manter resultado** ou **Indicar correção**. A demonstração preserva um parecer por documento e associa o resultado vigente na data da análise. Autor, horário e documentos ficam internamente rastreáveis.
- Um parecer que indique correção oferece os itens da revisão examinada. A solicitação na tela da I11 leva o vínculo com a reanálise e valida no servidor se o documento, a base e a inspeção correspondem. Se a base tiver mudado, a interface impede a vinculação a uma revisão diferente. Pedidos, decisões, revisões e termos anteriores permanecem consultáveis.
- A tela de reanálise, o parecer e a correção continuam internos. Fiscal de outra equipe e cliente não consultam pareceres. Administrador pode conferir os pareceres. O supervisor que recebe uma correção de outra inspeção da ação pode conferir o parecer e baixar o documento pelo próprio pedido, enquanto autorizado.
- POST de parecer exige sessão, CSRF e contexto da tela. A operação é confirmada após gravação atômica e repete a confirmação se a mesma chave e os mesmos dados forem reenviados. Um parecer ou documento sozinho não altera estado, nota, resultado nem PDF.

## Aceite

Verificar complemento posterior à conclusão, escopo da unidade e da equipe, recebimento e parecer sem efeito oficial imediato, controle de duplicação, vínculo com correção e manutenção do termo anterior. Validar que uma correção ligada ao parecer ainda passa pelas permissões, pela revisão original e por nova liberação do retificador da I11.
