# Spec 0002: Autenticação e sessão

- **Status:** Proposto; elaboração documental para revisão, sem implementação.
- **Data:** 10/11/2026.
- **Etapa:** 5, somente autenticação.
- **Produto:** [PRD 0001](../prd/0001-sistema-avaliacao-seguranca-alimentar.md), principalmente RF001, RS003 e RS004.
- **Base:** [arquitetura](../arquitetura.md), [decisões confirmadas](../decisoes-confirmadas.md), [ADR 0003](../adr/0003-usuario-customizado-e-sessao-django.md) e fontes F003/F008 no [índice](../referencias/README.md).
- **Depende de:** [Spec 0001 de fundação](0001-fundacao-tecnica.md), ainda Proposta, e das decisões aplicáveis de P001, P002, P014, P015, P017, P019 e P020 nas [pendências](../pendencias.md).
- **Nova recomendação:** [ADR 0008](../adr/0008-sessoes-no-servidor-com-postgresql.md), sessões no servidor com PostgreSQL; não aprovada.

## Objetivo e resultado esperado

Detalhar como uma conta ativa entra com nome de usuário e senha, mantém uma identidade reconhecida pelo servidor e encerra a sessão correspondente. O acesso protegido deve recusar identidade ausente, expirada ou inválida. O documento transforma o RF001 em contratos verificáveis de entrada, tela, HTTP, sessão e falha, preservando as políticas ainda abertas.

Esta entrega não cria aplicação, dependências, ambiente, tabelas, migrações ou testes executáveis. A autorização para elaborar a Etapa 5 não aceita automaticamente suas propostas nem inicia a Etapa 6. Todos os caminhos, nomes, mensagens e comportamentos técnicos novos abaixo são propostas para revisão, salvo quando identificados como base confirmada.

## Confirmado, proposto e aberto

| Tema | Situação | Consequência para esta spec |
|---|---|---|
| Python/Django e PostgreSQL | Confirmado, DC003; versões em P001 | Usar mecanismos do framework; não fixar versão ou driver por exemplo |
| `AbstractUser` customizado, nome de usuário/senha e sessão Django | Confirmado, DC007 | Não substituir por JWT, login por e-mail ou provedor externo por inferência |
| Views próprias com herança direta de `View`; login/logout na camada HTTP | Confirmado, DC005/DC006 | Forms e autenticação nativos são admitidos; services não recebem `request` |
| Conta ativa, erro de credenciais genérico e logout que invalida a sessão | RF001 e RS003/RS004 no PRD Proposto; sem regra conflitante posterior | Preservar o comportamento e detalhar sua verificação |
| Nome `contas.Usuario`, identificador e campos iniciais | Candidatos da Spec 0001; P002 aberta | Não escolher UUID físico nem criar outro usuário paralelo |
| Backend de autenticação `ModelBackend` e form baseado em `AuthenticationForm` | Recomendação desta spec | Aproveitar validação nativa, normalizando a mensagem pública |
| Backend de sessão em banco, `django.contrib.sessions.backends.db` | Recomendação nova, ADR 0008 | Permitir invalidar a sessão no servidor, sem depender apenas de apagar cookie |
| Rotas, classes, templates, mensagens e destino inicial | Contratos candidatos desta spec | Revisar antes da implementação; não são telas implementadas |
| Recuperação, política de senha, tentativas, MFA/SSO, duração e concorrência de sessões | P014 aberta | Não ativar fluxos nem inventar limites; resolver o que afetar a parte implementada |
| Tratamento de senha quando a resposta se perde | Proposta específica, P014/P020 | Validar a reconciliação descrita abaixo antes de implementar a recuperação |

A consulta à documentação oficial apoia o desenho, mas não seleciona a versão do projeto. As APIs, o comportamento nativo e as configurações deverão ser reconferidos na versão escolhida em P001.

## Escopo e limites

Inclui entrada, saída, reconhecimento da sessão em páginas protegidas, destino seguro após login, conta inativa, expiração observável, falhas de comunicação, proteção de credenciais e um plano de aceite. Aplica-se aos três perfis-base, sem conceder funções de negócio ao autenticar.

Cadastro, ativação/inativação administrativa e vínculos de usuários pertencem ao RF002 e à Etapa 6. Aqui se consome a situação da conta existente. Não são criados perfil, grupo, designação de Supervisor, equipe, estabelecimento, inspeção ou permissão de aprovação. Supervisor continua fiscal designado por ação; `is_staff` e superusuário técnico não equivalem a Administrador de negócio ou autoridade aprovadora.

Recuperação/troca de senha, cadastro público, confirmação de e-mail, MFA, SSO, opção de manter conectado, painel de sessões e encerramento em todos os aparelhos não têm fluxo aprovado nesta entrega. Não apresentar controles que prometam essas funções. Sua ausência na spec não encerra P014 nem dispensa sua avaliação para operação real.

## Dependências e pontos de bloqueio

| Parte futura | Condição necessária | Limite enquanto estiver aberta |
|---|---|---|
| Preparar autenticação executável | Resolver versões e preparação P001; validar a fundação e os nomes aplicáveis | Não criar ambiente ou presumir APIs de uma versão |
| Criar usuário e primeira migração | Resolver nome, chave e campos estruturais P002 conforme Spec 0001 | Não cristalizar UUID ou vínculos por conveniência |
| Persistir e invalidar sessão | Validar backend proposto no ADR 0008, integração e configuração aplicável P014/P015 | Não afirmar que qualquer backend atende à reutilização após logout |
| Definir validade e controle de acesso de conta | Resolver política de duração, tentativas, concorrência e revogação pertinente P014 | Defaults técnicos não viram política aprovada do produto |
| Recuperar login/logout após perda da resposta | Validar tratamento de credenciais e de outras abas, P014/P020 | Não implementar reenvio automático de senha por suposição |
| Aceitar interface e operar remotamente | Homologar P019 e definir HTTPS, proxy, cookies, logs e responsabilidades P015/P017 | Sem evidência de compatibilidade ou prontidão operacional |

P003 a P005 impedem fechar supervisão e autoridades na Etapa 6; não são motivo para inventar um vínculo no login. Campos e regras de negócio continuam nos recortes próprios. A spec pode ser revisada enquanto as pendências permanecem abertas; implementação integral e operação não estão liberadas por sua redação.

## Dados e validação de entrada

### Correspondência com as fontes

| Referência do PRD/F003 | Tipo de referência | Correspondência técnica candidata | Regra |
|---|---|---|---|
| RF001 `login`; RS003 `identificador` | `str` | Campo de formulário `username`, rótulo Usuário | Mesmo nome de usuário da identidade customizada; não é CPF ou e-mail por inferência |
| RF001/RS003 `senha` | `str` transitória | Campo `password` | Recebido por POST; nunca gravado ou devolvido como texto legível |
| RF001/RS004 `usuarioId` | UUID sugerido na fonte | Chave do modelo configurado, obtida no servidor | O tipo físico depende de P002; não é campo editável da tela |
| RF001/RS003 `ativo` | `bool` | Atributo nativo `is_active` | Verificado no servidor; o cliente não ativa a própria conta |
| RS003 `hashSenha` | `str` | Representação codificada no campo nativo `password` do usuário | Não criar coluna adicional nem comparar hash manualmente |
| RS004 `identificadorSessao` | `str` | Identificador opaco mantido pelo mecanismo de sessão | Não mostrar em tela, URL, logs ou retorno de diagnóstico |
| RS004 `criadaEm`, `expiraEm`, `revogada` | `datetime`, `datetime`, `bool` | Conceitos de ciclo de sessão a conferir com backend/política | Não pressupor que sejam colunas nativas com esses nomes; não criar tabela duplicada |

Os mecanismos nativos de senha armazenam uma representação codificada e realizam a conferência apropriada. A extensão de `AbstractUser` mantém esses mecanismos; a escolha dos parâmetros e das políticas adicionais depende da versão e de P014. [Autenticação e modelo de usuário do Django](https://docs.djangoproject.com/en/stable/ref/contrib/auth/).

### Contrato dos campos do formulário

| Campo | Tipo e presença | Máscara, normalização e limites | Validação e retorno |
|---|---|---|---|
| `username` | `str`, obrigatório, origem no usuário | Texto sem máscara de documento; limite e validadores alinhados ao `USERNAME_FIELD` do modelo escolhido. Conferir normalização e remoção de espaços externos do form nativo na versão selecionada | Vazio ou composto só de espaços falha como obrigatório. Excesso do limite aprovado falha no servidor. Não converter automaticamente para minúsculas ou admitir identificador alternativo |
| `password` | `str` sensível, obrigatório, origem no usuário | Entrada visualmente ocultada; sem máscara de conteúdo. Preservar caracteres e espaços de uma senha não vazia, com `strip=False` | Proposta para a regra de obrigatório da fonte: recusar vazio/somente espaços sem aparar outra senha. Não reaplicar política de criação de senha no login. Não preencher novamente o campo na resposta HTML |
| `next` | `str` opcional; recebido por GET e, se usado, transportado no POST | Destino de navegação; sem significado de permissão. Sem tamanho numérico inventado; limite de transporte/validação depende da configuração aprovada | Validar novamente antes de cada redirecionamento. Ausente, inválido ou inadequado usa destino interno fixo. Campo oculto não é confiável |
| `csrfmiddlewaretoken` | Token de transporte do framework nos formulários POST | Gerado e conferido pelo mecanismo CSRF; não é campo de negócio | Falha de proteção impede a operação e não é tratada como senha incorreta |

`usuarioId`, perfil, `is_active`, `is_staff`, `is_superuser`, Supervisor e permissões não integram a entrada autenticadora. Valores extras com esses nomes não mudam o ator nem a autoridade. Senha, chave de sessão e token CSRF nunca compõem query string ou parâmetro de destino.

Comprimento mínimo/máximo de senha, política de criação e alteração, normalização do identificador, limites de requisição e medidas contra tentativas abusivas precisam de definição aplicável antes da implementação. Não assumir números por aparecerem em exemplos antigos. O form nativo distingue o tratamento de usuário e senha; a adaptação proposta deve preservar essa diferença. [Código oficial dos formulários de autenticação](https://github.com/django/django/blob/main/django/contrib/auth/forms.py).

## Organização candidata e responsabilidades

Os caminhos abaixo complementam a estrutura proposta da Spec 0001. São nomes de contrato para futura implementação, sem arquivos de aplicação criados agora.

| Local candidato | Conteúdo e responsabilidade | Restrição |
|---|---|---|
| `contas/forms.py` | `EntradaForm`, derivado de `AuthenticationForm`; campos e mensagens de entrada | Não salva perfil, inspeção ou autoridade; normaliza erros públicos de credenciais |
| `contas/views.py` | `EntrarView(View)`, `SairView(View)` e `AcessoView(View)` | Herança direta de `View`; mixins de acesso admitidos; sem consultas explícitas de negócio ao ORM |
| `contas/urls.py` | Namespace candidato `contas`, três nomes de rota abaixo | Não publicar rotas de funcionalidades futuras |
| `templates/contas/entrar.html` | Formulário de credenciais e mensagens | Campo de senha não repopulado; sem dados internos de erro |
| `templates/contas/acesso.html` | Destino mínimo para confirmar identidade reconhecida e oferecer saída | Sem painel, indicadores, lista de inspeções ou seleção de perfil antecipados |
| `contas/tests/` | Cenários futuros de formulário, HTTP e sessão | Ferramenta de testes conforme fundação aprovada; PostgreSQL isolado onde houver persistência |

O `AuthenticationForm` nativo recebe `request` e usa a autenticação do framework. Essa é a exceção de infraestrutura já admitida na arquitetura; não autoriza services a receber HTTP. A view valida o form, obtém seu usuário validado e chama `login(request, usuario)` ou `logout(request)`. Não criar um `AuthService` apenas para contornar essa exceção nem reimplementar o mecanismo de senha. [Uso da autenticação Django](https://docs.djangoproject.com/en/stable/topics/auth/default/).

Views próprias não serão subclasses de `LoginView`, `LogoutView` ou `FormView`, para respeitar a decisão de herança direta. Os componentes internos do Django e do Admin não precisam ser reescritos. Uma tela autenticada não realiza autorização de inspeções; o caso de uso de negócio continuará a verificar perfil, vínculo, situação e escopo nos services da Etapa 6 em diante.

### Persistência reutilizada

| Componente | Dados consumidos nesta spec | Limite estrutural |
|---|---|---|
| Usuário customizado da fundação | Chave aprovada, `username`, representação codificada de `password` e `is_active`; demais campos técnicos herdados não concedem perfil de negócio | Não criar segundo cadastro de identidade; referenciar o modelo configurado, sem importar uma classe de usuário padrão fixa |
| Sessão nativa em banco, se o ADR 0008 for aceito | Chave, conteúdo codificado e vencimento mantidos pelo framework; nomes nativos de referência `session_key`, `session_data`, `expire_date` | Conferir estrutura/migrações na versão escolhida; não criar uma entidade de sessão da aplicação nem persistir senha ou cópia de inspeção nela |
| Configuração e diagnóstico | Backend e opções aprovadas; contexto mínimo de falha operacional | Não são cadastros editáveis do produto; sem valor de segredo em tabelas de negócio ou registros de teste |

Datas de sessão são conceitos técnicos, distintos das datas oficiais de visita, emissão ou auditoria. Nenhuma chave estrangeira de fiscalização, tabela de aprovação ou vínculo com estabelecimento é introduzido pela autenticação.

## Contrato HTTP candidato

Respostas de erro são páginas HTML; esta spec não cria API JSON. Os códigos abaixo descrevem a resposta da aplicação, antes de eventuais falhas de transporte. Métodos de leitura não executam login, logout ou alteração de negócio.

| Rota e nome | Método e condição | Resultado proposto |
|---|---|---|
| `/conta/entrar/` — `contas:entrar` | GET anônimo | 200, formulário vazio, token CSRF e destino tratado como entrada não confiável |
| Mesma rota | POST anônimo, campos e credenciais válidos, conta ativa | Sessão estabelecida pelo Django; 302 para destino permitido ou `contas:acesso` |
| Mesma rota | POST anônimo com campo inválido ou credencial recusada | 200, formulário com erro; nenhuma nova sessão autenticada; senha não volta no HTML |
| Mesma rota | GET ou POST de usuário já autenticado e ativo | 302 para destino permitido; não autenticar outra conta nem trocar identidade silenciosamente |
| `/conta/sair/` — `contas:sair` | POST com proteção CSRF válida | Encerrar a sessão corrente no servidor; 302 para `contas:entrar`, sem `next` livre |
| Mesma rota | GET ou HEAD | 405, sem encerrar sessão; saída é formulário/botão POST, não link que altera estado |
| Mesma rota | POST válido já sem sessão autenticada | 302 para entrada, sem autenticar ninguém; repetição não cria efeito de negócio |
| `/conta/acesso/` — `contas:acesso` | GET de identidade válida e ativa | 200, página mínima protegida com nome de usuário e ação de saída |
| Mesma rota | GET sem identidade válida | 302 para entrada com destino interno validado; não renderizar conteúdo protegido |
| Rotas com POST | CSRF ausente/inválido | 403 pela proteção do framework, antes de executar a operação |

HEAD acompanha GET sem corpo nas rotas de entrada/acesso. OPTIONS pode responder metadados nativos sem executar ação. Demais métodos não previstos retornam 405 quando chegam ao despacho da view. Middleware de segurança, CSRF e verificação de acesso podem rejeitar ou redirecionar antes disso; não prometer 405 como substituto desses controles.

Proposta: usar 302 no sucesso de POST, com a navegação seguinte por GET. Não reenviar corpo de credenciais por 307/308. O destino mínimo não é o painel definitivo do sistema; a distribuição por perfil depende da Etapa 6 e da interface futura.

### Destino de retorno `next`

1. Tratar o valor recebido tanto no GET quanto no POST como não confiável. Proposta: no POST, usar o valor desse formulário; não aproveitar um GET anterior sem nova validação.
2. Aceitar apenas destino relativo interno ou URL de mesmo host permitido, com esquema admissível; em requisição segura, exigir HTTPS. A origem de comparação é o host validado por `ALLOWED_HOSTS`, obtido pelo framework, sem lista liberada por parâmetro do cliente.
3. Usar a validação nativa `url_has_allowed_host_and_scheme` e a construção de resposta/URI do framework. Rejeitar domínio externo, esquema indevido, destino que provoque ciclo entre entrada/saída e redução indevida de HTTPS para HTTP.
4. Na ausência ou recusa, usar o nome fixo `contas:acesso`. Não devolver URL suspeita como link clicável nem incluí-la em mensagem/log sem tratamento.
5. A rota de destino continua responsável por seu controle de acesso. Destino aceito não concede permissão sobre um estabelecimento, inspeção ou ação.

O helper nativo é parte da proteção; sozinho não prova codificação adequada da URI nem autorização do recurso de destino. [Validação de destinos no código oficial do Django](https://github.com/django/django/blob/main/django/utils/http.py).

## Telas e mensagens propostas

Não é criado novo protótipo visual nesta etapa. Os contratos abaixo orientarão o desenho e a implementação futuros, preservando a revisão de protótipos em P021.

| Tela ou estado | Conteúdo e interação | Validação observável |
|---|---|---|
| Entrada inicial | Título do sistema; campos Usuário e Senha; botão Entrar; rótulos associados aos campos | Uso por teclado, foco perceptível, leitura sem depender apenas de cor e disposição utilizável em celular/tablet |
| Erro obrigatório/formato | Erro próximo ao campo e resumo legível quando necessário; preservar usuário não sensível de forma escapada | Senha vazia na resposta; erro não atribui privilégio nem confirma existência da conta |
| Credencial recusada | “Não foi possível entrar com os dados informados.” | Mesma mensagem pública para usuário inexistente, senha incorreta e conta inativa |
| Entrada em processamento | Indicação de tentativa; prevenir múltiplos envios acidentais enquanto há resposta em curso | Botão desabilitado é apoio de interface; não é prova de persistência ou controle de abuso |
| Falha operacional | “Não foi possível confirmar o acesso agora. Tente novamente.” | Não classificar indisponibilidade do servidor como senha errada; não mostrar detalhes internos |
| Sessão ausente ou expirada | Solicitar autenticação antes de novo acesso protegido | Não informar por padrão o motivo interno ou revelar uma conta; dados já renderizados exigem política específica |
| Saída confirmada | Formulário de entrada e indicação simples de encerramento, se adotada | Confirmação somente após resposta do servidor; não basta apagar cookie na interface |
| Proteção CSRF recusada | Orientação legível para atualizar a página/retomar entrada com segurança | Não reaproveitar automaticamente o POST sensível nem mostrar token bruto |

Proposta de atributos: identificador com finalidade `username` e senha com finalidade `current-password`, respeitando o funcionamento do navegador. Não prometer controle sobre gerenciadores de senha do usuário. Recursos de mostrar senha, textos finais e critérios formais de acessibilidade deverão ser validados; não impor confirmação extra ou fluxo de recuperação não aprovado.

## Fluxos e condições

### Entrada válida

1. O usuário anônimo abre a entrada por HTTPS no ambiente operacional validado. O servidor apresenta formulário e proteção CSRF; `next` permanece não confiável.
2. O usuário informa nome e senha e envia POST. O servidor valida transporte, presença, limites aplicáveis e credenciais pelo mecanismo nativo.
3. Conta inexistente, credencial incorreta ou conta inativa não abrem sessão. O form apresenta a mensagem genérica proposta; a interface não repõe senha na resposta.
4. Com identidade válida e ativa, a view chama o login nativo. O mecanismo de sessão mantém a identidade; não recebe papel/autoridade do formulário.
5. O servidor valida o destino e responde com redirecionamento. A página protegida verifica novamente a identidade na requisição seguinte; retorno da função de login isoladamente não é confirmação de sessão persistida.
6. Se a resposta se perder, usar o tratamento de ambiguidade abaixo. Não afirmar sucesso ou falha de credenciais apenas por timeout.

### Acesso com sessão existente

1. O middleware lê a sessão e recupera a identidade pelo backend configurado. Proposta: backend nativo `ModelBackend`, que não admite conta inativa.
2. Sessão reconhecida e conta ativa permitem o destino mínimo. A verificação não se resume a um atributo `is_authenticated` isolado de qualquer validação de conta.
3. Ausência, expiração ou invalidação exigem nova entrada. Inativação ocorrida depois do login deve impedir o próximo acesso protegido; não desfaz uma requisição já autorizada e em execução.
4. Uma mudança de perfil/vínculo exige revalidação de autorização no caso de uso de negócio. Não copiar Supervisor ou permissões para o cookie como autoridade permanente.

### Encerramento

1. A ação Sair envia POST protegido para a rota correspondente. GET, pré-carregamento de link ou visita de robô não encerram sessão.
2. A view chama o logout nativo, que limpa a sessão corrente. Com o backend em banco proposto no ADR 0008, a sessão antiga deixa de ser reconhecida no servidor.
3. O servidor redireciona para entrada. Repetir uma requisição protegida com a chave anterior não recupera acesso. Repetir a saída válida, já sem identidade, continua sem autenticar ninguém.
4. Encerrar sessão corrente não promete encerrar todos os dispositivos. Troca de senha, revogação global, painel de sessões, autorizações de suporte e tratamento de requisições concorrentes dependem de P014.

## Sessão, cookies e expiração

Recomenda-se sessão Django no servidor com o backend de banco e PostgreSQL, conforme ADR 0008. O navegador mantém o identificador opaco; não transporta uma cópia de perfil, senha ou inspeção como fonte de autoridade. O backend e as migrações nativas serão configurados apenas na implementação autorizada, depois da validação da proposta.

O login nativo trata a renovação da chave para reduzir fixação de sessão; o logout limpa a sessão corrente. Backend de cookies assinados tem propriedades de revogação diferentes e não deve ser considerado equivalente para impedir a reutilização de uma cópia anterior após logout. [Sessões Django](https://docs.djangoproject.com/en/stable/topics/http/sessions/).

| Configuração ou controle | Contrato proposto | O que continua aberto |
|---|---|---|
| Backend | `django.contrib.sessions.backends.db`, no PostgreSQL aprovado para a aplicação | Aceite do ADR 0008 e preparação P001/P015 |
| HTTPS e cookies | Propor cookies de sessão/CSRF com `Secure` no ambiente HTTPS; sessão com `HttpOnly`; escopo restrito | Domínio, caminho, `SameSite`, origens confiáveis e proxy/TLS em P014/P015; conferir compatibilidade antes de aplicar |
| Duração | Expiração efetivamente aplicada no servidor; sessão expirada não autoriza novo acesso | Valores de `SESSION_COOKIE_AGE`, expiração ao fechar navegador e atualização por atividade; não assumir horas/minutos |
| Concorrência | Nenhum limite de aparelhos aprovado; testar o comportamento que vier a ser escolhido | Quantidade, substituição da sessão anterior e aviso ao usuário em P014 |
| Revogação | Logout da sessão corrente; recusa de conta inativa pelo backend candidato | Revogar todas as sessões, efeitos de alteração de senha/permissões e procedimentos administrativos em P014 |
| Cache | Propor `Cache-Control: no-store` em respostas sensíveis, inclusive entrada preenchida e página protegida | Conferência de navegador/proxy e comportamento em múltiplas abas, P019/P020 |
| Limpeza | Não persistir credenciais ou tokens em `localStorage`, `sessionStorage`, serviço offline ou cache próprio da aplicação | Política de dados de inspeção ainda abertos ao sair/expirar/trocar conta, P014/P020 |

Nomes de settings nesta tabela são referências técnicas, não arquivos configurados nem valores aceitos. Configurações relacionadas devem ser avaliadas em conjunto; `HttpOnly` não dispensa CSRF, e cabeçalhos de cache não garantem apagar uma página já exibida, a memória de outra aba ou o histórico de um aparelho compartilhado.

O ciclo de expiração é nativo do backend, mas a política de produto ainda precisa ser escolhida. A manutenção dos registros expirados, sua frequência e responsáveis operacionais dependem de P015/P017. Não criar campos `revogada` e `criadaEm` só para imitar a tabela de referência do RS004.

## Segurança da operação

Preservar os middlewares nativos de sessão, autenticação e CSRF. Login e logout são operações POST protegidas. O segredo CSRF pode mudar após login, portanto um formulário aberto antes dele pode precisar ser recarregado; falha de CSRF não deve disparar reenvio silencioso de credenciais. [Proteção CSRF do Django](https://docs.djangoproject.com/en/stable/ref/csrf/).

Normalizar a mensagem pública de autenticação recusada, inclusive a de conta inativa que componentes nativos possam distinguir. Não prometer igualdade absoluta de tempo de resposta; aproveitar as proteções nativas e avaliar limitação de tentativas em P014. Não implementar bloqueio permanente, captcha, armazenamento de IP ou contador de tentativa sem a política correspondente.

Usar mecanismos nativos para definir/conferir senha. Não aplicar uma função de hash própria, comparar senha com conteúdo do banco, devolver a representação codificada ou registrar senha em auditoria. O uso transitório da senha pelo form/framework não autoriza persistência legível.

Mensagens, URLs, logs e dumps de diagnóstico não incluem corpo integral do POST, cópia de cookie de sessão, token CSRF, senha, chave de configuração ou conexão. O transporte nativo necessário de CSRF no formulário/cookie e do identificador de sessão no cookie continua permitido; isso não autoriza exibi-los em mensagens ou reproduzi-los em registros. Contexto técnico mínimo, código de falha e correlação podem apoiar diagnóstico conforme P015/P017; coleta de identificador, IP, tentativas e eventos de acesso precisa de política explícita. Log de acesso não substitui auditoria oficial de inspeções.

A rota do Admin não serve como atalho de login do produto. Acesso técnico ao Admin continua sujeito aos controles nativos e à governança futura; não se registra automaticamente qualquer modelo de inspeção para edição direta. Não confundir superusuário técnico com autorização para corrigir, cancelar ou aprovar.

## Perda de comunicação e confirmação

O sistema permanece somente online. RF011 e DC018/DC019 continuam preservando o conteúdo da página aberta, bloqueando temporariamente ações dependentes do servidor e distinguindo pendência de confirmação. A autenticação tem dados sensíveis e uma resposta perdida pode ocorrer depois de a sessão ter sido gravada; esse caso exige decisão específica, sem reclassificar timeout como credencial inválida.

**Proposta a validar em P014/P020:** ao recuperar comunicação, consultar a condição de acesso por uma requisição de leitura à página protegida antes de repetir credenciais. Se a sessão já estiver reconhecida, continuar com ela; se não estiver, permitir nova tentativa explícita. Não reenviar automaticamente a senha em segundo plano. A técnica de interação no navegador ainda não foi escolhida.

| Situação | Comportamento proposto | Limite |
|---|---|---|
| Falha antes de enviar entrada | Indicar falta de comunicação; manter os dados apenas na página ainda aberta; reabilitar tentativa depois da recuperação | Não criar cópia persistente da senha ou garantir recuperação após recarga |
| POST de entrada enviado, resposta ausente | Exibir “Tentativa não confirmada”; não afirmar acesso nem senha incorreta | O servidor pode ter criado a sessão; o navegador pode ou não ter recebido seu cookie |
| Comunicação restabelecida | Verificar acesso sem senha; continuar se já autenticado ou permitir nova tentativa explícita | Não tratar disponibilidade de internet ou resposta 200 da tela de login como prova de sessão autenticada |
| Resposta de saída ausente | Indicar encerramento não confirmado; conferir acesso e, se necessário, repetir POST válido de saída | Não afirmar logout só porque a interface apagou seus controles |
| Página fechada/recarregada | Solicitar os dados necessários novamente, conforme condição real da sessão | Nenhuma garantia de restaurar campo de senha ou dados não confirmados |
| Outra aba com formulário antigo | Tratar recusa de CSRF/sessão com orientação de retomada | Não reenviar POST de inspeção nem descartar dados pendentes por regra inventada aqui |

Essa proposta não aprova uma exceção definitiva à política geral de retentativa. Seu tratamento de credenciais precisa ser aceito antes da implementação correspondente; o registro de P020 permanece aberto. Recuperação de respostas/evidências/termos continua exigindo controle próprio de repetição nas specs funcionais, sem ser resolvida por login ou redirecionamento.

A senha não é repopulada em HTML retornado pelo servidor. Preservar um campo ainda presente na página sem resposta não significa guardá-lo em armazenamento persistente da aplicação. Saída, expiração ou troca de conta enquanto existem dados de inspeção em outra tela exigem política de proteção/limpeza a definir; não se presume salvar, descartar ou transferir esses dados para outro usuário.

## Falhas e consistência

| Condição | Resposta observável proposta | Efeito e diagnóstico |
|---|---|---|
| Campo obrigatório/limite recusado | 200 com erro no formulário | Não tentar login com dados inválidos; não refletir senha |
| Conta inexistente, inativa ou senha errada | 200 com mesma mensagem pública genérica | Sem nova sessão autenticada; não distinguir a conta na interface |
| CSRF inválido | 403, orientação segura de retomada | Sem login/logout; não revelar token nem repetir o corpo automaticamente |
| Destino de retorno inválido | Sucesso usa destino fixo interno, se credenciais forem válidas | Não executar redirecionamento externo nem conceder acesso por URL |
| Sessão ausente/expirada/revogada | Redirecionar entrada nas páginas HTML protegidas | Não renderizar conteúdo protegido; não simular estado de inspeção salva |
| Banco/autenticação indisponível | 503 quando a falha operacional for reconhecida e tratada; mensagem genérica | Sem transformar indisponibilidade em erro de senha; contexto técnico restrito |
| Falha ao persistir a sessão | Não apresentar confirmação de autenticação só porque a view chamou login | Verificar o ciclo inteiro até middleware/resposta e o acesso seguinte |
| Falha inesperada | 500 sanitizado conforme fundação | Sem stack trace, configuração ou credenciais públicas |
| Método não aceito | 405 se o despacho da view for alcançado | Sem efeito; controles anteriores de segurança/acesso continuam válidos |

A gravação de sessão pode ocorrer no middleware, depois da execução da view. O contrato de falhas precisa cobrir essa fronteira na integração; um teste isolado de função não comprova o resultado observado pelo navegador. O mapeamento de indisponibilidade deve funcionar com os templates de erro da fundação e não depender de consultar o banco para renderizar a falha.

Não prometer transação única entre toda atualização auxiliar nativa, como `last_login`, gravação de sessão e entrega de cookie. Nenhum desses eventos é uma alteração oficial de inspeção. Se o acesso seguinte não for reconhecido, a interface continua sem confirmação, ainda que uma atualização auxiliar tenha ocorrido.

## Relação local com os requisitos

Esta tabela delimita a contribuição da autenticação. A [matriz completa de fontes, RF/RNF/RS e validação](../matriz-rastreabilidade.md) foi elaborada na Etapa 6 e continua Proposta. Documento redigido não significa requisito implementado.

| Origem ou requisito | Parte detalhada aqui | Validação futura relacionada |
|---|---|---|
| F003/RF001; F008/DC007 | Entrada por usuário/senha, conta ativa e saída; base Django confirmada | AU01 a AU08, AU11/AU12 e AU19 a AU22 |
| F003/RS003 | Credenciais transitórias, validação nativa e mensagem genérica | AU04 a AU08, AU23 e AU29 |
| F003/RS004 | Sessão reconhecida, expiração, logout e impossibilidade de reutilizar a sessão encerrada | AU15 a AU22, AU24, AU26/AU27; backend/políticas a validar |
| RF002; RS001/RS002 | Identidade como pré-requisito e distinção entre autenticação e autorização | AU28; contratos de perfil, vínculo e supervisão estão na Spec 0003, elaborada na Etapa 6 |
| RS005, RS009 e RS011 | Transporte/configuração, validação de entrada, CSRF e proteção de segredos | AU02/AU03, AU09/AU10, AU13/AU14 e AU29; implantação ainda pendente |
| RS012; RNF10 | Falha sanitizada e diagnóstico sem dados sensíveis | AU23/AU24 e AU29; retenção/coleta em P015/P017 |
| RNF01, RNF07 e RNF08 | Contratos de tela para navegador, celular/tablet e acesso legível | AU30; homologação P019 ainda necessária |
| RNF04, RNF09 e RNF12 | Uso de PostgreSQL, componentes nativos e respeito às fronteiras | AU19, AU24 e AU32; fundação validada separadamente |
| RF011, RNF14 e RS014 | Interface de autenticação diante de comunicação ambígua, sem persistência de senha | AU25 a AU27, condicionados a P014/P020; não atende ao fluxo completo de inspeção |

RS013 não é satisfeito apenas pelo redirecionamento ou pela possibilidade de repetir logout: deduplicação dos atos de inspeção/arquivo/PDF continua no escopo funcional correspondente. O controle de dados abertos em aparelho compartilhado permanece parcialmente aberto em RS014.

## Critérios de aceite da implementação futura

Todos os cenários abaixo estão **planejados, não executados**. Usar contas/dados fictícios, proteção CSRF efetiva e PostgreSQL isolado quando houver persistência. Registrar versões, configuração sem segredos, pré-condição, ação, resposta HTTP, estado da sessão e acesso seguinte quando aplicáveis. A simulação deve observar o comportamento real, não apenas comparar textos constantes.

| ID | Pré-condição e ação | Resultado verificável |
|---|---|---|
| AU01 | Anônimo abre a rota de entrada | 200, campos rotulados, POST protegido e nenhuma credencial/token bruto em URL |
| AU02 | Enviar campos ausentes, vazios e somente espaços | Erros de obrigatório conforme contrato, sem autenticar e sem refletir senha; senha não vazia não é aparada |
| AU03 | Enviar usuário acima do limite do modelo aprovado, inclusive sem validação do navegador | Rejeição no servidor, sem erro interno ou truncamento silencioso |
| AU04 | Conta ativa e credencial correta enviam POST válido, com chave prévia de sessão anônima quando aplicável | Sessão reconhecida no acesso seguinte e renovação da chave conferida; destino seguro, sem senha na resposta ou URL |
| AU05 | Conta existente envia senha incorreta | Sem nova sessão autenticada e mensagem genérica de recusa |
| AU06 | Enviar usuário inexistente e comparar com AU05 | Mesmo conteúdo público de recusa, sem indicação da existência da conta |
| AU07 | Conta inativa envia credencial correta | Acesso recusado com a mesma mensagem pública de AU05/AU06 |
| AU08 | Conta de teste com senha não vazia contendo espaços externos/internos | Somente a senha exata autentica; a adaptação do form não modifica os caracteres |
| AU09 | Login válido recebe `next` interno permitido | Redirecionamento adequado; acesso do destino é verificado pela própria rota |
| AU10 | Repetir com domínio externo, esquema impróprio, downgrade em HTTPS e ciclo entrada/saída | Destino recusado e fallback interno; sem URL suspeita no corpo, credenciais ou concessão de acesso |
| AU11 | Usuário ativo autenticado abre GET de entrada | Redireciona com a identidade atual, sem abrir outra autenticação |
| AU12 | Usuário autenticado envia POST com credenciais de outra conta | Identidade atual preservada; não há troca silenciosa de conta |
| AU13 | Anônimo envia login sem CSRF ou com token inválido | 403, sem criar sessão autenticada; erro legível sem segredo |
| AU14 | Abrir form em outra aba antes do login e submetê-lo depois da mudança de token | Recusa de CSRF quando aplicável e retomada segura; sem reenvio automático de senha |
| AU15 | Anônimo solicita diretamente a página protegida | Redireciona entrada sem conteúdo privado; `next` de retorno é validado |
| AU16 | Conta ativa com sessão válida abre o destino mínimo | 200 apenas com conteúdo previsto; nenhum painel ou privilégio de negócio antecipado |
| AU17 | Inativar conta autenticada pelo mecanismo de teste e fazer nova requisição protegida | Conta deixa de obter acesso, sem depender de o usuário clicar Sair |
| AU18 | Usar sessão ausente, expirada em configuração controlada de teste ou não reconhecida | Nova autenticação exigida; configuração de teste não se torna prazo do produto |
| AU19 | Fazer logout POST e repetir acesso com uma cópia da chave anterior | Sessão antiga não autoriza no servidor; não basta observar remoção do cookie |
| AU20 | Fazer GET/HEAD de saída com sessão válida | 405, nenhum encerramento; requisição protegida posterior ainda reconhece a sessão |
| AU21 | Fazer POST de saída com CSRF inválido | 403, sessão não encerrada por esse POST |
| AU22 | Após saída, repetir POST com CSRF atualmente válido, já sem usuário | Redireciona entrada, sem autenticação ou alteração de negócio |
| AU23 | Simular indisponibilidade do banco durante autenticação | Falha operacional sanitizada, 503 quando mapeada; não informar senha errada nem expor conexão |
| AU24 | Simular falha na persistência de sessão após a view | Nenhuma confirmação fictícia; verificar middleware, resposta e acesso seguinte, incluindo atualização auxiliar eventualmente ocorrida |
| AU25 | Perder resposta de login antes/depois da entrega do cookie e reconectar | Proposta P014/P020: conferir acesso por leitura; não reenviar senha silenciosamente nem afirmar falha de credenciais |
| AU26 | Perder resposta de logout e reconectar | Conferência/repetição segura confirma a condição real; chave encerrada não recupera acesso |
| AU27 | Usar Voltar e duas abas após logout/expiração | Novas requisições protegidas são recusadas; conferir cabeçalhos e registrar limites de conteúdo já exibido/limpeza conforme política aprovada |
| AU28 | Enviar campos extras de identidade, perfil, staff, superusuário ou Supervisor | Nenhum campo concede identidade/autoridade; autenticar não atribui aprovação ou vínculo |
| AU29 | Provocar erros de entrada, CSRF, sessão e banco; inspecionar HTML, URL e registros autorizados | Nenhuma senha/hash/segredo ou cópia indevida de chave/token; CSRF somente no transporte nativo necessário, sem exposição em mensagens/URL/logs ou detalhes internos |
| AU30 | Executar entrada/erro/saída com teclado, leitura assistida e dispositivos homologados | Rótulos e foco utilizáveis, estados compreensíveis e campos/ações acessíveis nos critérios aprovados em P019 |
| AU31 | Exercitar métodos previstos e não previstos, HEAD/OPTIONS e rejeição anterior por middleware | Sem efeitos em leitura; respostas compatíveis com a ordem dos controles documentada |
| AU32 | Revisar entrega futura e migrações efetivas | Usuário/ORM/sessão nativos e views diretas respeitados; sem tabela de sessão duplicada, serviços com HTTP ou modelos de negócio antecipados |

- [ ] Contratos novos e decisões bloqueantes da parte implementada revisados, com origem registrada.
- [ ] Cenários aplicáveis executados com evidências e falhas/limitações reais documentadas.
- [ ] Políticas de sessão, credenciais, tentativa e recuperação pertinentes definidas antes da operação.
- [ ] Nenhuma função de negócio ou etapa posterior marcada como entregue por existir login.

## Questões de revisão e continuidade

1. Validar o backend de sessões no servidor proposto no ADR 0008 e os nomes/rotas/forms candidatos, preservando a base já confirmada.
2. Resolver P001 e a parte estrutural de P002 antes de criar ambiente/modelo/migração. Escolher políticas de P014 e as proteções operacionais aplicáveis; não fechar a pendência inteira pela aprovação do form.
3. Validar em P014/P020 o tratamento de resposta perdida sem reenvio silencioso de senha e a proteção de dados ainda abertos ao sair/expirar/trocar conta.
4. Revisar esta spec. A [Spec 0003 de acesso](0003-acesso-vinculos-supervisao.md) e a [matriz completa](../matriz-rastreabilidade.md) foram elaboradas na Etapa 6 e permanecem Propostas, sem implementação. As Etapas 7 e 8 foram elaboradas para revisão; [skills](../revisao-skills-tecnicas.md), [revisão final](../revisao-final-fundacao.md) e [estado](../state.md) registram a continuidade, sem iniciar implementação.

O [estado](../state.md), as [etapas](../etapas.md) e o [acompanhamento no Trello](../acompanhamento-trello.md) registram a entrega. O resultado desta etapa é documental e permanece Proposto.
