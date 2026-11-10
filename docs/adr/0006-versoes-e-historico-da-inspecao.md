# ADR 0006: Preservação de versões e histórico da inspeção

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** registro de restrição confirmada; política detalhada e persistência pendentes.
- **Origem:** DC011 a DC016 e DC020 nas [decisões confirmadas](../decisoes-confirmadas.md); F003 no [índice de fontes](../referencias/README.md).

## Contexto

Publicações de checklist e correções autorizadas não podem alterar silenciosamente a base de uma avaliação ou o conteúdo de um termo já emitido. O histórico deve permitir relacionar decisão, mudança e resultado.

## Decisão registrada

Preservar checklist e regras desde o início da inspeção, resultados anteriores e novos quando houver correção, termos emitidos e eventos oficiais. A revisão autorizada mantém justificativa, autoria, decisão e momento, com recálculo pelas regras originais quando afetar a avaliação.

Nova versão ou retificador se relaciona à emissão anterior sem sobrescrevê-la. O PDF usa dados confirmados; sua falha não apaga a inspeção salva. Como detalhamento técnico proposto, coordenar alteração e auditoria oficial no mesmo caso de uso, tratando separadamente os efeitos no armazenamento de arquivos.

## Alternativas e razões

- Recalcular avaliações antigas com a regra atual: muda o fundamento original da avaliação.
- Sobrescrever resultado/termo e conservar só a versão mais recente: impede reconstruir o ato anterior.
- Usar apenas log técnico como histórico oficial: não garante os vínculos e o acesso exigidos para a decisão.
- Adotar event sourcing completo: não é necessário nem foi aprovado para cumprir a preservação exigida.

Essas razões são análise técnica. Não há decisão entre cópia de checklist e referência a versão imutável, nem schema de revisões escolhido.

## Consequências

Há custo adicional de armazenamento, relacionamentos e consulta das versões. As comparações de indicadores precisam considerar regras e checklists compatíveis. Banco e arquivos exigem recuperação coordenada; uma transação do banco não resolve sozinha a preservação física de documentos.

## Pendências e verificação futura

P009 a P013, P016 e P017 tratam do conteúdo, cálculo, política documental, assinatura, arquivos e retenção. Verificar futuramente uma publicação posterior, uma correção autorizada com mudança de resultado, uma nova emissão e falha de PDF. Confirmar preservação e relação entre versões. Nenhuma revisão ou emissão foi implementada nesta etapa.

Relacionados: RF004, RF007, RF013, RF015, RF019 a RF023, RNF05, RNF13 e RS007 no [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md); [arquitetura](../arquitetura.md).
