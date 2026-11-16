# Spec 0005 — Checklist e versões

Implementação I04 do RF004 no ambiente local. Prepara a referência que a I05 deverá guardar ao iniciar uma inspeção (RF007). O conteúdo sanitário validado e a autoridade para publicação oficial seguem em P009. A fórmula de pontuação segue em P010. [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md) · [ADR 0006](../adr/0006-versoes-e-historico-da-inspecao.md)

## Dados

| Dado | Tipo | Regra do recorte |
|---|---|---|
| Título | Texto | Obrigatório. Remover espaços externos e rejeitar vazio. |
| Referência e regras | Texto | Opcionais no rascunho de demonstração. São copiadas para a versão publicada. |
| Enunciado | Texto | Obrigatório em cada item. |
| Ordem | Inteiro | Positiva e única no mesmo checklist. Pode ter intervalos. |
| Peso | Decimal opcional | Guardado como texto decimal exato quando informado, com até 18 dígitos e 8 casas. O valor não é calculado na I04. |
| Obrigatório | Booleano | Define a configuração do item. A validação da resposta na inspeção pertence à I06/I09. |
| Opções de resposta | Lista ordenada de texto | Uma por linha na edição. Remover linhas vazias e espaços externos. Exigir pelo menos uma opção e rejeitar duplicatas sem distinguir caixa. |
| Referência do item | UUID interno | Gerada ao inserir o item e preservada ao editar. Uma resposta futura deve referenciar a versão e o item. |
| Versão publicada | Inteiro positivo por checklist | Gerado pelo servidor, com conteúdo completo, autor, data e finalidade de demonstração. |

## Gestão e publicação

- Administrador ativo cria um checklist, edita o rascunho e inclui, edita ou remove itens. As alterações são confirmadas pelo servidor e usam uma revisão do rascunho para detectar conflito.
- Para publicar a versão de demonstração, o checklist deve ter pelo menos um item válido. A publicação copia o conteúdo do rascunho para um registro separado. Publicar novamente a mesma revisão retorna a versão já registrada. Salvar o rascunho e publicar são ações distintas.
- A transação bloqueia o rascunho ao editar ou publicar. A restrição do banco garante número e revisão de origem únicos por checklist. Uma proteção no PostgreSQL recusa alterações e exclusões de versões publicadas. A consulta a versões antigas recupera o conteúdo próprio da versão.
- A I05 deverá usar referência protegida à versão publicada e decidir quais versões são elegíveis conforme a finalidade. Uma versão de demonstração destina-se a dados fictícios. Fórmula, regra de N/A, pesos oficiais e política de publicação sanitária permanecem nas decisões P009/P010.

## Rotas e validação

As páginas de gestão ficam em `/gestao/checklists/`. A página de cada checklist permite editar metadados e itens e consultar seu histórico. A seleção de uma versão abre uma página de leitura. Edição, remoção de item e publicação usam POST com CSRF. Contas fora do perfil são recusadas no servidor. Formulário inválido mantém a entrada na resposta. Revisão desatualizada retorna 409. A confirmação de publicação apresenta o número recuperado do banco.

Verificar acesso negativo, opções duplicadas, conflito de ordem, publicação vazia recusada, repetição concorrente, falha de persistência, consulta de versões distintas e tentativa de alterar ou excluir uma versão por acesso direto ao banco. [Documentação do Django sobre bloqueio de linhas](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update) · [Documentação do PostgreSQL sobre gatilhos](https://www.postgresql.org/docs/17/sql-createtrigger.html)
