# I14 — Adiamento e reanálise para a demonstração acadêmica

**Entrega local em 16/11/2026.** A aplicação usa Django e PostgreSQL no computador da apresentação, conforme DC037. DC038 define os dois fluxos desta etapa. [Decisões](decisoes-confirmadas.md#dc037-demonstração-acadêmica-local) · [Preparo local](../README.md#preparo-local)

## Demonstrar o adiamento

1. Como Administrador, atribua uma inspeção fictícia e designe um fiscal elegível como Supervisor da ação. Entre como fiscal da equipe e abra **Adiamento** no detalhe da inspeção Atribuída.
2. Informe a justificativa e a nova data e hora no fuso de Maceió. Enquanto o pedido estiver pendente, a tela de detalhe informa o bloqueio do início.
3. Entre como um Supervisor elegível diferente do solicitante e abra **Pedidos de adiamento**. Confira a proposta, selecione **Aprovar**, informe o motivo e registre. A inspeção segue Atribuída e mostra a data aprovada.
4. Na data agendada, o responsável usa **Iniciar inspeção** e seleciona o checklist pela tela existente. Se a proposta for rejeitada, permanece a data anteriormente vigente. O Administrador só decide na ausência de outro Supervisor elegível. [Spec 0014](specs/0014-adiamento.md)

## Demonstrar a reanálise

1. Depois de concluir uma inspeção fictícia, entre como conta vinculada ao Estabelecimento. Abra **Documentos do estabelecimento**, selecione a inspeção e envie um complemento em PDF, JPEG ou PNG.
2. Entre como fiscal da equipe e abra **Reanálise documental** no detalhe. Selecione o documento, confira o arquivo, informe o parecer e escolha **Manter resultado** ou **Indicar correção**.
3. Ao indicar correção, escolha um item e envie o pedido. O supervisor elegível pode consultar o parecer e baixar o documento no pedido. A correção mantém as condições de aprovação e aplicação da I11.
4. Se a correção alterar o conteúdo de termo já emitido, confira o retificador e faça a liberação separadamente. O termo original liberado continua disponível. [Spec 0015](specs/0015-reanalise-documental.md) · [Correção e retificação](specs/0012-correcao-e-retificacao.md)

## Verificações

- `manage.py check` e `makemigrations --check --dry-run` passaram. A suíte de 120 testes passou no PostgreSQL isolado.
- Os testes cobriram autoridade, alternativa administrativa, bloqueio de início, data, preservação de registros, repetição e consulta privada. Cobriram ainda os dois tipos de parecer, o vínculo com correção e a preservação do termo anterior enquanto o retificador aguarda liberação.
- Chromium a 360 e 820 px percorreu solicitação e decisão do adiamento, recebimento de complemento, parecer e encaminhamento a correção com documento acessível ao supervisor.
- Duas expectativas da I09 foram ajustadas à nova regra de recebimento. O teste continua verificando que a área de documentos não expõe a avaliação e que o recibo original permanece válido.

A validação é local e usou dados fictícios. Os prazos de operação e as políticas aplicáveis a inspeções reais ficam em P007/P008/P011. [Pendências](pendencias.md) · [Trello](https://trello.com/c/KL83kx24)
