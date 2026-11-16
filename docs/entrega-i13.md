# I13 — Preparação da homologação e do piloto

**Situação em 16/11/2026.** I13 concluída no escopo acadêmico local com dados fictícios. A homologação remota e a escolha de hospedagem ficam para uma fase futura. [DC037](decisoes-confirmadas.md#dc037-demonstração-acadêmica-local)

**Base ensaiada.** Commit `0885769d5fbfe63a2bf76656a0879a443e2bba74`, com as entregas I01 a I12, Python 3.14, Django 5.2 e PostgreSQL 17. O ensaio utilizou uma base criada para a execução, um navegador Chromium com larguras de 360 e 820 px e HTTPS local. O PostgreSQL testado guarda os bytes dos anexos e dos termos de demonstração.

## Evidências locais

| Verificação | Resultado observado |
|---|---|
| Django e migrações | `manage.py check` passou. `makemigrations --check --dry-run` confirmou que os modelos correspondem às migrações. Os 116 testes passaram no PostgreSQL. |
| Navegação e acesso | Entrada por teclado e uso do fluxo em 360 e 820 px. Fiscal, Supervisor designado, Administrador e Estabelecimento passaram pelos acessos previstos. Uma conta de outra unidade recebeu 404 para os termos protegidos. O painel administrativo recusou o Fiscal. |
| Campo, documentos e conexão | O Estabelecimento enviou um PDF e o Fiscal enviou uma foto. A perda simulada da resposta após a gravação manteve o texto na tela. A retentativa reutilizou o envio e o banco ficou com um único recibo da resposta. |
| Resultado, PDFs e correção | A inspeção concluiu com 80%. O termo só ficou disponível ao Estabelecimento após liberação. A correção aprovada gerou revisão com 0% e termo retificador. O retificador exigiu liberação própria. Após essa liberação, o termo original continuou disponível, com os mesmos bytes. |
| Cancelamento e consulta | Em outra inspeção da mesma ação, o pedido passou pela decisão do Supervisor e a situação final ficou cancelada. A consulta administrativa exibiu os dados de demonstração. |
| HTTPS e logs | A requisição de teste validou o certificado local e o host permitido. O Chromium aceitou esse certificado de teste. Foram verificados cookies seguros e rejeição de host não cadastrado. Na amostra de logs HTTP/CSRF, as recusas registraram status sem credenciais, trecho do formulário ou caminho da inspeção. |
| Backup e restauração | `pg_dump` gerou um arquivo de 161.355 bytes em 0,24 s. `pg_restore` restaurou em um banco separado em 0,18 s. Conferimos estado, revisões de pontuação, auditoria e os bytes da foto, do documento e dos dois termos por SHA-256. As sessões anteriores não foram restauradas. O acesso autorizado aos termos e o isolamento por unidade foram verificados novamente. |

Os tempos descrevem somente a base fictícia. O ensaio em Chromium simulou as larguras de tela. Dispositivos físicos, Safari, câmera e comportamento em rede móvel ficam para a homologação. A amostra de logs cobriu o Django local. O proxy e os registros do provedor precisam de verificação no ambiente escolhido.

O `manage.py check --deploy` com o perfil de produção apontou `security.W008` para redirecionamento a HTTPS e `security.W004` para HSTS. Antes da abertura, verificar o redirecionamento externamente, definir como o proxy informa o protocolo e aplicar HSTS após confirmar que o domínio opera corretamente em HTTPS. Se o proxy fizer o redirecionamento, registrar a configuração que atende ao controle e a evidência externa. [Checklist de implantação do Django](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

## Opções de hospedagem em avaliação

**VPS Hostinger, recomendada para o piloto fictício.** Usar Linux com Docker Compose, Django em servidor WSGI, PostgreSQL em rede privada e proxy reverso com HTTPS para servir a aplicação e os arquivos estáticos. Configurar o limite da requisição acima de 5 MiB para comportar o arquivo e a sobrecarga do formulário. O KVM 1 com 1 vCPU e 4 GB de RAM é candidato para poucos participantes. Medir consumo de memória, CPU e disco antes de aceitar o porte. A equipe precisará manter o sistema operacional, certificados, monitoramento, cópias e restauração. [Hostinger Docker Hosting](https://www.hostinger.com/br/docker-hosting) · [Modelo Docker da Hostinger](https://www.hostinger.com/support/8306612-how-to-use-the-docker-vps-template-at-hostinger/) · [Backups da VPS](https://www.hostinger.com/br/support/1583232-como-fazer-backup-ou-restaurar-um-servidor-vps-hostinger/)

**Vercel, alternativa.** Hospeda Django com Python 3.14 e PostgreSQL externo, por exemplo Neon. O limite de 4,5 MB do corpo da requisição da função é inferior aos 5 MiB por arquivo aceitos pela aplicação de demonstração. O envio atual exigiria um limite menor na aplicação ou outro fluxo de upload. Cada alternativa precisaria de aceite e de revalidação de autorização, confirmação e reenvio. [Django na Vercel](https://vercel.com/docs/frameworks/full-stack/django) · [Python na Vercel](https://vercel.com/docs/functions/runtimes/python) · [Limites das funções](https://vercel.com/docs/functions/limitations) · [PostgreSQL na Vercel](https://vercel.com/docs/postgres)

## Roteiro para o ambiente remoto

1. **Confirmar destino e recorte.** Registrar ambiente, domínio, responsáveis, participantes, janela e dados autorizados. A proposta é usar apenas dados fictícios, com cadastro, inspeção, documentos, cancelamento, pontuação, termo, correção e consulta das I01 a I12. A abertura ocorre após a autorização e o aceite do ambiente. [P015 a P019 e P022](pendencias.md#p015-hospedagem-e-operação)
2. **Preparar ambiente isolado.** Fixar a versão implantada. Usar segredos próprios, hosts explícitos, `DEBUG=False`, cookies seguros, processos de aplicação e banco com acesso restrito. Definir a configuração de homologação separada para habilitar os fluxos de demonstração. Eles ficam desabilitados por padrão no perfil de produção. Configurar HTTPS, o encaminhamento confiável do protocolo e as restrições de acesso antes de convidar participantes.
3. **Restaurar e migrar.** Ensaiar recuperação em banco descartável, verificar migrações e aplicar a versão prevista em uma única execução controlada. Conferir arquivos estáticos, login, sessão, permissões, rotas privadas e operação via HTTPS. Verificar o maior arquivo aceito, rejeição acima do limite, tipo inválido e resposta perdida. Repetir as verificações de documentos e termos após a restauração.
4. **Validar com os participantes.** Repetir os cenários de campo em celular e tablet reais, incluindo seleção de arquivo, foto, teclado, foco e rede intermitente. Medir o tempo de resposta e o volume conforme metas de P018. Verificar que os registros da aplicação e do proxy permitem diagnosticar falhas sem expor dados dos formulários. Registrar configuração, evidências, falhas, responsável pelo atendimento e decisão de abrir ou corrigir.
5. **Preparar recuperação.** Definir agenda, retenção, proteção e destino externo das cópias. Para um incidente, restringir escritas e preservar logs e registros afetados. Restaurar em outro banco, confrontar os resultados e termos com as operações ocorridas após a cópia e reabrir se o responsável aprovar. Antes de voltar a uma versão de aplicação, avaliar compatibilidade do esquema e preservar escritas confirmadas.

## Procedimento de cópia e recuperação

Executar com credenciais fornecidas ao cliente PostgreSQL pelo ambiente. Gravar a cópia em local protegido. Restaurar em banco novo e isolado, com credenciais e permissões do destino já preparadas. A exclusão dos dados de sessão exige novo login após recuperação.

```sh
umask 077

pg_dump --format=custom --no-owner --no-acl \
  --exclude-table-data=public.django_session \
  --dbname "$PILOTO_BANCO_ORIGEM" --file "$PILOTO_ARQUIVO_BACKUP"

pg_restore --exit-on-error --single-transaction --no-owner --no-acl \
  --dbname "$PILOTO_BANCO_RESTAURACAO" "$PILOTO_ARQUIVO_BACKUP"
```

Verificar a trilha da inspeção, os resultados anterior e corrigido, os anexos, os termos emitidos e as liberações. Repetir o login e conferir o acesso de uma unidade autorizada e de outra unidade ao mesmo termo. A configuração de implantação, os segredos, as funções e as permissões PostgreSQL precisam de procedimentos próprios. Nesta versão, anexos e termos de demonstração estão no banco. Se o armazenamento mudar, a recuperação precisará incluir os objetos externos e os vínculos com o banco. [pg_dump do PostgreSQL 17](https://www.postgresql.org/docs/17/app-pgdump.html) · [pg_restore do PostgreSQL 17](https://www.postgresql.org/docs/17/app-pgrestore.html)

## Caso o projeto avance para operação remota

Provedor e destino, participantes, dispositivos e navegadores, configuração remota, política de arquivos e retenção, responsáveis, metas de capacidade e recuperação e autorização para abertura. O ensaio local apoia a preparação do piloto. Uso de dados reais e regras oficiais continuam sujeitos a validação. O adiamento e a reanálise da demonstração seguem a decisão da I14. [Plano da I13](plano-implementacao.md#i13--homologação-e-piloto-controlado) · [Pendências](pendencias.md) · [Cartão da I13](https://trello.com/c/y1hVzQze)
