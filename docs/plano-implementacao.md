# Plano de implementação — Sistema de Avaliação de Segurança Alimentar

- **Data:** 15/11/2026.
- **Status:** Roteiro aprovado em 15/11/2026. I00 aceita. I01 a I12 concluídas no ambiente local. I13 aguarda autorização.
- **Base:** [PRD](prd/0001-sistema-avaliacao-seguranca-alimentar.md), [matriz de rastreabilidade](matriz-rastreabilidade.md), [arquitetura e ADRs](arquitetura.md), [decisões confirmadas](decisoes-confirmadas.md) e [pendências](pendencias.md).
- **Fundação:** [decisões da I00](decisoes-fundacao-i00.md) e [verificações da I01](entrega-i01.md).
- **Acompanhamento:** [Plano no Trello](https://trello.com/c/Ok3dpbjJ), [rotina do quadro](acompanhamento-trello.md) e [estado](state.md).

## Como aprovar e executar

Este plano organiza a próxima fase, após as oito etapas documentais. Os códigos **I00 a I14** pertencem ao roteiro de implementação; não substituem os IDs do PRD. A ordem indica dependências, sem aprovar escopo, prioridades, datas ou estimativas de entrega. Não há autorização para executar o plano todo em sequência.

1. O roteiro foi aprovado em 15/11/2026, com autorização para a I00. O pedido de seguir autorizou a I01 com as escolhas apresentadas no [registro da I00](decisoes-fundacao-i00.md).
2. Antes de cada etapa, confirmar o recorte, a spec aplicável e apenas as decisões que bloqueiam aquele trabalho. Se parte da etapa estiver bloqueada, indicar o que pode ser separado sem inventar a regra pendente.
3. Entregar a etapa com evidências verificáveis, atualizar estado/matriz/Trello conforme o que foi executado e parar para revisão. Iniciar a próxima somente por solicitação. Se uma etapa reunir entregas independentes, aprovar o subrecorte indicado antes de executar.

A fundação tem execução registrada na I01. A I02 verificou o fluxo básico da Spec 0002 e o backend do ADR 0008. Para os fluxos posteriores, escrever e validar a spec funcional antes do código.

## Sequência proposta

| Etapa | Entrega | Dependência principal |
|---|---|---|
| I00 | [Decisões de partida](decisoes-fundacao-i00.md) | Aceitas |
| I01 | [Fundação executável com Django e PostgreSQL](entrega-i01.md) | Verificada no ambiente local |
| [I02](entrega-i02.md) | Login, logout e sessão | I01 |
| [I03](entrega-i03.md) | Usuários, estabelecimentos, perfis e vínculos | I02 e escopo cadastral aprovado |
| [I04](entrega-i04.md) | Cadastro, publicação e versões do checklist | I03 e P009 |
| [I05](entrega-i05.md) | Atribuição, início, equipe e supervisão por ação | I03/I04 e regras de escopo/designação |
| [I06](entrega-i06.md) | Preenchimento, evidências e confirmação de envio | I05 e regras de arquivos/reenvio |
| [I07](entrega-i07.md) | Envio de documentos pelo estabelecimento | I03/I05 e contrato de recebimento de I06 |
| [I08](entrega-i08.md) | Cancelamento autorizado e auditoria do ciclo | I05, P005/P006 e registros dos atos anteriores |
| [I09](entrega-i09.md) | Pontuação, classificação e conclusão | I06 e regras de cálculo/conclusão; validar I07/I08 quando aplicáveis ao fluxo |
| [I10](entrega-i10.md) | Emissão de termo, publicação e consulta do estabelecimento | I09 e políticas de documentos/publicação |
| [I11](entrega-i11.md) | Correção autorizada, recálculo e retificação | I08–I10 e políticas de revisão/versões |
| [I12](entrega-i12.md) | Consultas, indicadores e relatórios | Inspeções e resultados no recorte autorizado |
| I13 | Homologação, recuperação e piloto | Fluxos aprovados para o piloto, com segurança e metas verificadas |
| I14 | Adiamento e reanálise, se aprovados | P007/P008, specs próprias e autorização específica |

## I00 — Decisões de partida · sem código

**Entrega:** proposta de decisão para tornar I01 executável. Comparar versões suportadas e compatíveis de Python/Django/PostgreSQL, driver e preparação de ambientes (P001), com fontes oficiais no momento da avaliação. Validar a parte estrutural da [Spec 0001](specs/0001-fundacao-tecnica.md) e do [ADR 0007](adr/0007-monolito-modular.md): organização inicial, configuração e separação entre desenvolvimento/teste. Definir, na parte aplicável de P002, app/modelo do usuário customizado, identificador e campos indispensáveis para a primeira migração. Não antecipar vínculos ou designações no schema inicial.

**Aceite:** apresentar uma recomendação por decisão, alternativas relevantes, impacto e o que pode ser adiado. Registrar aceite como decisão somente após retorno explícito. Entregar o recorte de I01 pronto para autorizar, sem instalar pacotes, gerar arquivos da aplicação, configurar ambiente ou migrar banco. P022 deve ser tratada antes de comprometer uma primeira versão ou um prazo; não é preciso aprovar as funções posteriores para revisar I01.

## I01 — Fundação executável

**Entrega:** estrutura Django mínima, dependências reproduzíveis, configuração externa por ambiente, PostgreSQL isolado para desenvolvimento/testes, `AbstractUser` configurado antes da primeira migração e templates básicos de erro. Partes candidatas: `manage.py`, `config/`, app de contas e templates, conforme a Spec 0001 aprovada para o recorte. Usar parâmetros fictícios em exemplos e verificar como os arquivos de ambiente serão excluídos do versionamento antes de colocar valores reais em uso. Não usar esquema ou versões do blog como base.

**Antes de executar:** I00 aceita na parte de I01; P001 e a parte estrutural de P002 resolvidas. Sem login, vínculo, inspeção ou ambiente operacional nesta etapa.

**Aceite:** reproduzir o preparo isolado; comprovar que o banco efetivo é PostgreSQL; criar o usuário customizado na migração inicial; rejeitar configuração inválida sem vazar segredos ou cair para SQLite; verificar templates de erro e isolamento. Usar **VF01–VF12** da Spec 0001 conforme aplicabilidade.

## I02 — Autenticação e sessão · RF001

**Entrega:** entrada por usuário e senha, área protegida mínima e saída, com form/mecanismos nativos, views próprias derivadas de `View` e CSRF. A [Spec 0002](specs/0002-autenticacao.md) detalha campos, rotas, redirecionamento, sessão, erros e falhas. Autenticar não concede perfil, vínculo ou poder de aprovação.

**Antes de executar:** I01; validar o backend de sessão recomendado no [ADR 0008](adr/0008-sessoes-no-servidor-com-postgresql.md) ou alternativa que satisfaça a invalidação no servidor. Resolver a parte de P014/P015 aplicável ao recorte; as políticas de recuperação, MFA/SSO e revogação global não entram sem decisão. A recuperação após resposta perdida no login depende do tratamento de credenciais de P014/P020, separado da retentativa de inspeção.

**Aceite:** conta ativa entra; senha incorreta, conta inexistente e conta inativa recebem a mesma negativa pública; destino externo é recusado; saída por POST invalida a sessão corrente no servidor; reapresentar a chave encerrada não recupera acesso. Verificar falha de gravação da sessão no middleware e ausência de credenciais em URL/log. Usar **AU01–AU32** conforme o recorte e anotar o que ficou condicionado.

**Resultado:** fluxo básico verificado localmente. As evidências e políticas abertas estão na [entrega da I02](entrega-i02.md).

## I03 — Cadastros, perfis e vínculos · RF002 parcial, RF003

**Entrega:** manutenção autorizada de contas/estabelecimentos, três perfis-base e vínculos de acesso. Implementar as áreas cadastrais necessárias em subrecortes se a manutenção de usuários e o vínculo com estabelecimento tiverem dependências distintas. Adotar os controles de histórico pertinentes desde as primeiras mudanças de perfil/vínculo; a auditoria de inspeções será ampliada em I08. A [Spec 0003](specs/0003-acesso-vinculos-supervisao.md) orienta acesso; detalhar o cadastro de estabelecimentos antes do código.

**Antes de executar:** P002 na parte de representação, cardinalidade, autoridade e concessão inicial; P014 para criação/entrega de credenciais e P017 para a parte de histórico da operação. Nenhuma concessão técnica por equivalência com `is_staff` ou superusuário.

**Aceite:** manutenção autorizada funciona; usuário de outro estabelecimento não consegue consultar ou alterar registros por endereço direto; revogar vínculo impede novo acesso na mesma sessão; nenhuma alteração apaga autoria histórica. Usar **AC01–AC07, AC13–AC14 e AC29–AC36** no que for aplicável. Designação de supervisor será entregue em I05.

**Resultado:** cadastros, perfis, vínculo de uma unidade por conta e concessão técnica de Administrador verificados localmente. O canal de entrega de credenciais reais permanece em P014. [Registro da I03](entrega-i03.md)

## I04 — Checklist e versões · RF004, preparação de RF007

**Entrega:** administrar itens e regras; distinguir rascunho de versão publicada. Definir a preservação imutável do conteúdo e das regras utilizadas; preparação para I05 vincular a versão no início da inspeção. A fórmula definitiva entra em I09 conforme P010; se sua representação afetar a versão, decidir o contrato antes de publicar um checklist usado em inspeções oficiais.

**Antes de executar:** I03; P009: referência, conteúdo, obrigatoriedade, opções, governança e publicação. Usar dados fictícios em demonstração; não assumir que modelo ilustrativo seja checklist oficial.

**Aceite:** publicar versão nova não modifica versão já usada; autoria e data da publicação são rastreáveis; acesso indevido é negado. Verificar a preservação no fluxo integrado de início em I05.

**Resultado:** edição e publicação de demonstração verificadas localmente. O conteúdo oficial e a autoridade para publicá-lo seguem em P009. A I05 deverá fixar a versão ao iniciar a inspeção. [Registro da I04](entrega-i04.md)

## I05 — Atribuição, início e supervisão · RF002 parcial, RF005–RF007

**Entrega:** Administrador atribui inspeção/equipe ou fiscal inicia diretamente; definir a versão do checklist no servidor quando a inspeção começar. Modelar supervisão apenas no escopo aprovado. Incluir no contrato os estados e transições do início e o histórico de atribuição, designação e troca, sem conceder poderes de aprovação por consequência.

**Antes de executar:** I03/I04; P003 para relação ação/inspeção; P004 para autoridade, elegibilidade, cardinalidade, substituição e vigência. P005 pode continuar aberta para I08/I11 se I05 não conceder decisão de alteração/cancelamento. Escolher como impedir início conflitante e mudança retroativa de versão antes de efetivar os atos.

**Aceite:** os dois caminhos de início preservam autoria/origem; inspeção em curso mantém a versão original após nova publicação; fiscal designado para A não recebe poder em B; remoção da designação vale na sessão atual. Usar **AC15–AC24** e os cenários de início/versionamento da matriz.

**Resultado:** atribuição, início, versão do checklist e designações simultâneas por ação verificados localmente. Poderes de aprovação continuam em P005. [Entrega da I05](entrega-i05.md)

## I06 — Checklist em campo, evidências e rede · RF008–RF012

**Entrega:** preenchimento em navegador móvel, observações/irregularidades, anexos vinculados e estados de envio. Se o desenho exigir subetapas, primeiro aprovar o contrato de salvamento/reenvio e depois adicionar a captura de arquivos. O comportamento online é parte do primeiro fluxo de gravação oficial, não uma correção para deixar para o final.

**Antes de executar:** I05; P009 para validações dos itens, P016 para armazenamento/limites/validação/entrega privada de evidências, P020 para identidade da operação, recuperação, conflito e limpeza. Definir alvos de dispositivos e revisar protótipo com P019/P021. A escolha de armazenamento para evidências não precisa antecipar biblioteca de PDF.

**Aceite:** preservar o preenchimento na página aberta, bloquear ações dependentes do servidor durante falha, tentar recuperar ao reconectar e só marcar **Salvo** com confirmação. Simular resposta perdida depois da gravação e repetição concorrente: uma única gravação oficial; conteúdo diferente com a mesma operação segue o contrato de conflito aprovado. Arquivo de outro escopo por URL direta é negado. Não garantir recuperação após recarga ou habilitar inspeção offline completa.

**Resultado:** preenchimento e fotos de demonstração verificados, com confirmação separada e retentativa após resposta perdida. Formatos e política operacional seguem em P016/P019/P020. [Entrega da I06](entrega-i06.md)

## I07 — Documentos do estabelecimento · RF017

**Entrega:** receber e consultar documentos do estabelecimento, associados à inspeção, com origem, autoria e confirmação. Separar documentos do cliente, evidências fiscais e termos. Esta entrega pode ser preparada junto aos contratos de I06 se a janela aprovada exigir envio durante o andamento; manter cada recorte de execução autorizado separadamente.

**Antes de executar:** vínculo de I03, inspeção de I05, mecanismo de recebimento/retentativa aplicável de I06; P011/P016/P020 para momento, formato, limites, substituição e reenvio.

**Aceite:** documento próprio é recebido uma vez, durante etapa permitida; tentativa de envio para terceiro ou arquivo inválido não é confirmada. Anexo não libera avaliação interna, muda nota ou dispara reanálise automaticamente. Usar **AC12–AC14** e os cenários de arquivos/reenvio da matriz.

**Resultado:** envio desde a atribuição ao fim do andamento, consulta por unidade e retentativa verificados em demonstração. [Entrega da I07](entrega-i07.md)

## I08 — Cancelamento autorizado e auditoria · RF022, RF023 transversal

**Entrega:** solicitação, decisão e efetivação separadas; registro oficial com autoria, escopo e histórico. Definir e usar contratos de auditoria desde os primeiros atos que precisam de histórico (I03/I05); aqui integrar e verificar a trilha do ciclo, estendida por I10/I11. Atualizar a tela de cancelamento para refletir solicitação/autorização. Não converter inspeção concluída em cancelada por este fluxo.

**Antes de executar:** I05; P005 para autoridade e autoaprovação, P006 para efeitos de pedido pendente, P017 para auditoria/acesso, P020 para repetição concorrente e P021 para a tela. Sem decisão de autoridade, não antecipar concessão ao Administrador ou Supervisor.

**Aceite:** pedido sem justificativa, pendente, rejeitado ou fora do escopo não cancela; aprovação válida permite efetivar uma vez, preservando respostas, evidências e histórico. Supervisor revogado antes da decisão não obtém concessão pela sessão antiga. Testar tentativa de alterar/remover histórico por conta não autorizada, preservando a política aprovada. Usar **AC18, AC21–AC28, AC32–AC35** no que se aplicar.

**Resultado:** DC032 aplicada. A I08 verificou solicitação, decisão contextual e efetivação automática, bloqueio de novas gravações durante a pendência e auditoria por inspeção. [Spec 0009](specs/0009-cancelamento-e-auditoria.md) · [Entrega da I08](entrega-i08.md)

## I09 — Pontuação, classificação e conclusão · RF013/RF014

**Entrega:** cálculo automático com regras da versão original, validação de conclusão e persistência do resultado com autoria e versão. Separar conclusão, emissão de termo e liberação ao estabelecimento.

**Antes de executar:** I06 e contratos pertinentes de I07/I08; P009/P010 para obrigatoriedade, pesos, faixas, arredondamento e “Não se aplica”; validar bloqueios de conclusão propostos em RF014, janelas documentais aplicáveis e comportamento em conflito/reenvio (P011/P012/P020).

**Aceite:** conferir exemplos de cálculo validados; conclusão usa registros confirmados e produz um resultado coerente sem duplicidade. Inspeção pendente de dados/envios recebe o tratamento aprovado para RF014. Nova versão de checklist não muda o cálculo da inspeção iniciada. Resultado interno ainda não liberado não aparece no portal.

**Resultado:** a I09 verificou as regras de demonstração da DC033, calculou pela versão original e registrou a conclusão uma vez, com resultado interno e auditoria. [Spec 0010](specs/0010-pontuacao-e-conclusao.md) · [Entrega da I09](entrega-i09.md)

## I10 — Termo, publicação e consulta externa · RF015/RF016; RF025 condicionado

**Entrega:** PDF com origem e versão, gerável a partir do resultado confirmado; liberação controlada e consulta/download pelo estabelecimento vinculado. Assinatura e ciência (RF025) são subrecorte próprio se P013 for aprovada; documento demonstrativo não deve ser apresentado como termo oficial quando faltar essa política.

**Antes de executar:** I09 e acesso de I03; P012/P016 para modelos, numeração, vigência, publicação, armazenamento e biblioteca; P013 para assinatura/ciência; P020 para confirmação e repetição da emissão. Definir se a geração será síncrona ou posterior conforme contrato aprovado, sem escolher fila por inferência.

**Aceite:** PDF corresponde à versão confirmada, é legível e não sobrescreve emissão anterior; falha na geração não desfaz conclusão ou cria nova emissão indevida. Apenas o estabelecimento vinculado obtém o final liberado e o arquivo autorizado, inclusive por acesso direto. Usar **AC08–AC11** e verificações de RNF13/RS010.

**Resultado:** a I10 verificou emissão e liberação separadas conforme DC034, com PDF preservado e download após autorização da unidade. Assinatura e ciência seguem em P013. [Spec 0011](specs/0011-termo-e-liberacao.md) · [Entrega da I10](entrega-i10.md)

## I11 — Correção, recálculo e retificação · RF018–RF021, RF023

**Entrega:** pedido com justificativa e escopo, decisão e aplicação em operações distintas; histórico com anterior/novo, autoria e datas; recálculo automático com checklist/regras originais quando a avaliação mudar; nova versão/termo retificador quando necessário. Não reabrir inspeção concluída para edição livre.

**Antes de executar:** I08–I10; P005/P006 para autoridade/pedido próprio e alterações, P010/P012 para cálculo/versão/retificação, P017/P020 para história e consistência. P008 só é necessária se este recorte incluir gatilho de reanálise, que permanece condicionado a I14.

**Aceite:** aprovação pendente, rejeitada, de outra inspeção ou para conteúdo diferente não autoriza efeito. Alteração aprovada registra dados e resultados anteriores/novos e preserva o PDF emitido; conflito ou reenvio não duplica a correção nem a retificação. Confirmar que o estabelecimento continua limitado ao que foi liberado.

**Resultado:** DC035 aplicada. A I11 verificou as três operações, cálculo pela regra original, imutabilidade das revisões e retificador com liberação própria. [Spec 0012](specs/0012-correcao-e-retificacao.md) · [Entrega da I11](entrega-i11.md)

## I12 — Consultas e indicadores · RF024/RF026

**Entrega:** listagem interna com filtros e paginação, indicadores/relatórios autorizados e exportações somente se aprovadas no recorte. Não comparar pontuação de versões incompatíveis por padrão.

**Antes de executar:** dados das inspeções/resultados do recorte; aprovação de indicadores e prioridade (P010/P022), requisitos de acesso, privacidade/retenção e volume/meta (P017/P018). Pode-se aprovar uma consulta interna antes do painel, sem antecipar indicadores.

**Aceite:** listagem, contagens, paginação e agregações usam somente dados acessíveis; valores conferem com uma base fictícia conhecida; filtros e exportações não expõem terceiros. Medir desempenho contra metas aprovadas, sem inventar percentuais ou prazos.

**Resultado:** DC036 aplicada. A I12 verificou filtros e paginação no escopo da equipe, painel administrativo com dados confirmados e resultados agrupados por versão e regra. [Spec 0013](specs/0013-consultas-e-indicadores.md) · [Entrega da I12](entrega-i12.md)

## I13 — Homologação e piloto controlado

**Entrega:** ambiente remoto de homologação e roteiro de piloto, com dados autorizados, fluxo completo do recorte escolhido, plano de restauração e critérios de reversão. Segurança, testes, logs e responsividade acompanham cada etapa; aqui são verificados de ponta a ponta. Implantação ou abertura para uso real exige autorização própria quando o escopo e destino estiverem definidos.

**Antes de executar:** aprovar o escopo do piloto em P022, fechar políticas relevantes do recorte, P015–P019 para operação/hospedagem, arquivos, retenção, metas e dispositivos. Sem usar documentos ou credenciais reais em teste por conveniência. P007/P008 não bloqueiam piloto se esses fluxos ficarem fora do recorte aprovado.

**Aceite:** demonstrar o fluxo autorizado em celular/tablet, isolamento, recuperação de rede, HTTPS, ausência de segredos nos registros, restauração do banco com arquivos e procedimento de incidente. Testar integridade e migrações em ambiente isolado; registrar falhas, riscos residuais e decisão de seguir ou corrigir, sem aprovar operação real por automatismo.

## I14 — Adiamento e reanálise, condicionados · RF027/RF028

**Entrega:** dois recortes independentes, somente quando aprovados: reagendamento com história e reanálise de documento novo com parecer/relação ao pedido de correção. Elaborar specs antes do código.

**Antes de executar:** P007 para estados/data/retomada e eventual autorização; P008 para gatilho, autoridade e eventual nova visita. Usar controles de I08/I11 no que se aplicar. A numeração não obriga a incluir os fluxos na primeira versão nem os considera aprovados.

**Aceite:** adiamento preserva contexto e não simula cancelamento/conclusão; reanálise não substitui resultado automaticamente e preserva versões quando houver correção aprovada.

## Qualidade e segurança ao longo das etapas

Esta tabela indica as etapas em que cada grupo será exercitado, sem substituir os requisitos, os critérios ou as lacunas da [matriz](matriz-rastreabilidade.md).

| Grupo | Aplicação e evidência proposta |
|---|---|
| RNF01, RNF07, RNF08 | Layout móvel, teclado/foco e compatibilidade em I02/I03/I06/I07/I10/I12; homologar recorte real em I13, com P019 |
| RNF02, RNF03, RNF06, RNF11 | Disponibilidade, desempenho/capacidade e restauração em I13; medir consultas em I12; metas em P018 |
| RNF04, RNF05 | PostgreSQL e testes de migração/transação em I01; revisar concorrência, histórico e confirmação em toda mutação até I11 |
| RNF09, RNF10, RNF12 | Estrutura reproduzível e erros/logs sanitizados em I01/I02; preservar camadas e diagnóstico; verificar portabilidade operacional em I13 |
| RNF13, RNF14 | PDF legível e versionado em I10/I11; instabilidade de rede em I06/I07 e atos oficiais posteriores, com tratamento de resposta perdida de credenciais dependente de P014/P020 |
| RS001, RS002, RS010 | Acesso negativo, revogação, contexto e autorização por arquivo em I03/I05–I08/I10–I12; validar no servidor, incluindo Admin |
| RS003, RS004, RS009 | Senha, sessão e CSRF em I01/I02; tipos, referências e entradas em todas as mutações |
| RS005, RS006, RS011, RS012, RS015, RS016 | Segredos e dependências em I01; transporte e logs em I02; acesso/retenção do armazenamento, TLS, processo de vulnerabilidades e resposta a incidentes em I13 |
| RS007, RS008, RS013, RS014 | História protegida desde I03 e integrada em I08/I11; arquivos em I06/I07/I10; retentativa e dados pendentes em I06 e atos posteriores, com P020 |

Em cada etapa autorizada, registrar requisitos cobertos total/parcialmente, arquivos afetados, decisões tomadas, cenários executados e evidência sanitizada. Preferir testes de service e banco para invariantes; HTTP e navegador para permissões, sessão e rede. Reproduzir cenários com dados fictícios em PostgreSQL isolado. Nenhuma mudança de schema deve depender de apagar dados operacionais; antes de migrar fora de testes, validar estratégia para restaurar ou avançar com correção, considerando arquivos persistidos junto ao banco.

## Próxima autorização sugerida

A I13 é o próximo recorte e aguarda autorização. Ambiente, metas de operação e escopo do piloto dependem de P015 a P019 e P022. [Entrega da I12](entrega-i12.md) · [Pendências](pendencias.md)
