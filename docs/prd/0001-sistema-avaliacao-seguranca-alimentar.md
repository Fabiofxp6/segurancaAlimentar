# PRD 0001 Sistema de Avaliação de Segurança Alimentar

- **Status:** Proposto, para revisão do responsável pelo projeto.
- **Data:** 10/11/2026.
- **Etapa de origem:** 2. Revisão de detalhamento solicitada em 10/11/2026, após a Etapa 4 e a curadoria de skills/agentes.
- **Fontes:** [índice de referências](../referencias/README.md), [catálogo revisado F003](../referencias/catalogo-requisitos-origem.md) e [decisões confirmadas](../decisoes-confirmadas.md).
- **Pendências:** [registro P001 a P022](../pendencias.md).
- **Arquitetura:** [proposta de detalhamento e índice dos ADRs](../arquitetura.md), elaborados na Etapa 3; escolhas anteriores e recomendações novas estão distinguidas.
- **Especificações:** [Spec 0001 de fundação técnica](../specs/0001-fundacao-tecnica.md), Proposta na Etapa 4, e [Spec 0002 de autenticação](../specs/0002-autenticacao.md), Proposta na Etapa 5. A [Spec 0003 de acesso](../specs/0003-acesso-vinculos-supervisao.md) e a [matriz completa](../matriz-rastreabilidade.md) foram elaboradas na Etapa 6, também Propostas. O roteiro das demais áreas está ao final deste documento.

## Objetivo

Apoiar a avaliação de segurança alimentar dos estabelecimentos, organizando o trabalho dos fiscais, as respostas do checklist, as evidências, o resultado e os termos emitidos. A inspeção deve poder ser consultada e revisada com identificação dos responsáveis e preservação do histórico.

O sistema será acessado por navegador em tablets e celulares, com registro oficial no servidor e operação somente online. O estabelecimento poderá fornecer documentos e consultar o resultado final disponibilizado de suas inspeções.

## Perfis de uso

| Perfil ou função | Atuação no produto | Limite principal |
|---|---|---|
| Fiscalização | Inicia ou executa inspeções, preenche o checklist e registra evidências; solicita cancelamentos e alterações sujeitos a autorização | Não recebe poder automático de supervisão ou de aprovação da própria solicitação |
| Administrador | Gerencia usuários, estabelecimentos, checklists e atribuições, conforme as permissões do processo | Poder de designar supervisor ou aprovar atos não é presumido; depende de P004 e P005 |
| Estabelecimento | Envia documentos próprios e consulta seus envios e resultados finais liberados | Não acessa dados de terceiros, avaliações parciais ou deliberações internas |
| Supervisor da ação | Fiscal designado para a supervisão em uma ação específica | Função adicional ao perfil Fiscalização; sua designação não concede poder em outra ação |

Existem três perfis-base. Supervisor não é um quarto perfil nem um cargo permanente. Cliente significa estabelecimento avaliado. A relação entre ação de fiscalização e inspeção e a política de designação continuam pendentes em P003 e P004.

## Restrições técnicas confirmadas

O projeto usará Python com Django e PostgreSQL, em sistema web com hospedagem remota ou em nuvem. Estão confirmados MVT, páginas com Django Templates e views baseadas diretamente em `View`; regras e consultas explícitas da aplicação ficam em services, separados da camada HTTP. A base de autenticação será um usuário customizado a partir de `AbstractUser`, com nome de usuário, senha e sessão Django.

Essas escolhas seguem DC003 a DC007. Versões, provedor, armazenamento e biblioteca de PDF continuam pendentes. A arquitetura e as specs detalharão as fronteiras e os contratos nas etapas próprias.

## Fluxo do produto

A inspeção pode nascer de atribuição administrativa ou início direto pelo fiscal. Ao iniciar, preserva o checklist e as regras aplicáveis. Durante o preenchimento, respostas e evidências só integram o registro oficial depois da confirmação do servidor.

A conclusão, a geração do termo e a liberação do resultado ao estabelecimento são operações distintas; o momento e as condições de liberação dependem de P012. Um pedido de cancelamento não cancela a inspeção enquanto aguarda decisão. Uma correção posterior à conclusão exige autorização e gera histórico, recálculo quando afetar a avaliação e nova emissão documental quando necessária.

Esta descrição estabelece o comportamento geral; não define uma lista definitiva de estados de implementação. Adiamento, reanálise, bloqueio durante análise e retomada seguem as pendências correspondentes.

## Escopo e leitura dos requisitos

O escopo do produto inclui cadastros, acesso, checklists versionados, inspeções, evidências, cálculo, documentos, histórico, autorizações e indicadores. A presença de uma função aqui não determina sua prioridade ou inclusão automática na primeira versão de software; essa composição depende de P022.

Os IDs RF001 a RF028, RNF01 a RNF14 e RS001 a RS016 foram preservados, totalizando 58 entradas. O texto apresenta o comportamento de produto de F003 e incorpora as confirmações posteriores registradas em F008 e nas decisões confirmadas. Este PRD preserva os dados, tipos e formatos apresentados em F003 para permitir a leitura completa dos requisitos. São referências e sugestões da fonte: não definem por si só schema, chave primária, coluna, mecanismo de arquivo ou contrato técnico aprovado. As specs detalharão e validarão a implementação.

Cada aceite descrito é uma verificação futura, não um teste executado. Quando há detalhamento pendente, o comportamento central está registrado, mas a política indicada precisa ser resolvida para completar sua especificação ou aceite. RF027 tem fluxo a validar e RF028 permanece proposta. O status global Proposto não desfaz decisões já confirmadas nem aprova as propostas remanescentes.

As prioridades permanecem **A validar**, conforme P022. Metas, limites e prazos numéricos não aprovados continuam abertos.

## Como interpretar os dados e o detalhamento

A revisão recupera as 183 entradas de dados dos 28 RF, além dos parâmetros dos RNF e RS, e explicita atores, condições, fluxo, regras, manutenção e aceite. Os nomes compostos, como `inicio/fim`, mantêm a notação da fonte; não significam que deva existir uma coluna com esse nome.

| Tipo ou notação de referência | Significado na fonte e limite de interpretação |
|---|---|
| `str` | Texto; tamanho e máscara específica dependem da regra validada |
| `bool` | Informação Sim/Não; pode ser condição verificada pelo sistema, sem ser campo editável |
| `int` | Contagem, ordem, revisão ou outro inteiro; não define tamanho de coluna ou valor padrão |
| `Decimal` | Valor decimal; precisão, pesos e arredondamento continuam pendentes quando não aprovados |
| `UUID` | Identificador sugerido e sem máscara visual; não aprova UUID como chave física, conforme P002 |
| `datetime` | Data/hora com fuso; F003 usa `dd/MM/yyyy HH:mm` como referência de exibição |
| `date` | Data civil; F003 usa `dd/MM/yyyy` como referência, sem definir fuso de apresentação |
| `Enum` | Conjunto de opções; opções de item vêm do checklist. A notação não decide enum físico ou armazenamento |
| `list[...]` e `dict[...]` | Coleção ou estrutura de informação; não determina coluna array/JSON nem dispensa validar conteúdo |
| `UploadedFile` | Arquivo recebido para validação; não é decisão de armazenar o binário em uma coluna de negócio |

Datas de autoria/decisão/recebimento vêm do servidor; datas propostas de reagendamento são informação distinta e dependem do fluxo a validar. Autor, perfil e autoridade não são aceitos como verdade apenas porque chegaram na requisição. O mecanismo de identificação da operação para retentativa permanece em P020.

Obrigatoriedade deve ser lida por operação e por momento: dados de aprovação não precisam existir quando o pedido ainda está pendente. Em RF008, inspeção, item e resposta estão expressamente definidos como obrigatórios; observação, irregularidade e evidência seguem o checklist. Nos demais casos, não se presume que todos os dados da tabela sejam entradas obrigatórias ou editáveis. Campos definidos como obrigatórios rejeitam vazio ou somente espaços.

Não foram completados por suposição limites de texto/arquivo, máscara de documento, fórmula, precisão, valor padrão, autoridade ou prazo. Os formatos transcritos mantêm o nível de referência da fonte; homologação da interface e escolhas físicas continuam nas pendências pertinentes. Os fluxos detalham o comportamento descrito pelas fontes e decisões, e os cenários são futuros; nenhuma verificação da aplicação foi executada. Quantidades de pessoas e nomes ilustrativos nos cenários da fonte são dados de teste, não limites do produto.

## Situação oficial, pedido e envio

| Dimensão | Referência de comportamento | Limite |
|---|---|---|
| Inspeção | Atribuição, início/andamento, conclusão e cancelamento | Nomenclatura técnica e transições finais ainda a detalhar; cancelamento exige decisão válida |
| Pedido de autorização | Pendente, Aprovada e Rejeitada | Pedido não produz o efeito oficial por si só; aplicar somente o escopo autorizado |
| Envio na página | Pendente, Enviando, Salva e Falha | Salva exige confirmação; resposta e arquivo podem ter situações diferentes |

Adiamento e reanálise permanecem a validar. Uma correção autorizada conserva a avaliação anterior e não reabre automaticamente a inspeção para edição livre. Conclusão, geração de termo e liberação do resultado são operações distintas.

## Requisitos funcionais

Prioridade de cada RF: **A validar**, conforme P022. Os tipos e formatos das tabelas têm a natureza de referência explicada acima.

### Acesso e cadastros

#### RF001 Autenticar usuário e encerrar sessão

Permitir que um usuário ativo entre com nome de usuário e senha e encerre sua sessão. Credenciais inválidas devem produzir mensagem que não revele se o usuário existe.

**Participantes:** Todos os perfis-base; o servidor verifica a identidade e mantém a sessão.

**Condições de uso e preenchimento:** Para entrar, informar nome de usuário e senha; a conta precisa estar ativa. Para sair, usar a sessão correspondente. usuarioId e ativo são dados verificados no servidor, não permissões concedidas pela entrada do usuário.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `login` | str |
| `senha` | str |
| `usuarioId` | UUID |
| `ativo` | bool; (Sim ou Não) |

**Fluxo principal:**

1. O usuário informa suas credenciais e solicita acesso.
2. O servidor verifica a conta e as credenciais e, quando válidas, estabelece a sessão Django.
3. Ao solicitar saída, o servidor encerra a sessão; o próximo acesso protegido exige autenticação.

**Regras e validações da fonte:**

1. Credencial inválida produz mensagem genérica; logout invalida sessão.

**Alteração, exclusão e consulta:**

- Alteração: Não se aplica como cadastro. O sistema atualiza o estado ou o resultado conforme as regras desta operação.
- Exclusão: Não se aplica como ação de exclusão neste requisito.
- Consulta: O estado ou resultado é exibido na tela correspondente ao usuário autorizado.

**Critérios de aceite:**

1. Credenciais válidas de conta ativa permitem iniciar uma sessão e acessar somente os recursos autorizados.
2. Credencial inválida ou conta inativa não inicia sessão; a mensagem não identifica isoladamente se o nome ou a senha estava errado.
3. Depois de sair, repetir uma solicitação com a sessão encerrada não permite acesso protegido.

**Relações e decisões pendentes:** RF002, RS001, RS003 e RS004; P002 e P014.

#### RF002 Gerir usuários e designar supervisor por ação

Permitir a gestão autorizada de usuários e dos três perfis-base e o registro da designação de um fiscal como supervisor de uma ação. Manter autoria, escopo e histórico das designações, substituições e encerramentos.

**Participantes:** Administrador na manutenção de usuários; pessoa autorizada pela política de designação, ainda a definir, para atribuir supervisão.

**Condições de uso e preenchimento:** É necessário acesso à gestão de usuários. Fiscal, ação/inspeção e designação devem ser identificáveis; elegibilidade, quantidade e vigência dependem da política a validar em P004. Não presumir que todos os dados sejam editáveis ou já conhecidos na abertura.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `usuarioId` | UUID |
| `nome` | str |
| `identificadorAcesso` | str |
| `perfil` | Enum (Fiscalização, Administrador, Estabelecimento) |
| `fiscalSupervisorId` | UUID |
| `inspecaoId` | UUID |
| `acaoFiscalizacaoId` | UUID, se houver agrupamento de inspeções |
| `designacaoId` | UUID |
| `designadoPor` | UUID |
| `inicio/fim` | datetime |
| `ativa` | bool |

**Fluxo principal:**

1. O usuário autorizado mantém o cadastro e o perfil-base, sem criar um quarto perfil Supervisor.
2. Na ação pertinente, registra-se o fiscal designado e o escopo/momento da designação conforme a política que será validada.
3. Substituição ou encerramento conserva a designação anterior, a autoria e o histórico, retirando seus efeitos para novos atos fora da validade.

**Regras e validações da fonte:**

1. O supervisor continua com o perfil Fiscalização. A designação não cria um quarto perfil nem uma condição permanente para todas as inspeções.
2. A função vale somente no escopo registrado. O mesmo grupo de fiscais pode ter supervisores diferentes em ações distintas.
3. O sistema deve identificar o fiscal designado, o responsável pela designação, a ação abrangida e o período ou situação de validade. Um campo global supervisor: bool não representa essa regra sozinho.
4. Designar supervisor para uma ação não concede poder de aprovação sobre outra ação. O fiscal mantém as atividades de fiscalização que já possui.
5. Quem designa ou substitui o supervisor, quantos podem atuar por ação e como tratar ausência ou autoaprovação ainda precisam ser definidos.
6. UUID não possui máscara. Datas e horas são preenchidas pelo servidor, com fuso, e exibidas em dd/MM/yyyy HH:mm. Limites de texto e arquivos ainda serão definidos.

**Alteração, exclusão e consulta:**

- Alteração: Registrar troca ou encerramento da designação com responsável, data e histórico. A designação anterior deixa de autorizar novas decisões fora de sua validade.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: Usuários autorizados consultam a equipe e o supervisor da ação; o estabelecimento não recebe acesso à gestão de usuários.

**Critérios de aceite:**

1. O cadastro distingue Fiscalização, Administrador e Estabelecimento; participar da equipe não concede supervisão.
2. Fiscal designado na ação A não aprova ato da ação B apenas por possuir essa designação.
3. Trocar ou encerrar a designação mantém seu histórico e impede novo ato baseado na autorização antiga fora de sua validade.

**Cenário de referência de F003:** Designar o fiscal A para a ação 1 e o fiscal B para a ação 2. Confirmar que A não aprova atos da ação 2 e que a troca de supervisor preserva a designação anterior.

**Relações e decisões pendentes:** RF005, RF018, RF022 e RS002; P002 a P005.

#### RF003 Gerir estabelecimentos

Permitir ao usuário autorizado cadastrar, consultar, atualizar e inativar estabelecimentos, preservando suas relações com inspeções existentes. Validar dados obrigatórios sem perder zeros à esquerda em documentos de identificação.

**Participantes:** Administrador ou outro usuário efetivamente autorizado à manutenção de estabelecimentos.

**Condições de uso e preenchimento:** Validar os campos definidos como obrigatórios e o acesso ao cadastro. O tipo de documento, sua máscara, tamanho, unicidade e regras de contato ainda não estão fechados.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `nome` | str |
| `documento` | str |
| `endereco` | str |
| `contato` | str |
| `ativo` | bool; (Sim ou Não) |

**Fluxo principal:**

1. O usuário consulta ou abre o cadastro do estabelecimento e informa seus dados.
2. O sistema valida preenchimento e acesso antes de confirmar a manutenção.
3. Uma atualização ou inativação preserva o vínculo com as inspeções já registradas e seu histórico.

**Regras e validações da fonte:**

1. Campos definidos como obrigatórios rejeitam vazio; documento não perde zeros à esquerda.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Campo obrigatório vazio ou somente com espaços é rejeitado; documento textual conserva zeros à esquerda.
2. Atualização ou inativação não elimina a inspeção nem altera silenciosamente a identificação histórica necessária.
3. Usuário sem acesso à manutenção ou ao estabelecimento não obtém os dados nem efetiva a alteração.

**Relações e decisões pendentes:** RF005, RF006, RF016, RS001 e RS009; P002.

#### RF004 Gerir checklist regras e versões

Permitir ao usuário autorizado manter os itens do checklist, opções de resposta, pesos, obrigatoriedade, regras e versões. Uma versão utilizada em inspeção não pode ser sobrescrita de forma a alterar essa avaliação.

**Participantes:** Usuário autorizado à manutenção do checklist; responsabilidade de publicação depende da governança de P009.

**Condições de uso e preenchimento:** Itens, respostas, pesos e obrigatoriedade precisam corresponder à regra sanitária validada. Não estão aprovados limites, soma de pesos, fórmula ou formato técnico da versão.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `titulo` | str |
| `versao` | str |
| `enunciado` | str |
| `ordem` | int |
| `peso` | Decimal |
| `obrigatorio` | bool; (Sim ou Não) |
| `publicadoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |

**Fluxo principal:**

1. O responsável prepara o checklist e seus itens, opções, ordem, pesos e regras.
2. A manutenção/publicação identifica uma versão e seu conteúdo conforme a governança aprovada.
3. Mudança posterior gera conteúdo versionado sem sobrescrever o que já fundamentou uma inspeção.

**Regras e validações da fonte:**

1. Versão usada não é sobrescrita; pesos e opções devem ser coerentes com regra aprovada.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Uma versão usada em inspeção permanece recuperável e com o mesmo conteúdo depois da publicação de outra.
2. Itens, opções e pesos incompatíveis com as regras validadas não são aceitos como uma avaliação válida.
3. Manutenção não autorizada ou tentativa de alterar retroativamente versão utilizada é impedida.

**Relações e decisões pendentes:** RF007, RF008, RF013, RF020 e RNF05; P009 e P010.

### Execução da inspeção e envio

#### RF005 Atribuir inspeção e equipe de fiscalização

Permitir ao administrador atribuir inspeção a fiscal e registrar os participantes da ação, com estabelecimento, origem e momento da atribuição identificáveis. Participar da equipe não concede supervisão.

**Participantes:** Administrador atribui; fiscais participantes consultam e executam conforme seu acesso.

**Condições de uso e preenchimento:** Estabelecimento e fiscais referenciados precisam existir. Registrar os participantes não substitui a designação específica de supervisor; sua obrigatoriedade antes de iniciar continua aberta.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `inspecaoId` | UUID |
| `estabelecimentoId` | UUID |
| `fiscalResponsavelId` | UUID |
| `participantesIds` | list[UUID] |
| `designacaoSupervisorId` | UUID, quando definida |
| `origem` | Enum |
| `atribuidaEm` | datetime |

**Fluxo principal:**

1. O administrador seleciona o estabelecimento, o fiscal responsável e os participantes.
2. O sistema valida as referências e registra a origem administrativa e o momento da atribuição.
3. A equipe acessa a inspeção conforme seus vínculos; mudanças posteriores preservam a autoria dos registros existentes.

**Regras e validações da fonte:**

1. Validar a existência do estabelecimento e dos fiscais vinculados. Registrar a origem administrativa da atribuição.
2. A ação pode reunir mais de um fiscal. Participar da equipe não concede automaticamente a função de supervisor.
3. A supervisão deve usar a designação específica de RF002. Sua obrigatoriedade antes do início e quem a cadastra ainda serão definidos.
4. UUID não possui máscara. Datas e horas são preenchidas pelo servidor, com fuso, e exibidas em dd/MM/yyyy HH:mm. Limites de texto e arquivos ainda serão definidos.

**Alteração, exclusão e consulta:**

- Alteração: Mudanças de equipe e de supervisão preservam quem realizou os registros anteriores e não transferem a autoria.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: Administrador consulta atribuições; fiscais consultam as ações para as quais possuem acesso.

**Critérios de aceite:**

1. Atribuição válida identifica estabelecimento, responsável, participantes e origem sem conceder supervisão a toda a equipe.
2. Referência inexistente ou atribuição não autorizada é rejeitada sem vínculo parcial inconsistente.
3. Troca de equipe ou supervisor não transfere a autoria do que outro fiscal registrou.

**Cenário de referência de F003:** Atribuir uma inspeção com três fiscais e um supervisor designado. Conferir os vínculos sem tornar todos os participantes supervisores.

**Relações e decisões pendentes:** RF002, RF006, RF007 e RS001/RS002; P003 e P004.

#### RF006 Iniciar inspeção pelo fiscal

Permitir que o fiscal selecione o estabelecimento e inicie a inspeção sem atribuição prévia. Identificar o fiscal responsável, a origem e o início confirmado pelo servidor.

**Participantes:** Fiscalização.

**Condições de uso e preenchimento:** Fiscal autenticado e estabelecimento identificado. Autoria vem da sessão; participação e eventual supervisão precisam permanecer distinguíveis.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `estabelecimentoId` | UUID |
| `fiscalId` | UUID |
| `iniciadaEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `origem` | Enum; (opções predefinidas) |

**Fluxo principal:**

1. O fiscal seleciona o estabelecimento e solicita iniciar uma inspeção sem atribuição prévia.
2. O servidor identifica o fiscal, registra a origem do início e vincula a base de checklist/regras conforme RF007.
3. Após a confirmação, a inspeção fica disponível ao preenchimento autorizado, sem transformar seu iniciador automaticamente em supervisor.

**Regras e validações da fonte:**

1. Origem FISCAL; autoria derivada da sessão; início somente confirmado pelo servidor.
2. Registrar os participantes da ação e sua designação de supervisão quando houver. Iniciar a inspeção por iniciativa do fiscal não o torna automaticamente supervisor nem aprovador de seus próprios pedidos. A forma de designar supervisor nesse caso ainda será definida.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Fiscal inicia diretamente sem exigir atribuição administrativa anterior; o histórico distingue as duas origens.
2. Sem confirmação do servidor, a tela não informa início oficial concluído.
3. A iniciativa do fiscal não lhe concede designação de supervisor ou autorização para aprovar seu próprio pedido.

**Relações e decisões pendentes:** RF002, RF005, RF007 e RF010; P004 e P005.

#### RF007 Congelar checklist no início

Vincular a inspeção à versão de checklist e regras utilizada em seu início e preservar essa referência nas avaliações, consultas e correções posteriores.

**Participantes:** Sistema no início da inspeção; fiscal consulta a base vinculada.

**Condições de uso e preenchimento:** A inspeção e a versão aplicável de checklist/regras devem ser identificadas e válidas. A seleção/publicação da versão aplicável depende de P009.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `inspecaoId` | UUID |
| `versaoChecklistId` | UUID |
| `versaoRegraId` | UUID |
| `vinculadaEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |

**Fluxo principal:**

1. No início, o sistema identifica a versão de checklist e de regras aplicável à inspeção.
2. Registra e preserva o vínculo e seu momento, mantendo disponível o conteúdo que fundamenta a avaliação.
3. Preenchimento, consultas e recálculos posteriores utilizam essa base original.

**Regras e validações da fonte:**

1. Nova publicação não altera inspeção iniciada; referências a versões devem existir.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Publicar checklist novo não troca itens, pesos ou regras da inspeção já iniciada.
2. Versão inexistente ou item incompatível não pode ser usado como base da avaliação.
3. Correção posterior continua vinculada às regras originais, sem adotar automaticamente a versão mais recente.

**Relações e decisões pendentes:** RF004, RF008, RF013, RF020 e RNF05; P009 e P010.

#### RF008 Registrar respostas e evidências

Permitir ao fiscal responder os itens, informar observações e registrar irregularidades da inspeção. As exigências de preenchimento seguem o checklist vinculado; a resposta só é apresentada como salva após confirmação do servidor.

**Participantes:** Fiscalização.

**Condições de uso e preenchimento:** Inspeção em preenchimento autorizado e item pertencente à versão vinculada. Inspeção, item e resposta são obrigatórios; observação, irregularidade e evidências seguem a obrigatoriedade do checklist, ainda a validar em P009.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `inspecaoId` | UUID |
| `itemVersaoId` | UUID |
| `resposta` | Enum; (opções predefinidas) |
| `observacao` | str |
| `haIrregularidade` | bool; (Sim ou Não) |
| `descricaoIrregularidade` | str |
| `operacaoId` | UUID |

**Fluxo principal:**

1. O fiscal abre um item e vê seu enunciado e opções da versão correta.
2. Seleciona a resposta, informa observação e irregularidade quando aplicáveis e solicita salvar; evidências seguem RF009.
3. O servidor valida ator, referências, estado e preenchimento e confirma o registro. Durante o envio, a tela informa a pendência.
4. Sem confirmação, o conteúdo continua pendente e preservado na página; ao reconectar, tenta-se confirmar sem duplicação.

**Regras e validações da fonte:**

1. Obrigatoriedade vem da versão; evidência é tratada em RF009; pendência não é salva; edição após conclusão usa RF018 e RF019.
2. Inspeção, item e resposta são obrigatórios. A observação, a irregularidade e as fotos seguem a regra do checklist.
3. O fiscal abre o item, seleciona a resposta, informa os dados necessários e salva. A tela só confirma o salvamento depois do retorno do servidor.
4. Se a conexão cair, manter o preenchimento na tela e tentar enviar após a reconexão, sem duplicar a resposta.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Resposta válida fica associada ao item e à inspeção corretos, com dados requeridos pelo checklist.
2. Item de outra versão, opção não permitida ou falta de dado obrigatório é rejeitado sem parecer salvo.
3. Interrupção da resposta do servidor conserva o preenchimento e não produz duas respostas oficiais na retentativa.
4. Depois da conclusão, uma alteração oficial segue RF018/RF019, sem edição livre pelo formulário de preenchimento.

**Relações e decisões pendentes:** RF007, RF009 a RF012, RF018, RF019, RS009 e RS013; P009, P020 e P021.

#### RF009 Anexar fotos e evidências

Permitir ao fiscal anexar fotos e documentos comprobatórios vinculados aos itens avaliados ou às irregularidades da inspeção. Distinguir sua autoria e origem dos documentos enviados pelo estabelecimento.

**Participantes:** Fiscalização; o servidor valida e vincula a evidência.

**Condições de uso e preenchimento:** Fiscal com acesso à inspeção e vínculo do anexo com item/irregularidade pertinente. Formatos, quantidade, limites e representação da associação serão detalhados em P016.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `evidenciaId` | UUID |
| `inspecaoId` | UUID |
| `itemId` | UUID |
| `nome` | str |
| `mime` | str |
| `tamanho` | int |
| `chaveArquivo` | str |
| `recebidoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `conteudo` | UploadedFile |

**Fluxo principal:**

1. O fiscal captura uma foto ou seleciona arquivo e identifica seu vínculo na inspeção.
2. O servidor valida o arquivo e registra conteúdo, metadados, origem e autoria conforme a estratégia escolhida.
3. A tela mostra recebido somente após confirmação; falha permanece identificável para retentativa sem duplicação.

**Regras e validações da fonte:**

1. Rejeitar tipo/tamanho inválido; erro de upload não vira Salvo; retentativa não duplica arquivo.
2. Os anexos enviados pelo estabelecimento seguem RF017. A origem e a autoria devem distinguir documentação do cliente de evidência registrada pela fiscalização; um envio do cliente não preenche automaticamente uma resposta do checklist.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Arquivo permitido e confirmado pertence à inspeção e à avaliação correta, com origem fiscal identificável.
2. Tipo ou tamanho inválido e erro de envio não produzem evidência apresentada como salva.
3. Retentativa do mesmo envio não cria outro arquivo oficial; documento do estabelecimento continua distinto da evidência fiscal.

**Relações e decisões pendentes:** RF008, RF011, RF012, RF017, RS008, RS010 e RS013; P016.

#### RF010 Operar exclusivamente online

Exigir comunicação e confirmação do servidor para as operações oficiais da inspeção. Dados ainda não confirmados não integram o registro oficial nem podem fundamentar documento emitido como se estivessem salvos.

**Participantes:** Sistema em todas as operações oficiais; todos os usuários recebem a situação real.

**Condições de uso e preenchimento:** Uma operação depende da comunicação com o servidor. Presença de rede no aparelho não é comprovação de que o servidor recebeu ou confirmou o dado.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `conectado` | bool; (Sim ou Não) |
| `operacaoId` | UUID |
| `confirmadoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |

**Fluxo principal:**

1. A interface solicita a operação ao servidor e a apresenta como não confirmada enquanto aguarda retorno.
2. O registro oficial e sua confirmação dependem da validação no servidor.
3. Se não houver comunicação, aplicar RF011/RF012, sem conclusão offline ou documento baseado em dados pendentes.

**Regras e validações da fonte:**

1. Sem servidor não há registro oficial; PDF depende de dados confirmados.

**Alteração, exclusão e consulta:**

- Alteração: Não se aplica como cadastro. O sistema atualiza o estado ou o resultado conforme as regras desta operação.
- Exclusão: Não se aplica como ação de exclusão neste requisito.
- Consulta: O estado ou resultado é exibido na tela correspondente ao usuário autorizado.

**Critérios de aceite:**

1. Sem servidor, a interface não confirma gravação, conclusão ou emissão oficial.
2. PDF e resultado oficial não incluem entrada ainda não confirmada como se estivesse salva.
3. Preservar preenchimento na tela não habilita uma inspeção completa offline.

**Relações e decisões pendentes:** RF011, RF012, RF014, RF015 e RNF14; P020 para detalhamento do reenvio.

#### RF011 Tratar perda de conexão

Ao perder a comunicação, bloquear temporariamente as ações dependentes do servidor, preservar o preenchimento atual na tela aberta e informar a pendência. Tentar o envio novamente quando a conexão retornar.

**Participantes:** Sistema e usuário que está preenchendo a página.

**Condições de uso e preenchimento:** Interrupção ou falha de comunicação antes ou durante uma operação. A página atual pode conter entrada ainda não confirmada.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `conectado` | bool; (Sim ou Não) |
| `pendencias` | list[Operacao] |
| `tentativas` | int |
| `operacaoId` | UUID |

**Fluxo principal:**

1. Identificar a perda de comunicação e informar que as ações dependentes do servidor estão temporariamente bloqueadas.
2. Preservar o conteúdo digitado na página aberta e manter suas operações sem confirmação visíveis.
3. Quando a comunicação retornar, tentar o envio novamente e reconciliar a confirmação sem outro efeito oficial.
4. Se a tentativa falhar novamente, manter o estado real de falha/pendência; não descartar silenciosamente a entrada.

**Regras e validações da fonte:**

1. Fechar/recarregar não tem recuperação garantida; sem inspeção offline completa.

**Alteração, exclusão e consulta:**

- Alteração: Não se aplica como cadastro. O sistema atualiza o estado ou o resultado conforme as regras desta operação.
- Exclusão: Não se aplica como ação de exclusão neste requisito.
- Consulta: O estado ou resultado é exibido na tela correspondente ao usuário autorizado.

**Critérios de aceite:**

1. Queda antes ou durante envio mantém o conteúdo visível sem indicar salvamento confirmado.
2. Retorno da conexão permite confirmar a operação uma única vez, inclusive se a primeira gravação ocorreu e só a resposta foi perdida.
3. Fechar ou recarregar a página não é apresentado como recuperação garantida; intervalos, conflitos e eventual cache continuam pendentes.

**Relações e decisões pendentes:** RF010, RF012, RNF04, RNF14, RS013 e RS014; P020.

#### RF012 Exibir estado de salvamento

Apresentar o estado de envio de cada resposta ou arquivo, distinguindo Pendente, Enviando, Salva e Falha com texto, além de cor. Somente confirmação do servidor permite indicar salvamento concluído.

**Participantes:** Sistema apresenta a situação a quem realizou ou acompanha a operação autorizada.

**Condições de uso e preenchimento:** Existir resposta, arquivo ou operação com situação de envio identificável. O estado de envio não é o estado oficial da inspeção.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `estadoEnvio` | Enum; (opções predefinidas) |
| `operacaoId` | UUID |
| `confirmadoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `mensagemErro` | str |

**Fluxo principal:**

1. Antes da confirmação, apresentar Pendente e, durante a comunicação, Enviando.
2. Com confirmação do servidor, apresentar Salva; se não foi possível enviar/confirmar, apresentar Falha ou a pendência correspondente.
3. Mostrar a situação por resposta e por arquivo, com texto e indicação do problema ou da possibilidade de tentar novamente.

**Regras e validações da fonte:**

1. Mostrar estado por resposta/arquivo; cores acompanhadas de texto.

**Alteração, exclusão e consulta:**

- Alteração: Não se aplica como cadastro. O sistema atualiza o estado ou o resultado conforme as regras desta operação.
- Exclusão: Não se aplica como ação de exclusão neste requisito.
- Consulta: O estado ou resultado é exibido na tela correspondente ao usuário autorizado.

**Critérios de aceite:**

1. Os estados mínimos Pendente, Enviando, Salva e Falha podem ser compreendidos sem depender apenas de cor.
2. Salvar a resposta não faz um arquivo com falha aparecer indistintamente como salvo.
3. Demora, desconexão ou erro não mudam a situação para Salva sem confirmação.

**Relações e decisões pendentes:** RF008 a RF011, RNF08 e RNF14; P020.

### Resultado e participação do estabelecimento

#### RF013 Calcular pontuação e classificação

Calcular automaticamente o resultado com base nas respostas e nas regras originais vinculadas à inspeção, sem aplicar retroativamente a versão atual do checklist.

**Participantes:** Sistema calcula; usuário autorizado consulta o resultado.

**Condições de uso e preenchimento:** Respostas oficiais e checklist/regras originais identificados. Fórmula, pesos, Não se aplica, arredondamento, faixas e momento de cálculo dependem das regras validadas.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `resultadoId` | UUID |
| `pontuacao` | Decimal |
| `classificacao` | str |
| `regraId` | UUID |
| `calculadoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |

**Fluxo principal:**

1. Recuperar as respostas confirmadas e a versão das regras da inspeção.
2. Calcular pontuação e classificação segundo essa versão, identificando base e momento do cálculo.
3. Disponibilizar o resultado conforme o acesso e a regra de liberação, preservando revisões posteriores conforme RF020.

**Regras e validações da fonte:**

1. Não calcular com checklist atual; limites, N/A e arredondamento conforme regra versionada.

**Alteração, exclusão e consulta:**

- Alteração: Não se aplica como cadastro. O sistema atualiza o estado ou o resultado conforme as regras desta operação.
- Exclusão: Não se aplica como ação de exclusão neste requisito.
- Consulta: O estado ou resultado é exibido na tela correspondente ao usuário autorizado.

**Critérios de aceite:**

1. Casos de referência aprovados produzem a pontuação e a classificação esperadas e identificam a regra utilizada.
2. Publicação de checklist novo não altera automaticamente a nota de inspeção anterior.
3. Sem fórmula e faixas validadas, o aceite numérico permanece pendente; não se aplica regra inventada para apresentar uma nota.

**Relações e decisões pendentes:** RF007, RF014, RF020 e RF026; P010 e P012.

#### RF014 Concluir inspeção no servidor

Registrar a conclusão da inspeção após as validações exigidas pelo fluxo e a confirmação do servidor. Conclusão não libera automaticamente o resultado ao estabelecimento.

**Participantes:** Fiscal com acesso para concluir; o servidor efetiva e confirma.

**Condições de uso e preenchimento:** Inspeção em situação compatível e registros oficiais identificados. As validações finais, inclusive bloqueio por campos obrigatórios vazios ou envios pendentes/falhos, ainda precisam ser aprovadas.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `estado` | Enum; (opções predefinidas) |
| `concluidaEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `concluidaPor` | UUID |
| `revisao` | int |

**Fluxo principal:**

1. O fiscal solicita concluir a inspeção.
2. O servidor verifica acesso, estado e as validações finais que forem aprovadas e registra a conclusão de forma consistente.
3. Só após a confirmação a tela informa Concluída; publicação ao estabelecimento e emissão do termo seguem suas políticas próprias.

**Regras e validações da fonte:**

1. Proposta: impedir conclusão com obrigatórios vazios ou envios pendentes/falhos; gravação atômica.
2. A conclusão não concede ao estabelecimento acesso a rascunhos ou deliberações internas. O momento da liberação do resultado final segue a regra ainda a definir em RF016.

O bloqueio por obrigatórios vazios ou envios pendentes/falhos continua **proposta a validar**, conforme P009, P012 e P020. A consistência exigida por RNF04 não aprova automaticamente essa regra de bloqueio.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Sem confirmação do servidor não aparece conclusão oficial realizada.
2. A conclusão identifica responsável e momento e mantém os registros correspondentes.
3. A proposta de bloqueio por obrigatórios ou envios pendentes só terá casos definitivos após validação; concluir não libera conteúdo interno ao estabelecimento.

**Relações e decisões pendentes:** RF008, RF012, RF013, RF015, RF016 e RNF04; P009, P012 e P020.

#### RF015 Gerar termo em PDF

Gerar termo em PDF com os resultados e não conformidades pertinentes após o salvamento confirmado da inspeção. Uma falha na geração não deve apagar a avaliação já registrada nem causar emissão duplicada no reenvio da mesma operação.

**Participantes:** Sistema gera o termo solicitado no fluxo autorizado; usuários o consultam conforme acesso.

**Condições de uso e preenchimento:** Inspeção/revisão salva e confirmada. Modelos, tipos, numeração, condições de emissão e geração síncrona ou posterior continuam a definir.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `documentoId` | UUID |
| `inspecaoId` | UUID |
| `versao` | int |
| `emitidoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `chavePdf` | str |
| `estadoGeracao` | Enum; (opções predefinidas) |

**Fluxo principal:**

1. Identificar a inspeção, o resultado e a revisão confirmada que fundamentam a emissão.
2. Gerar o PDF com os dados e não conformidades pertinentes e registrar identificação, versão, momento e situação da geração.
3. Disponibilizar o documento pelo acesso autorizado; em falha, informar o problema e permitir recuperação sem apagar a inspeção ou emitir duplicata indevida.

**Regras e validações da fonte:**

1. Falha de geração não apaga inspeção; repetição não cria emissão indevida.

As fontes de levantamento preveem termos de autorização, multa e bloqueio/interdição. Seu conteúdo, condição de emissão e validade dependem de P012; isso não inclui pagamento ou cobrança eletrônica.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. O PDF corresponde à revisão confirmada e identifica inspeção e emissão.
2. Falha de geração conserva a inspeção salva e não é apresentada como PDF disponível.
3. Repetir a mesma emissão não cria outro termo indevidamente nem substitui um documento já emitido.

**Relações e decisões pendentes:** RF013, RF014, RF016, RF021, RF025, RNF13 e RS010; P012, P013 e P016.

#### RF016 Consultar resultados finais e termos do estabelecimento

Permitir ao estabelecimento consultar somente seus resultados finais liberados e os documentos finais autorizados, identificando versões. Não disponibilizar respostas em elaboração, avaliações parciais ou decisões internas.

**Participantes:** Estabelecimento autenticado, limitado ao vínculo que possui.

**Condições de uso e preenchimento:** Resultado próprio final liberado ou documento final autorizado. Estar concluída não significa que a inspeção foi publicada; liberação depende de P012.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `estabelecimentoId` | UUID |
| `inspecaoId` | UUID |
| `inicio/fim` | date (dd/MM/yyyy) |
| `pagina` | int |
| `resultadoId` | UUID |
| `documentoId` | UUID |
| `versaoDocumento` | int |

**Fluxo principal:**

1. O estabelecimento consulta seus resultados finais disponíveis, com os filtros admitidos.
2. O servidor verifica o vínculo e a liberação também ao abrir o resultado e ao baixar o termo.
3. A consulta identifica a versão acessível; os próprios envios documentais seguem RF017, sem abrir avaliações em elaboração.

**Regras e validações da fonte:**

1. O vínculo do usuário com o estabelecimento deve ser validado no servidor em toda consulta e download.
2. O estabelecimento acessa o resultado final disponibilizado e seus documentos finais. Não acessa respostas em elaboração, avaliações parciais, deliberações internas ou dados de outros estabelecimentos.
3. O histórico consultável pelo cliente é o de resultados e documentos finais. Seus documentos enviados são consultados conforme RF017.
4. Preservar a identificação da versão do resultado e do termo. Não substituir silenciosamente uma versão já emitida.
5. O momento de liberação do resultado final e eventual aprovação antes da publicação ainda serão definidos. Concluir e publicar não são considerados automaticamente o mesmo evento.

**Alteração, exclusão e consulta:**

- Alteração: Este requisito realiza consulta; o estabelecimento não edita respostas fiscais, pontuação ou termo emitido.
- Exclusão: A consulta não exclui registros.
- Consulta: Filtrar somente os resultados finais acessíveis do estabelecimento autenticado.

**Critérios de aceite:**

1. Resultado final próprio liberado e seu termo autorizado podem ser consultados com a versão identificada.
2. Inspeção em elaboração, resultado ainda não liberado e registro de terceiro são negados.
3. A consulta não permite editar pontuação, resposta fiscal ou termo, nem obter evidência interna por endereço direto.

**Cenário de referência de F003:** Entrar como estabelecimento e tentar consultar uma inspeção em elaboração, um resultado final liberado e uma inspeção de terceiro. Somente o resultado próprio liberado deve ficar acessível.

**Relações e decisões pendentes:** RF015, RF017, RF021, RF024, RS001 e RS010; P002 e P012.

#### RF017 Enviar documentos pelo estabelecimento

Permitir ao estabelecimento anexar documentos relacionados à sua inspeção, com origem, autor e recebimento identificáveis. O envio não altera automaticamente respostas fiscais, pontuação ou termo.

**Participantes:** Estabelecimento envia e consulta documentos próprios; equipe fiscal autorizada recebe/consulta o vínculo.

**Condições de uso e preenchimento:** Usuário vinculado ao estabelecimento e à inspeção correspondente; tipo, prazo e etapa precisam permitir o envio conforme a política ainda aberta. Autoria não é aceita livremente do navegador.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `documentoEnviadoId` | UUID |
| `estabelecimentoId` | UUID |
| `inspecaoId` | UUID |
| `tipoDocumento` | str ou Enum a definir |
| `descricao` | str |
| `nomeOriginal` | str |
| `tipoMime` | str |
| `tamanhoBytes` | int |
| `conteudo` | UploadedFile |
| `autorId` | UUID |
| `enviadoEm` | datetime |
| `estadoEnvio` | Enum |

**Fluxo principal:**

1. O estabelecimento seleciona sua inspeção e o documento e informa o contexto exigido pela categoria.
2. O servidor verifica acesso, vínculo, etapa e validação do arquivo, registra autor/origem e confirma o recebimento.
3. O estabelecimento acompanha seus envios; a análise não altera a avaliação automaticamente e eventual correção segue autorização própria.

**Regras e validações da fonte:**

1. O documento deve ficar vinculado à inspeção e ao estabelecimento correspondente. O servidor identifica o autor pela sessão.
2. O cliente pode anexar seus documentos durante a etapa permitida; esse acesso não libera a visualização do checklist em andamento.
3. Validar arquivo no servidor segundo RS008. Só mostrar como salvo após a confirmação do recebimento, conforme RF010 a RF012.
4. O envio não modifica respostas fiscais, pontuação ou resultado final automaticamente. Após a conclusão, qualquer alteração oficial segue RF018 a RF021.
5. Categorias obrigatórias, formatos, limites, prazos, pedido de complementação e possibilidade de envio após a conclusão ainda serão definidos.
6. UUID não possui máscara. Datas e horas são preenchidas pelo servidor, com fuso, e exibidas em dd/MM/yyyy HH:mm. Limites de texto e arquivos ainda serão definidos.

**Alteração, exclusão e consulta:**

- Alteração: Proposta a validar: uma substituição de documento já confirmado gera novo registro vinculado ao anterior, sem apagar o arquivo recebido.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: O estabelecimento consulta seus próprios envios e a confirmação de recebimento; fiscais autorizados consultam os documentos vinculados à ação.

**Critérios de aceite:**

1. Documento válido para inspeção própria é recebido com vínculo, autoria e confirmação identificáveis.
2. Envio para inspeção de terceiro ou arquivo inválido não é aceito como recebido.
3. Anexar documento não modifica checklist, nota ou termo; envio após conclusão e substituição dependem da política validada.

**Cenário de referência de F003:** Enviar um documento para uma inspeção própria e tentar enviá-lo para inspeção alheia. Confirmar somente o envio autorizado e verificar que a nota e o checklist não mudam por causa do anexo.

**Relações e decisões pendentes:** RF016, RF018 a RF021, RF028, RS008 e RS010; P011 e P016.

### Alteração autorizada e histórico

#### RF018 Solicitar e autorizar alteração da fiscalização

Registrar pedido de alteração com justificativa e decisão anterior à aplicação, obrigatoriamente para correções posteriores à conclusão. A autorização deve se referir à inspeção e à mudança solicitada.

**Participantes:** Solicitante autorizado e autoridade definida pela política; supervisor somente no escopo em que lhe couber decidir.

**Condições de uso e preenchimento:** Inspeção e mudança identificadas, com justificativa e acesso. Correção após conclusão exige o fluxo; mudanças adicionais em andamento sujeitas à autorização dependem de P006.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `solicitacaoId` | UUID |
| `inspecaoId` | UUID |
| `tipoAlteracao` | Enum |
| `camposOuDocumentos` | dict[str, object] |
| `justificativa` | str |
| `solicitanteId` | UUID |
| `solicitadaEm` | datetime |
| `aprovadorId` | UUID |
| `designacaoSupervisorId` | UUID, quando aplicável |
| `decisao` | Enum (Pendente, Aprovada, Rejeitada) |
| `motivoDecisao` | str |
| `decididaEm` | datetime |

**Fluxo principal:**

1. Registrar o que se pretende alterar, a justificativa e os campos/documentos pertinentes, com solicitante e momento.
2. Manter a solicitação pendente até decisão válida, sem aplicar a mudança solicitada.
3. A autoridade competente analisa e registra aprovação ou rejeição e seu contexto; validar designação quando a decisão couber ao supervisor.
4. Aplicar somente o escopo aprovado via RF019; conteúdo modificado exige nova decisão ou revalidação.

**Regras e validações da fonte:**

1. A solicitação identifica o que se pretende alterar e o motivo. Não aplicar a alteração enquanto não houver aprovação válida no servidor.
2. O fiscal solicita; a autoridade responsável decide. Se o aprovador for o supervisor, validar a designação daquela ação, e não apenas o perfil de fiscal.
3. Aprovação deve estar vinculada à inspeção e à mudança solicitada. Uma autorização não libera edição irrestrita.
4. Correções de inspeção concluída exigem autorização, justificativa e histórico. O preenchimento normal do checklist em andamento continua previsto em RF008.
5. Ainda será definido quais mudanças em andamento também exigem autorização, quem pode aprovar na ausência de supervisor e como tratar a solicitação feita pelo próprio supervisor.
6. Documentos novos após a conclusão podem motivar pedido de alteração. A regra de reanálise ainda depende da decisão descrita em RF028.
7. UUID não possui máscara. Datas e horas são preenchidas pelo servidor, com fuso, e exibidas em dd/MM/yyyy HH:mm. Limites de texto e arquivos ainda serão definidos.

**Alteração, exclusão e consulta:**

- Alteração: Se o conteúdo solicitado mudar, exigir nova decisão ou revalidação, sem aproveitar aprovação para uma mudança diferente.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: Solicitante e autoridade autorizada acompanham o pedido. Deliberações internas não integram o acesso do estabelecimento.

**Critérios de aceite:**

1. Pedido pendente ou rejeitado não permite aplicar a mudança.
2. Aprovação válida permite somente a alteração autorizada na inspeção correspondente.
3. Supervisor de outra ação ou aprovação reaproveitada para conteúdo diferente não autoriza a operação; deliberações não são expostas ao estabelecimento.

**Cenário de referência de F003:** Solicitar mudança, tentar executá-la pendente, rejeitada e aprovada. Somente a mudança aprovada, no escopo correto, pode ser aplicada; supervisor de outra ação não pode decidir.

**Relações e decisões pendentes:** RF002, RF008, RF019 a RF021, RF028 e RS002; P005, P006 e P008.

#### RF019 Aplicar correção com histórico

Aplicar somente a correção autorizada e preservar o conteúdo anterior, o novo, a justificativa, quem solicitou, quem decidiu, quem executou e quando ocorreu. Não sobrescrever silenciosamente uma revisão concorrente.

**Participantes:** Executor autorizado; sistema mantém vínculo com solicitante e decisão.

**Condições de uso e preenchimento:** Solicitação aprovada, escopo correspondente e revisão atual verificada. Não basta ter acesso de edição ou conhecer a inspeção.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `correcaoId` | UUID |
| `solicitacaoId` | UUID |
| `antes/depois` | dict[str, object] |
| `executorId` | UUID |
| `aplicadaEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |

**Fluxo principal:**

1. Recuperar a mudança e a decisão válida, verificando novamente escopo, acesso e estado atual.
2. Aplicar somente o conteúdo autorizado e registrar antes/depois, executor, justificativa, momento e vínculos documentais pertinentes.
3. Se afetar a avaliação ou os termos, acionar os comportamentos de RF020 e RF021 sem perder as versões anteriores.

**Regras e validações da fonte:**

1. Histórico preserva valores, autoria e justificativa; conflito de versão deve impedir sobrescrita silenciosa.
2. Aplicar apenas a mudança autorizada em RF018. Conservar o vínculo entre solicitação, decisão, executor, valores anteriores e novos e documentos que motivaram a correção.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. A correção pode ser reconstruída a partir do pedido, decisão, executor e valores anteriores/novos.
2. Mudança sem aprovação correspondente ou fora do escopo não é aplicada.
3. Revisão desatualizada não sobrescreve silenciosamente a alteração de outro usuário; o histórico anterior continua preservado.

**Relações e decisões pendentes:** RF018, RF020, RF021, RF023, RNF04 e RS007; P005, P006 e P017.

#### RF020 Recalcular resultado após correção

Quando a correção autorizada afetar a avaliação, recalcular automaticamente com o checklist e as regras originais e registrar pontuação e classificação anteriores e novas.

**Participantes:** Sistema, a partir de correção autorizada que afete a avaliação.

**Condições de uso e preenchimento:** Correção identificada, resultado anterior preservado e regras originais disponíveis. Documento isolado não é autorização para mudar nota.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `pontuacaoAnterior/nova` | Decimal |
| `classificacaoAnterior/nova` | str |
| `regraId` | UUID |
| `correcaoId` | UUID |

**Fluxo principal:**

1. Identificar o efeito da correção autorizada na avaliação e recuperar a base original.
2. Recalcular automaticamente com essa base e registrar pontuação/classificação anteriores e novas, vinculadas à correção.
3. Destacar a mudança e encaminhar a necessidade de nova emissão conforme RF021, sem sobrescrever o resultado anterior.

**Regras e validações da fonte:**

1. Resultado anterior permanece consultável; mudanças de classificação são destacadas.
2. Se novos documentos motivarem correção autorizada que afete a avaliação, recalcular automaticamente com as versões originais e registrar pontuação e classificação anteriores e novas. O simples recebimento de documento não dispara mudança oficial de nota.

**Alteração, exclusão e consulta:**

- Alteração: Não se aplica como cadastro. O sistema atualiza o estado ou o resultado conforme as regras desta operação.
- Exclusão: Não se aplica como ação de exclusão neste requisito.
- Consulta: O estado ou resultado é exibido na tela correspondente ao usuário autorizado.

**Critérios de aceite:**

1. Correção que afeta a avaliação usa a regra original, ainda que exista versão publicada mais nova.
2. Pontuações/classificações anteriores e novas ficam identificáveis e relacionadas à correção.
3. Receber um documento sem mudança oficialmente autorizada não altera o resultado.

**Relações e decisões pendentes:** RF007, RF013, RF019, RF021 e RF028; P010 e P012.

#### RF021 Versionar termo e retificar

Preservar o termo emitido e, quando necessário, gerar nova versão ou termo retificador relacionado ao anterior, à correção e ao resultado correspondente. Identificar o documento vigente segundo a política aprovada.

**Participantes:** Sistema no fluxo de emissão autorizado; usuários consultam documentos conforme acesso.

**Condições de uso e preenchimento:** Termo anterior identificado e motivo de nova emissão relacionado à revisão/correção. Decidir entre versão nova, retificador e vigência depende da política documental.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `documentoAnteriorId` | UUID |
| `versao` | int |
| `tipo` | Enum; (opções predefinidas) |
| `motivo` | str |
| `vigente` | bool; (Sim ou Não) |
| `emitidoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |

**Fluxo principal:**

1. Identificar o termo anterior, a correção e o resultado que fundamentam a nova emissão.
2. Gerar nova versão ou retificador quando a política aprovada exigir, com motivo, identificação e vínculo ao anterior.
3. Preservar a emissão original e apresentar as relações e a situação documental conforme os acessos e a política de vigência.

**Regras e validações da fonte:**

1. Original preservado; anterior não é sobrescrito; relação entre documentos consultável.
2. Relacionar o documento emitido à correção autorizada e ao resultado correspondente. A necessidade de nova versão ou termo retificador segue a política ainda a definir; a versão anterior permanece preservada.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Documento original continua recuperável e não é sobrescrito pela nova emissão.
2. É possível relacionar termo novo, termo anterior, motivo e resultado correspondente.
3. Não se presume anulação ou perda de vigência por simples edição; aplicar os critérios que forem validados em P012.

**Relações e decisões pendentes:** RF015, RF016, RF019, RF020, RNF13 e RS010; P012, P013 e P016.

#### RF022 Solicitar e autorizar cancelamento da inspeção

Permitir ao fiscal solicitar cancelamento em andamento com justificativa e exigir autorização válida antes de efetivá-lo no servidor. Preservar respostas, arquivos e histórico.

**Participantes:** Fiscal solicita; autoridade ainda a definir decide; servidor efetiva.

**Condições de uso e preenchimento:** Inspeção em andamento, justificativa preenchida e acesso ao pedido. Aprovação válida deve anteceder o cancelamento; nenhum poder de aprovação é concedido por inferência.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `solicitacaoId` | UUID |
| `inspecaoId` | UUID |
| `justificativa` | str |
| `solicitanteId` | UUID |
| `solicitadaEm` | datetime |
| `aprovadorId` | UUID |
| `designacaoSupervisorId` | UUID, quando aplicável |
| `decisao` | Enum (Pendente, Aprovada, Rejeitada) |
| `motivoDecisao` | str |
| `decididaEm` | datetime |
| `canceladaEm` | datetime |
| `estado` | Enum |

**Fluxo principal:**

1. O fiscal solicita cancelar e registra o motivo; o pedido fica separado da situação da inspeção.
2. A autoridade competente analisa e registra sua decisão, verificando escopo/designação aplicável.
3. Somente após aprovação válida o servidor confirma o cancelamento, registra momento/estado anterior e conserva dados/evidências.
4. Pedido rejeitado ou pendente permanece identificável sem cancelamento; o bloqueio de edições durante análise segue decisão ainda aberta.

**Regras e validações da fonte:**

1. O fiscal não efetiva o cancelamento apenas informando uma justificativa. Primeiro deve existir uma decisão de aprovação válida para a inspeção.
2. Justificativa obrigatória não aceita texto vazio ou somente espaços. Registrar solicitante, decisão, responsável e datas.
3. Se a decisão couber ao supervisor, ele deve estar designado para aquela ação. Autoridade aprovadora, substituição e autoaprovação ainda precisam ser definidas.
4. Pedido pendente ou rejeitado não torna a inspeção cancelada. O bloqueio de novas edições durante a análise do pedido ainda será definido.
5. Após aprovação e confirmação do servidor, registrar o cancelamento sem apagar respostas, arquivos ou histórico. Inspeção já concluída segue procedimento de revisão ou anulação ainda a definir.
6. Esta revisão substitui a regra anterior que permitia cancelamento pelo fiscal somente com justificativa.
7. UUID não possui máscara. Datas e horas são preenchidas pelo servidor, com fuso, e exibidas em dd/MM/yyyy HH:mm. Limites de texto e arquivos ainda serão definidos.

**Alteração, exclusão e consulta:**

- Alteração: Não permitir cancelamento direto nem reabertura automática. Registrar cada decisão e conservar o estado anterior no histórico.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: Fiscal e autoridade autorizada acompanham o pedido e a decisão; o registro da inspeção permanece consultável pelos usuários internos autorizados.

**Critérios de aceite:**

1. Sem justificativa, sem aprovação ou com aprovação de outra ação, o cancelamento não é efetivado.
2. Pedido pendente ou rejeitado não torna a inspeção cancelada.
3. Aprovação válida e confirmação efetivam o cancelamento uma única vez e preservam respostas, arquivos e histórico.
4. Inspeção concluída não é cancelada por esse atalho e não há reabertura automática.

**Cenário de referência de F003:** Tentar cancelar sem justificativa, sem aprovação e com aprovação de outra ação: negar. Aprovar corretamente e confirmar no servidor: cancelar uma única vez e preservar os dados e as evidências.

**Relações e decisões pendentes:** RF002, RF018, RF023, RS001, RS002 e RS007; P005, P006, P012 e P021.

#### RF023 Registrar trilha de auditoria

Registrar eventos críticos com autoria, momento e contexto, incluindo designação/troca de supervisor, pedidos e decisões, correções, cancelamento, recebimento de documentos e emissão de termos. Preservar as mudanças pertinentes sem registrar senhas ou credenciais.

**Participantes:** Sistema registra eventos; usuários internos autorizados consultam conforme política de auditoria.

**Condições de uso e preenchimento:** Ocorrer um evento oficial relevante, com ator/contexto identificáveis. Acesso e retenção da trilha continuam em P017.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `eventoId` | UUID |
| `atorId` | UUID |
| `acao` | str |
| `entidade` | str |
| `entidadeId` | UUID |
| `ocorridoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `alteracoes` | dict[str, object] |

**Fluxo principal:**

1. Identificar o evento, o ator, o objeto, o momento e a mudança pertinente.
2. Registrar a sequência ligada ao ato oficial, incluindo designação, solicitação, decisão, correção, cancelamento, recebimento documental e emissão.
3. Permitir reconstrução autorizada sem expor credenciais; correções do histórico seguem novo evento e preservação, não edição livre do anterior.

**Regras e validações da fonte:**

1. Registrar aprovação, correção, cancelamento e emissão; nunca gravar senha/token.
2. Incluir designação e troca de supervisor por ação, solicitações e decisões de cancelamento e alteração, recebimento de documentos do estabelecimento e, quando aprovados os fluxos, adiamento e reanálise.

**Alteração, exclusão e consulta:**

- Alteração: Usuários comuns não editam eventos oficiais. Uma correção gera novo evento e conserva o anterior, conforme RS007; a regra genérica de manutenção da fonte não concede edição livre da auditoria.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. É possível reconstruir quem solicitou, decidiu e executou a alteração e quais valores mudaram quando aplicável.
2. Usuário comum não altera ou apaga eventos; senhas e tokens não integram os registros.
3. Adiamento e reanálise só entram como atos executáveis depois de seus fluxos serem aprovados; log técnico não substitui a trilha oficial.

**Relações e decisões pendentes:** RF002, RF017 a RF022, RS007 e RS012; P017.

### Consulta e acompanhamento

#### RF024 Consultar inspeções com filtros

Permitir consultas autorizadas por situação, estabelecimento, fiscal e período, com navegação paginada. Filtros não ampliam o conjunto de dados permitido ao usuário.

**Participantes:** Usuários autenticados dentro de seus vínculos e escopos de consulta.

**Condições de uso e preenchimento:** Filtros válidos, período inicial não posterior ao final e paginação positiva. Tamanho de página e nomes finais de estados ainda serão detalhados.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `estado` | Enum; (opções predefinidas) |
| `estabelecimentoId/fiscalId` | UUID |
| `inicio/fim` | date; (dd/MM/yyyy) |
| `pagina/tamanho` | int |

**Fluxo principal:**

1. O usuário informa os filtros admitidos de situação, estabelecimento, fiscal e período.
2. O servidor aplica primeiro o limite de acesso e consulta os registros compatíveis com os filtros.
3. Apresentar os resultados paginados sem permitir que filtro ou navegação ampliem a autorização.

**Regras e validações da fonte:**

1. Data inicial não posterior à final; paginação positiva; consulta não amplia acesso.
2. O estabelecimento consulta somente resultados finais e documentos próprios liberados, conforme RF016 e RF017. Filtros não liberam acesso ao checklist em elaboração nem a pedidos internos de autorização.

**Alteração, exclusão e consulta:**

- Alteração: Este requisito realiza consulta. As alterações são feitas nas funções específicas de cadastro ou inspeção.
- Exclusão: A consulta não exclui registros.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Resultados respeitam os filtros válidos e o conjunto de inspeções autorizado ao usuário.
2. Período inválido e paginação não positiva são rejeitados sem ampliar a consulta.
3. Estabelecimento permanece limitado aos próprios envios e resultados finais liberados, sem avaliações em elaboração ou pedidos internos.

**Relações e decisões pendentes:** RF016, RF017, RS001 e RS009; P002, P003 e P012.

#### RF025 Assinatura e registro de ciência

Registrar a identificação do fiscal e do responsável pelo estabelecimento e a ciência de recebimento, vinculadas ao termo correspondente.

**Participantes:** Fiscal e responsável pelo estabelecimento, conforme o mecanismo de ciência que será validado.

**Condições de uso e preenchimento:** Termo e partes identificados. documentoId referencia o termo; a fonte não define, por esse campo, um documento pessoal ou sua máscara.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `fiscalId` | UUID |
| `nomeResponsavel` | str |
| `documentoId` | UUID |
| `registradoEm` | datetime; (dd/MM/yyyy HH:mm; preenchido pelo servidor) |
| `formaRegistro` | Enum; (opções predefinidas) |

**Fluxo principal:**

1. Identificar fiscal, responsável e termo correspondente.
2. Registrar a forma de ciência/assinatura adotada na política aprovada e o momento do registro.
3. Manter a ciência vinculada à emissão correta e recuperável por usuário autorizado.

**Regras e validações da fonte:**

1. O registro deve estar ligado ao termo. A assinatura em tela ou no PDF e sua validade ainda precisam ser definidas.

**Alteração, exclusão e consulta:**

- Alteração: As alterações dependem das permissões do usuário e devem manter o histórico quando afetarem registros da inspeção.
- Exclusão: Não apagar registros e evidências necessários ao histórico da inspeção.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. O registro identifica as partes e a emissão a que se refere.
2. A forma adotada e o momento ficam rastreáveis sem confundir versões de termo.
3. Não declarar assinatura certificada ou validade jurídica específica sem definição e validação de P013.

**Relações e decisões pendentes:** RF015, RF021 e RNF13; P012 e P013.

#### RF026 Dashboard de indicadores e relatórios

Apresentar a usuários autorizados indicadores de inspeções, resultados dos estabelecimentos e irregularidades frequentes, usando dados confirmados. Considerar versões de checklist e regras nas comparações de pontuação.

**Participantes:** Administrador ou usuários de gestão efetivamente autorizados; não há perfil novo Gestor.

**Condições de uso e preenchimento:** Dados confirmados, filtros válidos e permissão definida para indicadores. Supervisão de uma ação não concede visão global automaticamente.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `dataInicial` | date; (dd/MM/yyyy) |
| `dataFinal` | date; (dd/MM/yyyy) |
| `estabelecimentoId` | UUID |
| `totalInspecoes` | int |
| `pontuacao` | Decimal |
| `quantidadeIrregularidades` | int |

**Fluxo principal:**

1. O usuário autorizado seleciona período e recortes permitidos.
2. O sistema agrega inspeções, pontuações e irregularidades a partir do conjunto de dados ao qual esse usuário tem acesso.
3. Apresentar indicadores/relatórios com critérios identificáveis e considerar a comparabilidade das versões usadas nas avaliações.

**Regras e validações da fonte:**

1. Usar dados confirmados e respeitar as permissões. Comparações de notas devem considerar as versões de checklist e regras.
2. O termo gestor não cria um novo perfil. Permissões de indicadores devem ser definidas para o Administrador ou para usuários autorizados; ser supervisor de uma ação não concede acesso global aos indicadores.

**Alteração, exclusão e consulta:**

- Alteração: Este requisito realiza consulta. As alterações são feitas nas funções específicas de cadastro ou inspeção.
- Exclusão: A consulta não exclui registros.
- Consulta: A consulta deve respeitar o perfil do usuário e os vínculos com o estabelecimento ou a inspeção.

**Critérios de aceite:**

1. Indicadores correspondem aos registros confirmados e filtros autorizados.
2. Fiscal supervisor de uma ação não obtém dados globais apenas por sua designação.
3. Comparações de notas não tratam checklists/regras incompatíveis como se fossem a mesma base; critérios dependem de P010.

**Relações e decisões pendentes:** RF013, RF020, RF023 e RF024; P005, P010 e P022.

### Fluxos a validar

#### RF027 Solicitar adiamento da fiscalização

**Situação:** possibilidade identificada, com fluxo pendente de validação em P007. Prever o registro do motivo e das datas do adiamento sem apagar a fiscalização já realizada. Os passos e critérios abaixo só se tornam aplicáveis após a aprovação da política.

**Participantes:** Proposta: solicitante interno e eventual autoridade conforme a política futura.

**Condições de uso e preenchimento:** Fluxo ainda não aprovado. Identificar inspeção, motivo e datas pertinentes; nova data é proposta de reagendamento e não deve ser confundida com o instante de autoria registrado pelo servidor.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `solicitacaoId` | UUID |
| `inspecaoId` | UUID |
| `justificativa` | str |
| `solicitanteId` | UUID |
| `solicitadaEm` | datetime |
| `novaDataProposta` | datetime, se informada |
| `aprovadorId` | UUID, se houver aprovação |
| `decisao` | Enum |
| `dataReagendada` | datetime, se definida |

**Fluxo principal proposto, condicionado à validação:**

1. Se a política for aprovada, registrar pedido e motivo com a data proposta, quando cabível.
2. Submeter à decisão se o fluxo escolhido exigir autorização; pedido pendente não aparece como adiamento efetivado.
3. Registrar o reagendamento/retomada conforme a política aprovada, mantendo datas anteriores, registros e checklist original de inspeção já iniciada.

**Regras e validações da fonte:**

1. A possibilidade de adiamento foi incluída no levantamento. O motivo e as datas propostas devem ser registrados sem apagar o que já foi feito.
2. Adiamento não conclui nem cancela a fiscalização. Uma nova data não deve ser confundida com data efetiva de realização.
3. Proposta a validar: seguir o mesmo fluxo de solicitação e autorização do cancelamento, com decisão registrada antes de efetivar o adiamento.
4. Ainda é necessário decidir se há estado Adiada, quais situações permitem adiamento, quem o autoriza e como ocorre a retomada.
5. Se a inspeção já tiver sido iniciada, preservar a versão original do checklist. Não substituir as regras por causa da mudança de data.
6. UUID não possui máscara. Datas e horas são preenchidas pelo servidor, com fuso, e exibidas em dd/MM/yyyy HH:mm. Limites de texto e arquivos ainda serão definidos.

**Alteração, exclusão e consulta:**

- Alteração: Manter as datas anteriores e os motivos dos reagendamentos. A regra definitiva de retomada depende de validação.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: Usuários internos autorizados consultam o pedido e o histórico de datas.

**Critérios de aceite após aprovação do fluxo:**

1. Depois da validação de P007, verificar situações permitidas, acesso, autorização quando exigida e retomada.
2. Pedido sem decisão necessária não altera a fiscalização como se o adiamento estivesse efetivado.
3. Reagendamento conserva histórico e versão original e não funciona como cancelamento ou conclusão implícitos.

**Cenário de referência de F003:** Após aprovar a política de adiamento, validar o fluxo escolhido, as permissões e a preservação dos registros. Pedido pendente não pode aparecer como adiamento já efetivado.

**Relações e decisões pendentes:** RF007, RF022 e RF023; P007 e P003/P004 quando afetarem o escopo.

#### RF028 Reanalisar documentos após a conclusão

**Situação:** proposta a validar em P008, não aprovada. Avaliar documentos novos que possam motivar correção autorizada de inspeção concluída. Os passos e critérios abaixo não autorizam sua execução antes dessa validação.

**Participantes:** Proposta: equipe de análise e autoridade a definir; estabelecimento fornece seus documentos sem alterar o resultado.

**Condições de uso e preenchimento:** Fluxo ainda não aprovado. Inspeção concluída e documentos vinculados; definir quais situações exigem reanálise, responsáveis, prazos e eventual nova visita.

**Dados de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `reanaliseId` | UUID |
| `inspecaoId` | UUID |
| `solicitacaoAlteracaoId` | UUID |
| `documentosIds` | list[UUID] |
| `responsavelAnaliseId` | UUID |
| `parecer` | str |
| `impactaResultado` | bool |
| `analisadaEm` | datetime |
| `resultadoAnteriorId` | UUID |
| `resultadoNovoId` | UUID, se houver mudança |

**Fluxo principal proposto, condicionado à validação:**

1. Se o fluxo for aprovado, identificar os documentos examinados, a inspeção e a solicitação pertinente.
2. Registrar parecer e avaliar o impacto sem substituir a avaliação oficial por simples recebimento de anexo.
3. Se houver mudança autorizada, aplicar RF019/RF020 e eventual nova emissão de RF021; conservar resultado/termo anteriores e a rastreabilidade do parecer.

**Regras e validações da fonte:**

1. Ainda não foi decidido se toda inclusão de documento após a conclusão exige reanálise ou somente os casos que afetam a avaliação.
2. Proposta a validar: registrar o pedido em RF018, obter autorização e encaminhar os novos documentos a um fiscal responsável para análise.
3. O anexo isolado não altera o resultado oficial. Se a análise levar a correção de respostas ou avaliação, aplicar RF019 e recalcular automaticamente conforme RF020, com as regras originais.
4. Preservar resultado e termo anteriores. Quando a correção exigir documento novo, seguir RF021.
5. Quem analisa, quem aprova, os prazos, a publicação do novo resultado e a necessidade de nova visita ainda precisam ser definidos. Este fluxo não está aprovado.

**Alteração, exclusão e consulta:**

- Alteração: Registrar documentos examinados, parecer, decisão e eventual mudança. Preservar o resultado anterior, inclusive quando a análise mantiver a avaliação.
- Exclusão: Não apagar solicitações, decisões, versões ou evidências necessárias ao histórico.
- Consulta: A equipe autorizada acompanha a análise; o estabelecimento continua limitado aos seus envios e aos resultados finais liberados.

**Critérios de aceite após aprovação do fluxo:**

1. Depois de aprovar a política, testar documento sem impacto e documento que motive pedido de correção.
2. Documento sem correção oficialmente autorizada não muda a nota.
3. Mudança autorizada preserva avaliação anterior, usa regras originais e mantém vínculo entre documentos, parecer, decisão e emissão posterior quando necessária.

**Cenário de referência de F003:** Depois da aprovação do fluxo, testar um documento sem impacto e outro que motive correção. Nenhum anexo pode alterar a nota sozinho; toda mudança oficial deve ser autorizada e rastreável.

**Relações e decisões pendentes:** RF017 a RF021 e RF023; P008, P010, P011 e P012.

## Requisitos não funcionais

Prioridade de cada RNF: **A validar**. Os parâmetros descrevem informações a medir ou verificar; não criam cadastros, colunas obrigatórias ou metas numéricas por si só. Aceite quantitativo depende da meta aprovada, da carga e das condições de medição; resultado sem esse referencial permanece inconclusivo.

#### RNF01 Usabilidade responsiva

Permitir ao fiscal preencher a inspeção em tablet ou celular sem dificuldade para ler os campos ou acionar os botões.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `larguraTela` | int, em pixels |
| `orientacao` | str |
| `etapa` | str |

São dados do teste, sem cadastro obrigatório.

**Regras de funcionamento:** Os formulários devem se ajustar à tela. Os botões de salvar, voltar e anexar evidência devem permanecer acessíveis. Um erro deve indicar o campo e preservar o conteúdo já digitado.

**Como verificar e resultado esperado:** Executar o RF008 e o RF009 em tablet e celular, nas orientações retrato e paisagem. O teste passa se os campos puderem ser lidos e usados, sem sobreposição ou controles cortados.

**Metas e definições pendentes:** A lista de dispositivos e os tamanhos mínimos de tela precisam ser aprovados.

**Relações:** RF008, RF009 e RF012. Pendências: P019.

#### RNF02 Disponibilidade

Manter o sistema acessível durante os períodos de fiscalização e informar quando o serviço estiver indisponível.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `tempoMonitoradoSegundos` | int |
| `tempoIndisponivelSegundos` | int |
| `disponibilidadePercentual` | Decimal |

**Regras de funcionamento:** Monitorar o acesso à aplicação e ao banco. Durante uma falha, a interface não pode indicar salvamento concluído. A manutenção programada deve ser comunicada aos usuários.

**Como verificar e resultado esperado:** Calcular a disponibilidade no período monitorado e simular uma interrupção do serviço. O aceite depende de atingir a meta aprovada e mostrar aviso de indisponibilidade durante a falha.

**Metas e definições pendentes:** Percentual mínimo, horário de atendimento e janela de manutenção ainda serão definidos.

**Relações:** RF010 e RF011. Pendências: P015 e P018.

#### RNF03 Desempenho

Responder às ações do usuário em tempo compatível com o trabalho em campo, inclusive ao salvar respostas, enviar fotos e gerar termos.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `tempoRespostaMs` | int |
| `usuariosSimultaneos` | int |
| `tamanhoArquivoBytes` | int |
| `percentil95Ms` | int |

**Regras de funcionamento:** Medir consulta, gravação, upload e geração de PDF separadamente. O teste deve registrar a rede usada e a quantidade de usuários. A tela deve informar quando uma operação ainda está sendo processada.

**Como verificar e resultado esperado:** Executar as ações com uma carga representativa e comparar o percentil 95, valor abaixo do qual ficam 95% das medições, com as metas aprovadas para cada ação.

**Metas e definições pendentes:** Metas de tempo, volume de usuários e tamanho de arquivo precisam ser definidos antes do teste de aceite.

**Relações:** RF008, RF009, RF015 e RF024. Pendências: P016 e P018.

#### RNF04 Confiabilidade

Evitar gravações parciais e duplicação de respostas ou evidências quando ocorrer falha de rede ou repetição de uma solicitação.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `operacaoId` | UUID |
| `revisao` | int |
| `confirmado` | bool |

Identificadores sem máscara confirmação definida pelo servidor.

**Regras de funcionamento:** Uma operação crítica deve concluir por inteiro ou manter o estado anterior. Uma nova tentativa da mesma operação não pode gerar um segundo efeito. Um erro deve deixar a pendência visível.

**Como verificar e resultado esperado:** Interromper uma gravação e reenviar a solicitação. Conferir que existe um único registro válido e que não há resultado concluído sem os dados correspondentes.

**Metas e definições pendentes:** A estratégia de controle de repetição e de transação será definida no projeto técnico.

**Relações:** RF011, RF014, RF019 e RS013. Pendências: P020.

#### RNF05 Integridade dos dados

Manter os vínculos corretos entre estabelecimento, inspeção, checklist, respostas, evidências, resultados e termos.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `inspecaoId` | UUID |
| `versaoChecklistId` | UUID |
| `itemId` | UUID |
| `documentoId` | UUID |

**Regras de funcionamento:** Rejeitar referências inexistentes ou incompatíveis. Um item deve pertencer à versão usada na inspeção. Uma versão já utilizada não pode ser alterada de forma a modificar o histórico.

**Como verificar e resultado esperado:** Tentar gravar um item de outro checklist e consultar uma inspeção após publicar uma nova versão. O sistema deve rejeitar o vínculo inválido e conservar os dados originais.

**Metas e definições pendentes:** As restrições e os relacionamentos físicos do PostgreSQL serão definidos no modelo de dados.

**Relações:** RF004, RF007, RF013 e RF021. Pendências: P002, P003 e P009.

#### RNF06 Escalabilidade

Permitir que a capacidade do serviço acompanhe o aumento de usuários, inspeções, fotos e documentos.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `usuariosSimultaneos` | int |
| `inspecoesPorDia` | int |
| `arquivosBytes` | int |
| `capacidadeUtilizadaPercentual` | Decimal |

**Regras de funcionamento:** O crescimento não deve causar perda de registros. A solução deve permitir ampliar recursos após medição da carga. Os limites de armazenamento precisam ser acompanhados.

**Como verificar e resultado esperado:** Aumentar gradualmente a carga em ambiente de teste e medir tempo, erros e consumo de recursos. Comparar os resultados com a capacidade e as metas aprovadas.

**Metas e definições pendentes:** Carga esperada, crescimento, retenção e orçamento de hospedagem ainda precisam ser levantados.

**Relações:** RF009, RF015 e RNF03. Pendências: P015, P017 e P018.

#### RNF07 Compatibilidade

Executar as funções do sistema nos navegadores e dispositivos escolhidos para uso da fiscalização.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `navegador` | str |
| `versaoNavegador` | str |
| `sistemaOperacional` | str |
| `dispositivo` | str |

**Regras de funcionamento:** Login, checklist, captura ou seleção de foto e consulta de PDF devem funcionar nos ambientes homologados. Quando a captura direta não estiver disponível, a seleção de arquivo deve continuar acessível.

**Como verificar e resultado esperado:** Repetir login, checklist, envio de documentos pelo estabelecimento, consulta do resultado final e fluxos de autorização em cada ambiente aprovado, incluindo perda e retorno da conexão. Registrar o resultado de cada combinação.

**Metas e definições pendentes:** Não foi definida restrição a um navegador específico. Acesso web está confirmado; a lista de navegadores, sistemas e versões mínimas será homologada com os usuários. Isso não equivale a garantir funcionamento em qualquer navegador. Recomendação a validar: testar navegadores atuais nos tablets e celulares previstos.

**Relações:** RF001, RF008, RF009 e RF015. Pendências: P019.

#### RNF08 Acessibilidade

Permitir que os usuários identifiquem campos, erros e estados da inspeção com clareza.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `rotulo` | str |
| `mensagemErro` | str |
| `ordemFoco` | int |

São propriedades da interface e registros do teste.

**Regras de funcionamento:** Os campos precisam de rótulos. Status como Salvo e Falha devem usar texto, além da cor. O foco deve ser visível e os controles compatíveis com navegação por teclado quando utilizada.

**Como verificar e resultado esperado:** Testar navegação por teclado e leitura assistiva, conferir rótulos e verificar se os estados podem ser entendidos sem distinguir cores.

**Metas e definições pendentes:** A norma e o nível de conformidade a adotar ainda precisam ser aprovados.

**Relações:** RF001, RF008 e RF012. Pendências: P019.

#### RNF09 Manutenibilidade

Facilitar a manutenção do código Python com Django e a alteração de regras sem comprometer funções existentes.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `modulo` | str |
| `versao` | str |
| `resultadoTeste` | bool |

São informações técnicas, sem máscara de tela.

**Regras de funcionamento:** Organizar as responsabilidades da aplicação. As regras do checklist devem ser versionadas. Alterações devem ter descrição, revisão e testes relacionados ao comportamento afetado.

**Como verificar e resultado esperado:** Reproduzir a preparação do ambiente e os testes documentados. Verificar se uma nova versão do checklist preserva inspeções antigas e se as funções afetadas continuam corretas.

**Metas e definições pendentes:** A arquitetura, os ADRs e a spec de fundação já apresentam a organização candidata. As skills técnicas foram preparadas na curadoria, sem aprovar automaticamente a divisão física dos apps; a revisão integrada com autenticação/acesso continua pendente. Versões e critérios efetivos de execução precisam de validação.

**Relações:** RF004, RF007, RF013 e RF020. Pendências: P001, P009 e P010; revisão integrada prevista na Etapa 7.

#### RNF10 Observabilidade

Permitir identificar falhas de consulta, salvamento, upload e geração de PDF para que a equipe possa investigá-las.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `correlacaoId` | UUID |
| `nivel` | Enum |
| `ocorridoEm` | datetime |
| `duracaoMs` | int |
| `codigoErro` | str |

**Regras de funcionamento:** Os registros técnicos devem permitir localizar a operação que falhou. Senhas, tokens e conteúdo sensível desnecessário não podem aparecer nos logs. Acesso aos registros deve ser restrito.

**Como verificar e resultado esperado:** Provocar uma falha controlada, localizar o evento pelo identificador e conferir que ele contém o contexto necessário sem expor credenciais.

**Metas e definições pendentes:** Ferramentas, alertas, responsáveis e prazo de retenção dos logs ainda serão definidos.

**Relações:** RF009, RF015, RS011 e RS012. Pendências: P015 e P017.

#### RNF11 Backup e recuperação

Permitir recuperar o banco, as evidências e os termos após falha ou perda do ambiente principal.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `backupId` | UUID |
| `realizadoEm` | datetime |
| `rpoMinutos` | int |
| `rtoMinutos` | int |
| `restauracaoValidada` | bool |

**Regras de funcionamento:** O backup deve incluir dados e arquivos vinculados. A cópia deve ter acesso restrito. O processo de restauração deve ser testado, com registro do tempo gasto e da perda de dados medida.

**Como verificar e resultado esperado:** Restaurar uma cópia em ambiente separado e abrir uma inspeção com suas fotos e termos. Comparar a perda temporal e o tempo de recuperação com as metas aprovadas.

**Metas e definições pendentes:** RPO é a perda máxima de dados aceitável no tempo; RTO é o tempo máximo de recuperação. Valores, frequência e retenção ainda serão definidos.

**Relações:** RF009, RF015 e RS006. Pendências: P015, P017 e P018.

#### RNF12 Portabilidade

Permitir preparar ambientes de desenvolvimento, teste e produção sem alterar as regras de negócio para cada hospedagem.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `ambiente` | str |
| `versaoAplicacao` | str |
| `configuracaoValidada` | bool |

**Regras de funcionamento:** Configurações de banco, arquivos e credenciais devem ficar fora do código de negócio. A preparação do ambiente precisa ser documentada e reproduzível.

**Como verificar e resultado esperado:** Preparar um novo ambiente com configuração própria e executar acesso, salvamento, upload e consulta de termo. Confirmar que as regras do sistema continuam iguais.

**Metas e definições pendentes:** Provedor de nuvem, empacotamento e estratégia de implantação ainda serão escolhidos.

**Relações:** RNF09, RS011 e RF015. Pendências: P001 e P015.

#### RNF13 Qualidade dos documentos PDF

Gerar termos legíveis e completos, com identificação da inspeção e da versão emitida.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `documentoId` | UUID |
| `versao` | int |
| `emitidoEm` | datetime |
| `tipoTermo` | Enum |
| `inspecaoId` | UUID |

**Regras de funcionamento:** O PDF deve corresponder aos dados confirmados da revisão utilizada. Textos e evidências não podem ficar cortados. Um documento emitido deve ser preservado quando houver retificação.

**Como verificar e resultado esperado:** Gerar termos com textos curtos e longos, abrir o arquivo e conferir os dados, a legibilidade e a relação com a inspeção e o documento anterior.

**Metas e definições pendentes:** Modelo oficial, numeração, mecanismo de assinatura e política de retificação precisam ser validados.

**Relações:** RF015, RF021 e RF025. Pendências: P012, P013 e P016.

#### RNF14 Tratamento de conexão

Informar com precisão o que está salvo e preservar o preenchimento em tela quando houver perda de comunicação.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `estadoEnvio` | Enum |
| `operacaoId` | UUID |
| `conectado` | bool |
| `confirmadoEm` | datetime opcional |

**Regras de funcionamento:** Ao perder a conexão, bloquear ações dependentes do servidor e manter o conteúdo da página aberta. Tentar enviar após a reconexão. Só apresentar Salvo depois da confirmação. Fechar ou recarregar a página não tem recuperação garantida.

**Como verificar e resultado esperado:** Interromper a rede antes e durante o envio e depois restabelecê-la. Conferir preservação em tela, bloqueio temporário, mensagem de pendência e uma única gravação após confirmação.

**Metas e definições pendentes:** Tempo entre tentativas e tratamento de conflitos ainda precisam ser definidos. Inspeção offline completa permanece fora do escopo.

**Relações:** RF010, RF011, RF012 e RS013. Pendências: P014 e P020.

## Requisitos de segurança

Prioridade dos RS: **A validar**, conforme P022. Cada requisito registra o risco, os dados de referência, os controles, a manutenção e a verificação futura. Mecanismo de usuário/senha e sessão Django já está confirmado em DC007; configurações adicionais, retenção e política legal continuam abertas. O texto não é evidência de segurança implementada ou de conformidade.

#### RS001 Autorização no servidor

**Risco tratado:** Um usuário acessar ou alterar uma inspeção sem possuir permissão.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `usuarioId` | UUID |
| `recursoId` | UUID |
| `acao` | Enum |
| `permitido` | bool |

Valores de autorização definidos pelo servidor.

**Controles requeridos:** Verificar usuário, perfil e vínculo com o recurso em cada operação. O estabelecimento acessa seus documentos enviados e resultados finais liberados, sem respostas em elaboração ou deliberações internas. Para autorizações, validar também a designação do supervisor naquela ação. Não confiar apenas no bloqueio de botões nem revelar conteúdo protegido na resposta de erro.

**Alteração e manutenção do controle:** Revalidar permissões após mudança de perfil ou concessão. Negar a ação se a autorização não for válida.

**Como verificar e resultado esperado:** Tentar consultar inspeção alheia, respostas em elaboração com conta de estabelecimento e aprovar pedido de outra ação como supervisor. Negar todos os acessos e manter os dados. Confirmar o acesso ao resultado final próprio liberado e ao envio documental autorizado.

**Definições pendentes e vínculos:** Detalhes dos escopos ainda serão validados. Relaciona-se a RF001, RF002, RF008 e RF016.

**Pendências relacionadas:** P002 a P006.

#### RS002 Menor privilégio e Supervisor

**Risco tratado:** Uma conta receber poderes maiores que os necessários, inclusive por concessão indevida de Supervisor.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `perfil` | Enum |
| `designacaoId` | UUID |
| `fiscalId` | UUID |
| `inspecaoId` | UUID |
| `acaoFiscalizacaoId` | UUID, se houver agrupamento |
| `designadoPor` | UUID |
| `inicio e fim` | datetime |
| `ativa` | bool |

Sem máscara para identificadores.

**Controles requeridos:** Supervisor é função adicional de um usuário com perfil Fiscalização, designada por ação, sem cargo permanente ou quarto perfil. Validar o escopo e a vigência em cada decisão. A participação na equipe não concede supervisão. Não aceitar autoconcessão pelo formulário ou por alteração de requisição.

**Alteração e manutenção do controle:** Registrar concessões e revogações e fazer a revogação valer no servidor, inclusive para sessões existentes.

**Como verificar e resultado esperado:** Designar o fiscal A como supervisor da ação 1 e o fiscal B da ação 2. A deve ser impedido de aprovar atos da ação 2. Substituir ou revogar a designação de A e repetir a decisão na mesma sessão: negar o uso da autorização anterior.

**Definições pendentes e vínculos:** Quem designa e substitui, vigência, quantidade de supervisores, ausência, autoaprovação e agrupamento de inspeções em uma ação ainda precisam ser decididos. RF002, RF005, RF018 e RF022.

**Pendências relacionadas:** P003 a P005.

#### RS003 Autenticação e credenciais

**Risco tratado:** Uso de conta por pessoa não autorizada ou exposição da senha armazenada.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `identificador` | str |
| `senha` | str transitória |
| `hashSenha` | str |
| `ativo` | bool |

Senha de entrada não é persistida em texto legível.

**Controles requeridos:** Validar a identidade antes de abrir sessão. A base de senha local Django já está confirmada; usar seus mecanismos de senha, sem persistir a entrada legível. Não informar se o login ou a senha isoladamente está errado. Recuperação de conta deve validar o titular.

**Alteração e manutenção do controle:** Mudança de senha ou de método de autenticação exige processo aprovado e registro do evento sem a senha.

**Como verificar e resultado esperado:** Testar credencial válida, inválida e usuário inativo; inspecionar armazenamento e logs para confirmar ausência de senha legível.

**Definições pendentes e vínculos:** Política de senha, MFA, SSO, limitação de tentativas e recuperação ainda precisam ser aprovados. RF001.

**Pendências relacionadas:** P014.

#### RS004 Gestão de sessão

**Risco tratado:** Uso de uma sessão expirada, roubada ou mantida ativa após encerramento.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `identificadorSessao` | str |
| `usuarioId` | UUID |
| `criadaEm e expiraEm` | datetime |
| `revogada` | bool |

Não mostrar o identificador ao usuário.

**Controles requeridos:** Usar a sessão Django confirmada em DC007 e proteger transporte e armazenamento no navegador. Configurar as proteções de cookies segundo a implantação e a política validadas. Exigir autenticação nas operações protegidas e impedir reutilização após revogação.

**Alteração e manutenção do controle:** Logout deve encerrar a sessão correspondente. Aplicar expiração e revalidar permissões alteradas.

**Como verificar e resultado esperado:** Após logout ou expiração, repetir uma requisição protegida. O acesso deve ser negado e uma nova autenticação solicitada.

**Definições pendentes e vínculos:** A sessão Django é decisão confirmada; não continua aberta como alternativa geral. Prazo, sessões simultâneas, backend/configuração de sessão e política de revogação ainda precisam de definição. RF001 e RF002.

**Pendências relacionadas:** P014 e P015.

#### RS005 Proteção do tráfego

**Risco tratado:** Intercepção ou alteração de credenciais, respostas e evidências durante a comunicação.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `dominio` | str |
| `certificadoValido` | bool |
| `expiraEm` | datetime |

São parâmetros de configuração e monitoramento.

**Controles requeridos:** Usar HTTPS nas páginas e nas operações que transmitem dados. O navegador deve validar o certificado. Arquivos protegidos também precisam de transporte seguro. Não colocar credenciais em URLs.

**Alteração e manutenção do controle:** A renovação de certificado deve ser acompanhada para evitar indisponibilidade por vencimento.

**Como verificar e resultado esperado:** Abrir o sistema, autenticar e enviar uma evidência; conferir que as conexões usam HTTPS e certificado válido.

**Definições pendentes e vínculos:** Domínio, configuração TLS e renovação dependem da hospedagem escolhida. RF001, RF008 e RF009.

**Pendências relacionadas:** P015.

#### RS006 Proteção dos dados armazenados

**Risco tratado:** Leitura indevida do banco, dos arquivos ou das cópias de segurança.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `recursoId` | UUID |
| `classeDado` | Enum |
| `chaveId` | str quando aplicável |
| `responsavelId` | UUID |

**Controles requeridos:** Restringir banco, armazenamento e backups a contas autorizadas. Avaliar criptografia em repouso conforme classificação dos dados. Separar a gestão de chaves do conteúdo protegido. Evitar arquivos em armazenamento público.

**Alteração e manutenção do controle:** Mudanças de acesso e de chave devem seguir procedimento controlado. A retenção e a eliminação dependem da política aprovada.

**Como verificar e resultado esperado:** Com uma conta sem privilégio, tentar ler banco, evidências e backup. Conferir negativa e testar restauração autorizada.

**Definições pendentes e vínculos:** Classificação, criptografia em repouso, gestão de chaves e retenção ainda precisam ser definidas. RNF11 e RF009.

**Pendências relacionadas:** P017.

#### RS007 Proteção da auditoria

**Risco tratado:** Apagar ou modificar o histórico para ocultar correções, aprovações ou cancelamentos.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `eventoId` | UUID |
| `atorId` | UUID |
| `ocorridoEm` | datetime |
| `acao` | str |
| `objetoId` | UUID |
| `antes e depois` | dict quando aplicável |

**Controles requeridos:** Registrar designação de supervisor por ação, pedidos e decisões de alteração e cancelamento, correções e recebimento de documentos, com autoria e contexto. Adiamento e reanálise entram na auditoria quando seus fluxos forem aprovados. Usuários comuns não editam nem excluem eventos; não registrar senhas ou tokens. Toda correção produz evento novo.

**Alteração e manutenção do controle:** Restringir consulta da auditoria e registrar intervenções administrativas conforme procedimento a definir.

**Como verificar e resultado esperado:** Executar correção e cancelamento e conferir os eventos. Tentar alterar ou remover o histórico com usuário sem autorização; a ação deve falhar.

**Definições pendentes e vínculos:** Retenção e proteção contra alteração administrativa serão definidas. RF018, RF019, RF022 e RF023.

**Pendências relacionadas:** P017.

#### RS008 Validação de arquivos

**Risco tratado:** Receber arquivo incompatível, adulterado ou com conteúdo perigoso como evidência.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `arquivoId` | UUID |
| `nomeOriginal` | str |
| `tipoMime` | str |
| `tamanhoBytes` | int |
| `resumoIntegridade` | str se adotado |

**Controles requeridos:** Validar formato, tamanho e conteúdo no servidor para evidências fiscais e documentos do estabelecimento. Não confiar apenas na extensão ou no tipo informado pelo navegador. Usar nome interno seguro e manter os vínculos aplicáveis com inspeção, estabelecimento e item. Identificar a origem e a autoria. Arquivo rejeitado não aparece como salvo.

**Alteração e manutenção do controle:** Substituição ou remoção de evidência já confirmada deve seguir a política de histórico e correção.

**Como verificar e resultado esperado:** Enviar arquivo permitido, extensão enganosa e arquivo acima do limite configurado. O sistema deve aceitar somente o válido.

**Definições pendentes e vínculos:** Formatos, teto de bytes, quantidade, verificação antimalware e uso de resumo de integridade ainda serão definidos. RF009.

**Pendências relacionadas:** P011, P016 e P017.

#### RS009 Validação das entradas

**Risco tratado:** Gravar dados inválidos ou executar uma ação fora das regras por manipulação da requisição.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `campo` | str |
| `valor` | object |
| `codigoErro` | str |

O tipo efetivo depende do campo do requisito funcional.

**Controles requeridos:** Validar no servidor tipos, obrigatoriedade, tamanho, referências e opções permitidas. Usar as consultas parametrizadas oferecidas pelo ORM quando aplicáveis. Proteger saídas e operações web contra conteúdo indevido e requisições forjadas.

**Alteração e manutenção do controle:** Alterações passam pelas mesmas validações do cadastro. Campos de autoria e permissão não são aceitos livremente do cliente.

**Como verificar e resultado esperado:** Enviar tipo errado, identificador inexistente, texto acima do limite configurado e opção não permitida diretamente ao servidor. Rejeitar sem gravação parcial.

**Definições pendentes e vínculos:** Limites por campo e configurações de proteção web serão definidos no projeto técnico. RF003, RF008 e RF019.

**Pendências relacionadas:** P002, P009 e P016.

#### RS010 Acesso a evidências e termos

**Risco tratado:** Obter uma foto ou PDF sem autorização usando seu endereço direto.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `arquivoId` | UUID |
| `usuarioId` | UUID |
| `documentoId` | UUID |
| `expiraEm` | datetime se houver link temporário |

**Controles requeridos:** Validar acesso também no download e na visualização. O estabelecimento não obtém evidências internas ou PDFs ainda não liberados por conhecer o endereço. Pode acessar seus envios e documentos finais autorizados. Não expor chaves internas. Se houver link temporário, restringir validade e acesso conforme o desenho aprovado.

**Alteração e manutenção do controle:** Reavaliar permissão após revogação. Preservar arquivos emitidos conforme a política de documentos.

**Como verificar e resultado esperado:** Abrir endereço direto sem sessão e com usuário de outro estabelecimento. Nenhum dos dois pode obter o arquivo protegido.

**Definições pendentes e vínculos:** Estratégia de entrega e prazo de links temporários ainda serão escolhidos. RF009, RF015, RF016 e RF021.

**Pendências relacionadas:** P012 e P016.

#### RS011 Gestão de segredos

**Risco tratado:** Exposição de senha do banco ou de chaves de serviço no código, navegador ou logs.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `nomeConfiguracao` | str |
| `versao` | str |
| `rotacionadoEm` | datetime |

O valor do segredo não integra cadastros de negócio.

**Controles requeridos:** Manter credenciais fora do código-fonte e do conteúdo enviado ao navegador. Separar valores por ambiente e restringir quem pode lê-los. Não incluir segredos em mensagens de erro ou evidências de teste.

**Alteração e manutenção do controle:** Troca e revogação devem seguir procedimento documentado, com verificação de funcionamento após a alteração.

**Como verificar e resultado esperado:** Revisar código, configuração distribuída e logs e confirmar ausência de segredos expostos; validar acesso restrito ao mecanismo escolhido.

**Definições pendentes e vínculos:** Serviço de gestão, responsáveis e frequência de rotação ainda serão definidos. RNF10 e RNF12.

**Pendências relacionadas:** P015 e P017.

#### RS012 Proteção dos logs

**Risco tratado:** Vazamento de credenciais ou informações sensíveis por registros técnicos.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `correlacaoId` | UUID |
| `nivel` | Enum |
| `ocorridoEm` | datetime |
| `mensagem` | str |
| `codigoErro` | str |

**Controles requeridos:** Registrar apenas o contexto necessário. Omitir ou ocultar credenciais, tokens e dados sensíveis desnecessários. Restringir consulta e exportação. Mensagens de erro da interface não devem exibir detalhes internos do servidor.

**Alteração e manutenção do controle:** A limpeza deve seguir a retenção aprovada; usuários operacionais não podem alterar livremente os registros.

**Como verificar e resultado esperado:** Provocar erro de login, upload e banco em ambiente de teste. Inspecionar interface e logs e confirmar que não há segredo nem conteúdo indevido.

**Definições pendentes e vínculos:** Campos permitidos, retenção e permissões de consulta ainda precisam ser definidos. RNF10, RS003 e RS011.

**Pendências relacionadas:** P015 e P017.

#### RS013 Retentativa sem duplicidade

**Risco tratado:** Criar respostas, evidências ou documentos duplicados após timeout e reenvio.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `operacaoId` | UUID |
| `usuarioId` | UUID |
| `resultadoId` | UUID |
| `resumoRequisicao` | str se utilizado |
| `confirmadoEm` | datetime |

**Controles requeridos:** Associar a operação a um identificador estável. Reenvios iguais devem retornar o mesmo efeito confirmado. A mesma identificação com conteúdo diferente deve ser rejeitada ou tratada como conflito. Impedir duplicidade também em tentativas simultâneas.

**Alteração e manutenção do controle:** Uma alteração posterior é nova operação e não deve sobrescrever silenciosamente o efeito anterior.

**Como verificar e resultado esperado:** Confirmar a gravação no servidor, interromper a resposta e reenviar. Verificar um único registro; repetir com duas tentativas concorrentes.

**Definições pendentes e vínculos:** Prazo de deduplicação, algoritmo e controle de concorrência serão definidos. RF011, RF014 e RF015.

**Pendências relacionadas:** P020.

#### RS014 Preservação temporária no navegador

**Risco tratado:** Exposição de dados pendentes em aparelho compartilhado ou armazenamento local sem controle.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `pendenciaId` | UUID |
| `usuarioId` | UUID |
| `conteudo` | dict |
| `expiraEm` | datetime se houver persistência local |

**Controles requeridos:** A preservação do conteúdo na página aberta está confirmada. Armazenamento persistente no navegador é condicional e ainda não foi aprovado. Se adotado, limitar conteúdo e prazo, separar por usuário e estabelecer proteção e limpeza.

**Alteração e manutenção do controle:** Logout, expiração e troca de conta precisam de tratamento definido para impedir acesso a dados de outro usuário. Dados não confirmados continuam pendentes.

**Como verificar e resultado esperado:** Testar perda de conexão com página aberta. Se houver cache aprovado, testar troca de conta, expiração e limpeza de acordo com a política definida.

**Definições pendentes e vínculos:** Decidir se existirá cache persistente e como proteger e recuperar seus dados. Não habilita inspeção offline completa. RF011 e RNF14.

**Pendências relacionadas:** P014 e P020.

#### RS015 Gestão de vulnerabilidades

**Risco tratado:** Manter versões vulneráveis do Python, Django ou de outras dependências sem acompanhamento.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `componente` | str |
| `versao` | str |
| `severidade` | Enum |
| `situacao` | Enum |
| `identificadoEm e corrigidoEm` | datetime |

**Controles requeridos:** Manter inventário de dependências e verificar avisos aplicáveis. Avaliar impacto e priorizar correções. Testar a atualização antes da implantação e registrar o tratamento de cada achado.

**Alteração e manutenção do controle:** Versões devem ser atualizadas por processo controlado, com registro da alteração e possibilidade de recuperação do ambiente.

**Como verificar e resultado esperado:** Revisar o inventário, conferir o tratamento de um achado e executar os testes relacionados após atualizar uma dependência.

**Definições pendentes e vínculos:** Ferramenta de análise, frequência e prazo por severidade ainda precisam ser definidos. RNF09 e RNF12.

**Pendências relacionadas:** P001 e P015.

#### RS016 Resposta a incidentes

**Risco tratado:** Demora para conter acesso indevido, perda ou exposição de dados.

**Dados e parâmetros de referência (F003)**

| Dado de referência | Tipo, formato ou condição descrita na fonte |
|---|---|
| `incidenteId` | UUID |
| `severidade` | Enum |
| `responsavelId` | UUID |
| `abertoEm e encerradoEm` | datetime |
| `medidas` | str |

**Controles requeridos:** Definir canal de registro, responsável pela análise e procedimento de contenção e recuperação. Preservar evidências pertinentes e restringir o acesso ao relato. Registrar decisões e medidas adotadas.

**Alteração e manutenção do controle:** Revisar o incidente até o encerramento e ajustar os procedimentos. Comunicação externa seguirá a política aprovada pelos responsáveis.

**Como verificar e resultado esperado:** Simular um incidente e verificar registro, acionamento do responsável, contenção, recuperação e revisão do ocorrido.

**Definições pendentes e vínculos:** Responsáveis, canais, prazos e regras de comunicação ainda serão aprovados. RNF10, RNF11 e RS007.

**Pendências relacionadas:** P015 e P017.

## Fora do escopo aprovado atualmente

- Inspeção completa offline, sincronização de visitas inteiras e garantia de recuperar dados não confirmados depois de fechar ou recarregar a página.
- Aplicativo nativo obrigatório, API pública e integrações com órgãos ou sistemas externos ainda não aprovadas.
- Pagamento ou cobrança eletrônica de multas; prever um tipo de termo de multa não cria um sistema de cobrança.
- Divulgação pública de rankings, geolocalização e processo formal de contestação, sem decisão posterior.
- Escolha de provedor, biblioteca de PDF, armazenamento, assinatura digital certificada ou metas numéricas por suposição.

MFA, SSO, recuperação de conta e armazenamento persistente no navegador são decisões pendentes, não funcionalidades incluídas automaticamente nem proibições definitivas. A operação real depende de resolver as políticas de segurança pertinentes.

## Priorização e dependências

A elaboração inicial da Etapa 2 e esta revisão consolidam o produto, sem definir um cronograma de implementação. P022 continua aberta para escolher a primeira versão, priorizar o catálogo e estimar prazo e custo. Não há classificação de todos os requisitos como essenciais nem data de entrega assumida.

Antes de implementar acesso e supervisão, resolver os aspectos aplicáveis de P002 a P005 e P014. Antes do checklist e cálculo, resolver P009 e P010. Documentos, assinatura e publicação dependem de P011 a P013 e P016. Metas de operação e aceite dependem de P015, P017 a P020. RF027 e RF028 não podem ser tratados como fluxos prontos enquanto P007 e P008 estiverem abertas.

As validações de conclusão de RF014 precisam de detalhamento, incluindo a proposta de bloqueio com obrigatórios vazios ou envios pendentes. Essa pergunta será tratada junto de P009, P012 e P020, sem assumir uma decisão adicional nesta etapa. P021 mantém a revisão dos protótipos necessária antes de usá-los como especificação.

## Roteiro das especificações

| Momento | Especificação ou área | Relação principal com o produto |
|---|---|---|
| Etapa 4 | [Fundação técnica proposta](../specs/0001-fundacao-tecnica.md) | Requisitos de qualidade e segurança aplicáveis à base; demais funções permanecem futuras |
| Etapa 5 | [Autenticação proposta](../specs/0002-autenticacao.md) | RF001, RS003 e RS004 detalhados, com as políticas abertas identificadas |
| Etapa 6 | [Perfis e acesso propostos](../specs/0003-acesso-vinculos-supervisao.md) e [matriz](../matriz-rastreabilidade.md) | RF002 e RS001/RS002; limites de RF016 e dos atos de RF018/RF022, sem implementar esses fluxos |
| Após o recorte inicial, por solicitação | Cadastros e checklist | RF003, RF004 e RF007 |
| Após o recorte inicial, por solicitação | Inspeção, respostas e envios | RF005, RF006, RF008 a RF012 e RF014 |
| Após o recorte inicial, por solicitação | Resultado, termos e ciência | RF013, RF015, RF020, RF021 e RF025 |
| Após o recorte inicial, por solicitação | Participação do estabelecimento | RF016 e RF017 |
| Após o recorte inicial, por solicitação | Autorizações e auditoria | RF018, RF019, RF022 e RF023 |
| Após o recorte inicial, por solicitação | Consultas e indicadores | RF024 e RF026 |
| Somente após validar a proposta e solicitar o trabalho | Adiamento e reanálise | RF027 e RF028 |

Os grupos posteriores organizam o trabalho futuro; não fixam número de arquivos, contratos ou ordem definitiva de implementação. RNF e RS acompanham as áreas em que se aplicam. A [matriz completa](../matriz-rastreabilidade.md) foi elaborada na Etapa 6, com cobertura documental e validações futuras, sem evidência de implementação. As specs de fundação, autenticação e acesso estão Propostas; demais specs serão elaboradas nos recortes correspondentes.

## Critérios de conclusão do produto

São cenários de validação para a versão de software que incorporar as áreas correspondentes, depois de resolver suas pendências e aprovar o recorte. Nenhum cenário foi executado nesta etapa documental.

1. Usuário ativo entra e sai; perfis e vínculos limitam o acesso, inclusive em solicitações diretas e downloads.
2. Administrador atribui inspeção e fiscal inicia diretamente, preservando autoria e origem; equipes com supervisores diferentes mantêm escopos distintos.
3. Checklist é preenchido com irregularidades e evidências vinculadas e permanece na versão original depois de uma publicação posterior.
4. Falha de comunicação preserva a tela, bloqueia ações oficiais e permite confirmar uma única gravação ao reconectar, sem salvamento fictício.
5. Conclusão e geração de PDF usam os registros confirmados; resultado e termo correspondem aos critérios aprovados e têm versões identificáveis.
6. Estabelecimento envia documentos e consulta apenas seus envios e resultados finais liberados, sem modificar a avaliação automaticamente.
7. Pedido de alteração ou cancelamento pendente, rejeitado ou fora do escopo não é efetivado; pedido aprovado produz o efeito autorizado e deixa histórico.
8. Correção que afeta a avaliação recalcula pelas regras originais e preserva resultado e termo anteriores, com emissão posterior quando necessária.
9. Indicadores e consultas usam dados autorizados, e as verificações de qualidade, segurança e recuperação atendem aos critérios e metas aprovados para a versão.
10. Adiamento e reanálise só passam a ter critérios de conclusão da versão após a aprovação dos respectivos fluxos, sem presumir sua inclusão atual.

## Situação desta entrega

Este PRD foi iniciado na Etapa 2 e recebeu esta revisão de detalhamento por solicitação do usuário, com comparação ao documento F003. Foram preservados os 58 IDs e recuperados dados, formatos, regras de manutenção e verificações, com fluxos e critérios explícitos. O status permanece Proposto; a revisão não implementa funções nem aprova pendências. A Etapa 5 foi posteriormente solicitada e está documentada na Spec 0002, também Proposta; a Etapa 6 foi posteriormente solicitada e suas entregas permanecem Propostas; a Etapa 7 revisou as skills técnicas e a Etapa 8 consolidou as orientações e a [revisão final](../revisao-final-fundacao.md), sem aceitar automaticamente este PRD ou iniciar implementação. O [estado](../state.md) registra o ponto de retomada e as [etapas](../etapas.md) mostram a sequência acordada.
