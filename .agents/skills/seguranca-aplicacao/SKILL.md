---
name: seguranca-aplicacao
description: Especificar ou revisar autorização, sessão, entradas, arquivos e proteção de dados do sistema alimentar no recorte solicitado. Use em controles sensíveis; não aprova políticas legais, MFA, criptografia ou acesso ainda pendentes.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Segurança da aplicação

Consultar os RF/RS pertinentes no [PRD](../../../docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md), [arquitetura](../../../docs/arquitetura.md), [decisões](../../../docs/decisoes-confirmadas.md) e [pendências](../../../docs/pendencias.md). Delimitar ator, recurso, entrada e efeito. Usar a [fundação](../../../docs/specs/0001-fundacao-tecnica.md) para ambientes/segredos, a [autenticação](../../../docs/specs/0002-autenticacao.md) para credenciais/sessão e o [acesso](../../../docs/specs/0003-acesso-vinculos-supervisao.md) para vínculos/designações. Não executar varredura externa como efeito de revisão documental.

## Autorização e revogação

- Conferir identidade ativa, perfil, vínculo, contexto e estado em consultas, alterações e downloads, no servidor. Validar formato de ID ou esconder botão não prova autorização.
- Supervisor é fiscal designado por ação; não recebe poder global nem aprovação automática. Administrador de negócio, `is_staff`, superusuário técnico e participação na equipe são conceitos distintos. P002–P006 mantêm representação e autoridades abertas, inclusive autoaprovação.
- O service do ato verifica o escopo na efetivação. Revalidar vínculo/designação revogados na sessão atual; não confiar em concessões copiadas no login ou cache sem invalidação. Não prometer desfazer uma requisição já efetivada.
- Filtrar também busca, contagem, exportação, versão e URL direta. Estabelecimento acessa somente seus envios e resultados/documentos finais liberados; conclusão não publica automaticamente nem libera avaliação interna. Novo anexo não altera nota.
- Aplicar a resposta de negativa da Spec 0003 sem revelar recurso fora do conjunto acessível. Falha de consulta não abre acesso; política ainda indefinida não gera concessão por inferência. Não inventar autoridade substituta ou acesso de emergência.

## Credenciais, sessão e transporte

- Manter senha, sessão, CSRF e escape pelos mecanismos do Django. Não criar autenticação paralela, hash próprio, JWT ou colunas extras de senha/sessão para imitar dados lógicos da fonte.
- Preservar os caracteres da senha conforme Spec 0002, não repopulá-la no HTML de resposta e manter mensagem pública genérica para usuário inexistente, senha incorreta e conta inativa. Indisponibilidade operacional não é senha errada.
- Login/logout propostos usam POST com CSRF. Validar `next` no servidor também no POST, incluindo host/esquema e fallback interno; destino aceito não concede permissão ao recurso. Seguir o contrato da spec, sem copiar links externos recebidos.
- Verificar encerramento no servidor e recusa da chave anterior, não só remoção do cookie. A sessão Django é confirmada; backend em banco do ADR 0008 permanece recomendado. Prazo, tentativas, recuperação, concorrência, MFA/SSO e revogação global continuam em P014/P015.
- Transporte nativo necessário de token CSRF no form/cookie e identificador de sessão no cookie é admitido. Isso não autoriza exibição em mensagens, URLs, dumps ou logs. Não desativar CSRF para satisfazer uma regra genérica de ocultação de tokens.
- Cookies, HTTPS/proxy e cache seguem implantação e políticas validadas; um cabeçalho não garante apagar conteúdo de outra aba. Não declarar isolamento ou limpeza de aparelho compartilhado sem política/verificação.

## Arquivos, confirmação e histórico

Revisar formato/tamanho/conteúdo no servidor e o acesso a cada arquivo/versão. Distinguir documento do estabelecimento, evidência fiscal e termo emitido. Não confiar só no nome/MIME recebido nem no conhecimento do endereço; tecnologia/limites/entrega privada continuam em P011/P012/P016.

Preservar autorização, justificativa, conteúdo exato aprovado e história de correção/cancelamento. Resultado, checklist original e termo anterior permanecem rastreáveis. Auditoria oficial e log técnico têm funções distintas; `atomic` ou uma mensagem de log não comprovam tudo isso.

Preservar preenchimento da página aberta na perda de comunicação e só confirmar após servidor. Armazenamento persistente no navegador não está aprovado. Para resposta perdida de login, consultar a proposta específica de reconciliação em P014/P020 na Spec 0002; não derivar uma política de reenvio de senha da retentativa geral de inspeções. Limpeza ao sair/expirar/trocar conta segue a decisão aplicável, sem presumir salvar ou descartar dados de outra tela.

## Evidência e limites da revisão

Manter ambientes/segredos separados e não incluir corpo sensível, senha, hash, cookie, token ou configuração secreta em registros. Acesso/retenção de logs e auditoria, proteção em repouso e política legal dependem de P015/P017; não declarar conformidade ou certificação a partir desta lista.

Usar AU/AC e as validações da [matriz](../../../docs/matriz-rastreabilidade.md) que correspondam ao recorte. Em implementação autorizada, verificar acesso direto negativo, revogação, middleware e concorrência com evidência; em documentação, registrar conferência documental sem alegar teste da aplicação. Separar fato, hipótese e decisão aberta, sem nota artificial ou vulnerabilidade inventada. Avaliação de ameaças completa só entra quando solicitada.

Atualizar o [Trello](../../../docs/acompanhamento-trello.md) e relatar controles/políticas ainda pendentes. Origem: [curadoria](../../../docs/curadoria-skills-agentes.md). Revisão integrada: [Etapa 7](../../../docs/revisao-skills-tecnicas.md).
