# Spec 0006 — Início, equipe e supervisão

I05, com RF002 parcial, RF005–RF007 e RS001/RS002. Uma ação pode reunir várias inspeções. O Administrador pode designar simultaneamente fiscais ativos da equipe da ação. A designação é opcional e vigora imediatamente. [Decisões](../decisoes-confirmadas.md) · [Spec 0003](0003-acesso-vinculos-supervisao.md)

## Transições e acesso

| Evento | Ator e condição | Resultado |
|---|---|---|
| Atribuir | Administrador ativo seleciona estabelecimento ativo, fiscal responsável e participantes ativos. Pode selecionar uma ação existente. | Inspeção `ATRIBUIDA`, com autoria e origem administrativa. Sem escolha, cria uma ação. |
| Iniciar atribuída | Fiscal responsável atual, com conta ativa, inicia escolhendo um checklist de demonstração publicado. | Inspeção `EM_ANDAMENTO`, com o ator, instante, identificação do estabelecimento e versão fixados no servidor. |
| Iniciar diretamente | Fiscal ativo escolhe estabelecimento ativo e checklist de demonstração publicado. | Cria ação e inspeção `EM_ANDAMENTO`, com o fiscal como responsável e origem fiscal. |
| Alterar equipe | Administrador ativo informa responsável e demais fiscais. | Mantém o histórico de autoria e versões. Encerra designações de fiscais removidos de todas as inspeções da ação. |
| Designar ou encerrar | Administrador ativo seleciona o conjunto de supervisores elegíveis da ação. | A inclusão abre uma designação. A remoção encerra a designação. Autor e instante são registrados em ambos os casos. |

A equipe elegível da ação reúne responsáveis e participantes atuais das suas inspeções. Fiscal consulta somente as inspeções em que atua. O estado da supervisão é consultado na requisição e requer designação aberta, conta ativa, perfil Fiscalização e vínculo atual à equipe da ação. A designação habilita a identificação do supervisor nesse contexto. A autoridade para aprovar pedidos continua em P005.

O rascunho de checklist fica fora da seleção. O servidor escolhe a última versão de demonstração do checklist selecionado no instante do início. O banco protege a referência, a data, o autor e a identificação do estabelecimento já gravados. As duas rotas de criação distinguem o mesmo pedido repetido de um reaproveitamento do identificador com dados diferentes. O início atribuído é serializado pela inspeção. O acesso de Estabelecimento aos resultados finais continua no seu recorte.

## Persistência e contrato de tela

- `AcaoFiscalizacao` agrupa inspeções por chave protegida. A ação pode ser reutilizada na atribuição administrativa.
- `Inspecao` registra origem, estado, estabelecimento, equipe, criador, início, versão e revisão da equipe. Datas vêm do servidor.
- `HistoricoInspecao` persiste atribuição, início e alterações de equipe na transação do ato. `DesignacaoSupervisor` guarda fiscal, ação, autor e instantes de abertura/encerramento. Uma mesma pessoa tem uma designação aberta por ação. Várias pessoas podem tê-la simultaneamente.
- Páginas de lista, detalhe, criação, equipe e supervisão ficam em `/inspecoes/`. Mutações usam POST com CSRF. Conflitos retornam 409. A UI confirma a operação pela página recuperada após gravação.
- A I05 usa dados fictícios e versões de demonstração no desenvolvimento e nos testes. Conteúdo e publicação oficiais seguem em P009. Retentativa automática e preservação do formulário diante de falha de rede seguem em P020 e I06.

[Plano de implementação](../plano-implementacao.md) · [Django 5.2, bloqueios de linha](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update)
