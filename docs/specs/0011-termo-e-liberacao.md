# Spec 0011 — Termo em PDF e liberação

I10 no ambiente de demonstração. Abrange RF015/RF016, RNF13, RS010 e trilha de emissão e liberação em RF023. [DC034](../decisoes-confirmadas.md#dc034-emissão-e-liberação-do-termo-na-i10) · [Conclusão](0010-pontuacao-e-conclusao.md)

## Autoridade e conteúdo

| Operação | Autorização |
|---|---|
| Solicitar emissão | Fiscal ativo da equipe da inspeção ou Administrador. Exige resultado confirmado. |
| Consultar e baixar antes da liberação | Administrador, fiscais da equipe atual e supervisores ativos da ação. O supervisor de outra inspeção da ação pode revisar o termo emitido. |
| Liberar | Administrador ou supervisor ativo da ação. A autorização é conferida novamente no servidor. Um fiscal sem designação pode emitir pela equipe, conforme a primeira linha. |
| Consultar e baixar no portal | Contas ativas atualmente vinculadas à unidade ativa, após liberação. Lista paginada, detalhe e download passam pela mesma regra de acesso. |

O PDF exibe identificação cadastrada da unidade na inspeção, inspeção e emissão, versão do checklist utilizada, resultado e os itens não conformes com as descrições registradas em campo. Irregularidades registradas em itens com outras respostas também integram a versão. A classificação da opção segue o resultado confirmado. As descrições vêm dos recibos imutáveis das revisões usadas no cálculo. Observações gerais do fiscal, evidências, documentos enviados e decisões internas ficam fora desse conteúdo.

## Emissão, liberação e recuperação

O registro `TermoInspecao` vincula o resultado confirmado, versão do termo, código de demonstração, autor e data, UUID da operação e conteúdo PDF privado. A versão inicial tem código `DEMO-<inspecao>-V01`. O servidor usa ReportLab e guarda os bytes no PostgreSQL. [Diagramador do ReportLab](https://docs.reportlab.com/reportlab/userguide/ch5_platypus/) O título identifica o caráter demonstrativo. Não há vigência ou classificação jurídica atribuída ao arquivo.

Emissão síncrona e registro de auditoria são confirmados em uma transação. O arquivo é armazenado antes de o servidor confirmar a emissão. Falha de geração mantém a inspeção concluída e permite nova tentativa. A liberação grava seu próprio registro com termo, decisor, designação quando aplicável, data e UUID da operação, acompanhada de outro evento de auditoria. A emissão não libera automaticamente o acesso externo. Os registros emitidos e liberados são preservados pelo banco.

Cada comando repete o recibo da mesma operação já confirmada com autorização atual. Duas operações concorrentes não criam duplicata. A interface usa a recuperação de conexão da I06. O portal recebe somente os campos públicos e o arquivo confirmado e liberado. O download retorna `application/pdf` como anexo e com cache privado desabilitado.

## Rotas e validação

| Fluxo | Rotas e métodos |
|---|---|
| Equipe interna | `GET /inspecoes/termos/`, `GET /inspecoes/<id>/termo/` e `GET /inspecoes/<id>/termo/<termo>/pdf/`. |
| Registro | `POST /inspecoes/<id>/termo/emitir/` e `POST /inspecoes/<id>/termo/<termo>/liberar/`, com CSRF, contexto da sessão e UUID. |
| Recuperação | `GET /inspecoes/<id>/termo/conexao/` com contexto da sessão e escopo atual. |
| Estabelecimento | `GET /inspecoes/resultados/`, `GET /inspecoes/resultados/<termo>/` e `GET /inspecoes/resultados/<termo>/pdf/`. |

Verificar termo coerente com a versão original, paginação de descrições longas, falha de geração, concorrência, perda da confirmação e imutabilidade. Conferir publicação separada e acesso com outros vínculos, revogação, endereço direto e supervisor de outra inspeção da ação. Assinatura e ciência ficam em P013. Política oficial de emissão, vigência e retificação fica em P012, com armazenamento de produção em P016.
