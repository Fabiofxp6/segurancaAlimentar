# Sistema de Avaliação de Segurança Alimentar

Sistema web para organizar inspeções de segurança alimentar: checklist, respostas, evidências, avaliação, termos e alterações autorizadas com histórico. A Fiscalização executa a inspeção; o Estabelecimento envia documentação própria e consulta resultados finais liberados; o Administrador atua na gestão conforme suas permissões.

## Situação atual

As oito etapas de documentação foram elaboradas e conferidas para revisão do usuário. O catálogo contém **28 RF, 14 RNF e 16 RS**, preservando os 58 IDs. Há treze specs e oito ADRs, além da matriz, das skills e dos perfis de agentes.

A I01 entregou a fundação Django local com configuração por perfil, PostgreSQL isolado e primeira migração de `contas.Usuario`. Os resultados estão no [registro da I01](docs/entrega-i01.md). A [I02](docs/entrega-i02.md) entregou entrada, saída e acesso protegido local, com sessão no PostgreSQL conforme o ADR 0008. A [I03](docs/entrega-i03.md) entrega cadastros, perfis, vínculos e o procedimento de concessão de Administrador. A [I04](docs/entrega-i04.md) entrega rascunhos e versões imutáveis de demonstração. A [I05](docs/entrega-i05.md) entrega atribuição, início, equipes e supervisão por ação em ambiente de demonstração. A [I06](docs/entrega-i06.md) entrega preenchimento em campo com evidências privadas e recuperação de envio. A [I07](docs/entrega-i07.md) entrega envio e consulta de documentos por unidade. A [I08](docs/entrega-i08.md) entrega cancelamento autorizado e auditoria por inspeção. A [I09](docs/entrega-i09.md) entrega pontuação ponderada, classificação e conclusão da inspeção em demonstração. A [I10](docs/entrega-i10.md) entrega emissão do termo em PDF e liberação ao estabelecimento. A [I11](docs/entrega-i11.md) entrega correção em revisão, recálculo e retificador. A [I12](docs/entrega-i12.md) entrega lista filtrada e painel administrativo de demonstração. O [estado](docs/state.md) informa a retomada e as [pendências](docs/pendencias.md) delimitam as decisões que faltam.

## Base confirmada

| Tema | Escolha ou regra |
|---|---|
| Tecnologias | Python 3.14, Django 5.2 LTS, PostgreSQL 17 e Psycopg 3.3. uv e Docker Compose no ambiente local. |
| Interface e operação | Navegador em tablets/celulares, hospedagem remota e operação somente online |
| Arquitetura | MVT/Django Templates; views próprias diretamente de View; regra/ORM explícito em services sem HTTP, com exceções nativas documentadas |
| Identidade | Usuário customizado AbstractUser, nome de usuário/senha e sessão Django; políticas complementares abertas |
| Perfis | Fiscalização, Administrador e Estabelecimento; Supervisor é fiscal designado por ação, sem quarto perfil |
| Início | Administrador pode atribuir inspeção e fiscal pode iniciá-la diretamente, sem supervisão automática |
| Confirmação | Queda de comunicação preserva a página aberta, bloqueia ações dependentes do servidor e permite recuperação sem salvamento fictício ou efeito duplicado |
| Revisão | Correção após conclusão e cancelamento em andamento exigem autorização, justificativa e história; checklist/regras, resultados e termos anteriores são preservados |
| Estabelecimento | Consulta apenas próprios envios e resultados/documentos finais liberados; anexo não altera nota automaticamente |

Os contratos completos e as decisões abertas estão nos documentos abaixo. Fórmula, limites, tipos físicos, autoridades e prazos ilustrativos não são aprovados por aparecerem em uma tabela ou protótipo.

## Guia de leitura

| Documento | Uso |
|---|---|
| [AGENTS.md](AGENTS.md) | Orientações de trabalho e entrada comum para os agentes |
| [Estado](docs/state.md) e [etapas](docs/etapas.md) | Retomada e histórico das oito entregas |
| [Decisões confirmadas](docs/decisoes-confirmadas.md) e [pendências](docs/pendencias.md) | O que foi escolhido e o que ainda depende de resposta |
| [PRD 0001](docs/prd/0001-sistema-avaliacao-seguranca-alimentar.md) | Produto, dados, regras, manutenção e critérios dos 58 requisitos |
| [Arquitetura e ADRs](docs/arquitetura.md) | Responsabilidades, limites e razões das escolhas/propostas |
| [Spec 0001 — fundação](docs/specs/0001-fundacao-tecnica.md) | Estrutura local, configuração, PostgreSQL e identidade inicial |
| [Spec 0002 — autenticação](docs/specs/0002-autenticacao.md) | Entrada, saída, sessão, campos, falhas e cenários de aceite |
| [Spec 0003 — acesso](docs/specs/0003-acesso-vinculos-supervisao.md) | Vínculos, papéis, supervisão, revogação e 36 cenários AC futuros |
| [Spec 0004 — estabelecimentos](docs/specs/0004-cadastro-estabelecimentos.md) | Cadastro, consulta, edição e inativação de estabelecimentos |
| [Spec 0005 — checklist e versões](docs/specs/0005-checklist-e-versoes.md) | Rascunho, itens e publicação de demonstração |
| [Spec 0006 — início, equipe e supervisão](docs/specs/0006-inicio-equipe-e-supervisao.md) | Atribuição, início com versão fixa e designações por ação |
| [Spec 0007 — campo e reenvio](docs/specs/0007-campo-evidencias-e-reenvio.md) | Respostas por item, evidências privadas e confirmação do servidor |
| [Spec 0008 — documentos do estabelecimento](docs/specs/0008-documentos-do-estabelecimento.md) | Janela, autorização por unidade e recebimento de documentos |
| [Spec 0009 — cancelamento e auditoria](docs/specs/0009-cancelamento-e-auditoria.md) | Pedido justificado, decisão por ação, efetivação e trilha por inspeção |
| [Spec 0010 — pontuação e conclusão](docs/specs/0010-pontuacao-e-conclusao.md) | Regra de demonstração, validações, conclusão e resultado interno |
| [Spec 0011 — termo e liberação](docs/specs/0011-termo-e-liberacao.md) | Emissão, versão, auditoria e download por unidade |
| [Spec 0012 — correção e retificação](docs/specs/0012-correcao-e-retificacao.md) | Pedido, decisão, aplicação, revisão e nova liberação |
| [Spec 0013 — consultas e indicadores](docs/specs/0013-consultas-e-indicadores.md) | Escopo da lista, filtros, paginação e métricas por versão |
| [Matriz de rastreabilidade](docs/matriz-rastreabilidade.md) | Fontes, relações e cobertura documental das 58 entradas; 58 validações VR futuras |
| [Skills e agentes](.agents/README.md) | Onze skills locais e seis perfis, com escopo de uso |
| [Revisão das skills](docs/revisao-skills-tecnicas.md) | Conferência integrada de Python, Django e segurança |
| [Revisão final](docs/revisao-final-fundacao.md) | Coerência do conjunto, verificações e limites de prontidão |
| [Fontes](docs/referencias/README.md) | Ata, PDFs/DOCX, decisões, análise de referência e protótipo, com procedência |
| [Acompanhamento no Trello](docs/acompanhamento-trello.md) | Regra contínua de atualização do quadro e links das atividades |

## Preparo local

Abra o Docker Desktop. Na raiz do projeto, execute `uv sync --locked`. O `uv.lock` contém as dependências resolvidas e `.python-version` identifica o CPython 3.14.10 usado na validação. Se o uv instalado ainda não oferecer essa versão, `uvx --from uv uv python install 3.14.10` permite instalá-la com a distribuição atual do uv.

Use [example.env](example.env) como referência para `.env.development` e `.env.test`. Crie apenas os arquivos que estiverem faltando. Para cada perfil, gere `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD` e `POSTGRES_ADMIN_PASSWORD` próprios, substituindo os exemplos por valores locais. Você pode gerar cada valor com `uv run --locked --no-env-file python -c "import secrets; print(secrets.token_hex(32))"`. O Django e o Compose recebem o arquivo selecionado em cada comando.

| Variável | `.env.development` | `.env.test` |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.development` | `config.settings.test` |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | `localhost,127.0.0.1,testserver` |
| `POSTGRES_DB` | `seguranca_alimentar_dev` | `seguranca_alimentar_test` |
| `POSTGRES_USER` | `seguranca_dev` | `seguranca_test` |
| `POSTGRES_PORT` | `55434` | `55433` |

Os dois perfis usam `POSTGRES_HOST=127.0.0.1`. Execute os comandos em um terminal livre de variáveis `DJANGO_*` e `POSTGRES_*` exportadas por outro projeto. Use os nomes de projeto Compose abaixo para separar contêineres e volumes.

```sh
docker compose --env-file .env.development -p seguranca-alimentar-i01-dev up -d --wait
uv run --locked --env-file .env.development python manage.py migrate
uv run --locked --env-file .env.development python manage.py check
uv run --locked --env-file .env.development python manage.py runserver
```

Abra [a página de entrada](http://127.0.0.1:8000/conta/entrar/). Para experimentar com uma conta fictícia em um banco de desenvolvimento novo, abra outro terminal na raiz do projeto e execute `uv run --locked --env-file .env.development python manage.py shell`. No console interativo, crie uma conta comum com uma senha escolhida por você.

```python
from getpass import getpass
from django.contrib.auth import get_user_model

get_user_model().objects.create_user(
    username="usuario-local",
    password=getpass("Senha local: "),
)
```

```sh
docker compose --env-file .env.test -p seguranca-alimentar-i01-test up -d --wait
uv run --locked --env-file .env.test python manage.py test --noinput
uv run --locked --env-file .env.development python manage.py migrate --check
uv run --locked --env-file .env.development python manage.py makemigrations --check --dry-run
```

### Demonstrar a gestão no ambiente local

Depois de aplicar as migrações, abra o shell com o perfil `.env.development` descrito acima. Em um banco de desenvolvimento com dados fictícios, é possível criar uma conta exclusiva para experimentar as telas. Substitua o nome sugerido caso já exista.

```python
from getpass import getpass
from contas.models import Usuario

Usuario.objects.create_user(
    username="administrador-demonstracao",
    password=getpass("Senha local de demonstração: "),
)
```

Em outro terminal, a equipe técnica pode conceder o perfil à conta de demonstração e registrar a operação.

```sh
uv run --locked --env-file .env.development python manage.py provisionar_administrador administrador-demonstracao
```

Entre com a conta de demonstração e abra **Gerir usuários** ou **Gerir estabelecimentos**. Para testar um usuário de Estabelecimento, cadastre a conta e uma unidade fictícia, escolha **Gerir vínculo** no cadastro da conta e selecione a unidade. Defina uma senha fictícia com o comando interativo e, em seguida, ative a conta pela tela de gestão.

```sh
uv run --locked --env-file .env.development python manage.py changepassword nome-de-usuario-ficticio
```

A conta poderá abrir **Meu estabelecimento** após entrar. Para confirmar a revogação, encerre o vínculo na gestão e recarregue a página da unidade na sessão do Estabelecimento. O canal de entrega de credenciais reais segue em P014.

O Django cria e remove seu banco descartável na instância de teste. Para pausar um dos bancos Docker, use o mesmo arquivo e nome de projeto do `up` com o comando `stop`. O perfil de produção seleciona configuração externa e rejeita debug ativo. A implantação e suas políticas fazem parte do recorte de operação.

### Demonstrar o checklist no ambiente local

Aplique as migrações e entre como Administrador de demonstração. Na área de acesso, abra **Gerir checklists**. Crie um checklist fictício e use **Adicionar item** para informar enunciado, ordem e uma opção por linha. Se desejar, registre peso e obrigatoriedade.

Use **Publicar versão de demonstração**. Depois, volte ao rascunho, altere uma regra, salve e publique novamente. Abra a versão anterior pela lista de versões para conferir o conteúdo preservado.

### Demonstrar inspeções no ambiente local

Aplique as migrações, prepare um estabelecimento fictício, publique um checklist de demonstração e cadastre fiscais fictícios conforme os passos anteriores. Na área de acesso, abra **Inspeções**. Como Administrador, atribua uma inspeção e selecione os fiscais. Para agrupar, escolha a mesma ação na atribuição seguinte. No detalhe, abra **Gerir supervisão da ação** para selecionar ou retirar supervisores.

Entre como fiscal responsável e inicie a inspeção atribuída, ou use **Iniciar nova inspeção** para começar diretamente. Selecione um checklist publicado. O detalhe mostra a versão persistida e sua origem. O fluxo usa o ambiente de demonstração.

### Demonstrar preenchimento e evidências

Atualize as dependências com `uv sync --locked` e aplique as migrações do perfil de desenvolvimento. Entre como fiscal da equipe e abra uma inspeção de demonstração em andamento. No detalhe, abra **Preencher checklist**, selecione um item e salve a resposta. Depois envie uma foto JPEG ou PNG fictícia, de até 5 MiB, vinculada ao item ou à irregularidade confirmada.

Para simular uma queda, mantenha a tela aberta. O formulário conserva os dados. O botão de envio é liberado após a recuperação da comunicação, e um envio já solicitado aguarda a confirmação do servidor.

### Demonstrar documentos do estabelecimento

Atualize as dependências e aplique as migrações como descrito no preparo local. Vincule ao menos uma conta de demonstração à unidade e atribua uma inspeção. No acesso da conta do estabelecimento, abra **Documentos do estabelecimento**, selecione a inspeção e envie um PDF, JPEG ou PNG fictício de até 5 MiB. Um PDF deve ter de 1 a 50 páginas e abrir sem senha.

Na tela da inspeção, o fiscal da equipe pode abrir **Documentos recebidos do estabelecimento**. As contas ativas da mesma unidade também podem consultar e baixar os documentos recebidos.

### Demonstrar o cancelamento

Aplique as migrações e prepare uma inspeção em andamento com dois fiscais fictícios na ação. Como Administrador, designe um deles como supervisor. Entre como o outro fiscal, abra o detalhe da inspeção e acesse **Pedidos de cancelamento**. Envie a justificativa e confira o checklist em leitura durante a pendência.

Entre como supervisor e acesse **Pedidos de cancelamento** na lista de inspeções. Abra o pedido, informe o motivo e aprove. No detalhe da inspeção, confira o estado **Cancelada** e abra **Ver auditoria da inspeção** para consultar solicitação, decisão e efetivação. Para testar a alternativa administrativa, prepare outro pedido sem supervisor elegível diferente do solicitante.

### Demonstrar pontuação e conclusão

Aplique as migrações e publique um checklist fictício com dois itens obrigatórios, opções Sim, Não e Não se aplica e pesos 4 e 1. Abra uma inspeção com essa versão. Como fiscal da equipe, confirme Sim no primeiro item e Não no segundo.

No checklist ou no detalhe, abra **Revisar para concluir**. Confira as respostas confirmadas e use **Concluir inspeção**. Após a confirmação, o resultado interno deve mostrar **80,00% — Satisfatória**. Abra **Ver auditoria da inspeção** no detalhe para conferir o evento. [Regras e limites](docs/specs/0010-pontuacao-e-conclusao.md)

### Demonstrar emissão e liberação

Atualize as dependências com `uv sync --locked` e aplique as migrações. Conclua uma inspeção fictícia. Como fiscal da equipe ou Administrador, abra **Termo e liberação**, clique em **Emitir termo em PDF** e confira o arquivo.

Como Administrador ou supervisor ativo da ação, abra **Termos emitidos** e use **Liberar ao estabelecimento**. Entre com uma conta vinculada à unidade da inspeção. Em **Resultados liberados**, abra o resultado e baixe a versão emitida. [Spec 0011](docs/specs/0011-termo-e-liberacao.md)

### Demonstrar correção e retificação

Aplique as migrações e use uma inspeção fictícia concluída com termo já liberado. Como fiscal da equipe, abra **Correções e revisões**, escolha um item e envie a alteração proposta com a justificativa. Como outro supervisor ou Administrador na ausência de outro supervisor elegível, abra **Pedidos de correção** e decida com motivo.

Como fiscal solicitante ou Administrador, abra o pedido aprovado e use **Aplicar correção aprovada**. Compare os resultados e confira o termo retificador em **Termo e liberação** quando a alteração afetar o PDF. Libere o novo termo com uma conta autorizada e confira as duas versões no portal do estabelecimento. [Spec 0012](docs/specs/0012-correcao-e-retificacao.md)

### Demonstrar consultas e indicadores

Abra **Inspeções** como Administrador ou fiscal da equipe. Combine os filtros de situação, estabelecimento, fiscal e datas de criação. Use **Próxima** quando houver mais de 25 registros. A lista conserva os filtros e apresenta o total autorizado.

Como Administrador, abra **Indicadores de inspeção** a partir da lista. Use inspeções fictícias concluídas com versões de checklist diferentes. Confira os totais e as médias por versão. Se houver correção aprovada e aplicada, confira a nota e a descrição de irregularidade na revisão mais recente. [Spec 0013](docs/specs/0013-consultas-e-indicadores.md)

## Uso das ferramentas de apoio

As respostas da conversa seguem a preferência de concisão Caveman, enquanto os documentos mantêm o detalhe solicitado. Graphify teve uma tentativa de extração sem retorno completo; o [mapa permanece pendente](docs/registro-graphify.md). Não há economia de tokens ou grafo pronto comprovados. Os perfis TOML foram conferidos, sem comprovação de execução/carregamento automático.

A próxima atividade deve ser solicitada e delimitada pelo usuário: revisar/aprovar documentos, responder decisões ou iniciar um recorte de implementação. A conclusão da Etapa 8 não começa uma nova fase automaticamente.
