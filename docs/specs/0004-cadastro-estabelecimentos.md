# Spec 0004 — Cadastro de estabelecimentos

RF003, com controle de acesso de RS001 e validação de RS009. O recorte I03 usa a autoridade de manutenção de estabelecimento prevista para o perfil Administrador. A spec de acesso registra a situação dos vínculos e da gestão de usuários. [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md#rf003-gerir-estabelecimentos) · [Spec 0003](0003-acesso-vinculos-supervisao.md)

## Dados do cadastro

| Campo | Tipo técnico | Preenchimento neste recorte |
|---|---|---|
| Nome | Texto | Obrigatório. Remover espaços externos e recusar valor em branco. |
| Documento | Texto | Opcional na I03. Preservar zeros iniciais e pontuação. Tipo, máscara e unicidade seguem em revisão. |
| Endereço | Texto | Opcional na I03. Formato em revisão. |
| Contato | Texto | Opcional na I03. Formato em revisão. |
| Ativo | Booleano | Cadastro inicia ativo. A edição permite alterar o estado, preservando a identidade do estabelecimento. |
| Versão | Inteiro positivo, gerado no servidor | Conferida na edição para evitar sobrescrever mudanças de outra tela. |

Os campos opcionais e o estado inicial são escolhas do recorte local. A homologação cadastral pode exigir campos ou regras adicionais em P002.

## Operações

O Administrador ativo consulta a lista paginada, abre um registro para consulta e edição e cria novos registros. O sistema verifica a identidade e o perfil no servidor a cada operação. O acesso a resultados ou documentos próprios será tratado nos fluxos correspondentes.

A edição usa a versão que o formulário abriu. Em conflito, retorna HTTP 409 e orienta reabrir o cadastro. Falha operacional reconhecida de banco retorna HTTP 503 e orienta consultar o registro antes de repetir. Nenhuma dessas respostas confirma gravação. A alteração e o histórico correspondente são feitos na mesma transação. O bloqueio de linha serializa edições concorrentes do mesmo cadastro enquanto a versão identifica formulários desatualizados. [Transações no Django](https://docs.djangoproject.com/en/5.2/topics/db/transactions/) · [Bloqueio de linhas no Django](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update) O histórico guarda objeto, autor, instante e dados alterados. A política operacional de acesso, retenção e proteção do histórico permanece em P017.

A inativação mantém a chave do estabelecimento e o histórico. Os futuros fluxos de inspeção devem guardar a identificação oficial aplicável à data do ato. O cadastro fornece a identidade estável e os registros de mudança usados por esses fluxos.

## Verificação

- Criar com nome válido e documento iniciado por zero. Consultar o valor após gravar.
- Rejeitar nome vazio ou composto só de espaços no servidor.
- Editar e inativar mantendo a mesma chave e o histórico. Rejeitar a cópia desatualizada e revalidar o acesso a cada ação.
- Recusar consulta ou mutação direta de Fiscalização, Estabelecimento, conta inativa, usuário sem perfil e conta técnica sem perfil de negócio.
- Simular falha do histórico e verificar a reversão do cadastro correspondente.
