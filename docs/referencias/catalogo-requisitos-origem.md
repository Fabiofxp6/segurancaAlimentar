# Catálogo de requisitos da fonte revisada

Extraído de F003 em 10/11/2026. São identificadores e títulos da fonte, sem alteração de regras, aprovação de prioridades ou elaboração de PRD. Para descrições, tipos e verificações, consultar os [requisitos revisados](arquivos/Documento_Requisitos_Python_Django_Revisado.docx).

RF027: adiamento com fluxo pendente de validação. RF028: proposta de reanálise ainda não aprovada. RNF e RS preservam as metas e políticas abertas descritas na fonte. As confirmações posteriores estão no [registro de decisões](../decisoes-confirmadas.md).


## Requisitos funcionais

| ID | Título da fonte |
|---|---|
| RF001 | Autenticar usuário e encerrar sessão |
| RF002 | Gerir usuários e designar supervisor por ação |
| RF003 | Gerir estabelecimentos |
| RF004 | Gerir checklist regras e versões |
| RF005 | Atribuir inspeção e equipe de fiscalização |
| RF006 | Iniciar inspeção pelo fiscal |
| RF007 | Congelar checklist no início |
| RF008 | Registrar respostas e evidências |
| RF009 | Anexar fotos e evidências |
| RF010 | Operar exclusivamente online |
| RF011 | Tratar perda de conexão |
| RF012 | Exibir estado de salvamento |
| RF013 | Calcular pontuação e classificação |
| RF014 | Concluir inspeção no servidor |
| RF015 | Gerar termo em PDF |
| RF016 | Consultar resultados finais e termos do estabelecimento |
| RF017 | Enviar documentos pelo estabelecimento |
| RF018 | Solicitar e autorizar alteração da fiscalização |
| RF019 | Aplicar correção com histórico |
| RF020 | Recalcular resultado após correção |
| RF021 | Versionar termo e retificar |
| RF022 | Solicitar e autorizar cancelamento da inspeção |
| RF023 | Registrar trilha de auditoria |
| RF024 | Consultar inspeções com filtros |
| RF025 | Assinatura e registro de ciência |
| RF026 | Dashboard de indicadores e relatórios |
| RF027 | Solicitar adiamento da fiscalização |
| RF028 | Reanalisar documentos após a conclusão |

## Requisitos não funcionais

| ID | Título da fonte |
|---|---|
| RNF01 | Usabilidade responsiva |
| RNF02 | Disponibilidade |
| RNF03 | Desempenho |
| RNF04 | Confiabilidade |
| RNF05 | Integridade dos dados |
| RNF06 | Escalabilidade |
| RNF07 | Compatibilidade |
| RNF08 | Acessibilidade |
| RNF09 | Manutenibilidade |
| RNF10 | Observabilidade |
| RNF11 | Backup e recuperação |
| RNF12 | Portabilidade |
| RNF13 | Qualidade dos documentos PDF |
| RNF14 | Tratamento de conexão |

## Requisitos de segurança

| ID | Título da fonte |
|---|---|
| RS001 | Autorização no servidor |
| RS002 | Menor privilégio e Supervisor |
| RS003 | Autenticação e credenciais |
| RS004 | Gestão de sessão |
| RS005 | Proteção do tráfego |
| RS006 | Proteção dos dados armazenados |
| RS007 | Proteção da auditoria |
| RS008 | Validação de arquivos |
| RS009 | Validação das entradas |
| RS010 | Acesso a evidências e termos |
| RS011 | Gestão de segredos |
| RS012 | Proteção dos logs |
| RS013 | Retentativa sem duplicidade |
| RS014 | Preservação temporária no navegador |
| RS015 | Gestão de vulnerabilidades |
| RS016 | Resposta a incidentes |
