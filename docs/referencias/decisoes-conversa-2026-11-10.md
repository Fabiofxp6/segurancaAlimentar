# F008 Decisões da conversa e execução por etapas

Consolidado em: 10/11/2026. Origem: instruções e respostas explícitas do usuário nesta conversa. Este é um resumo das decisões, não uma transcrição integral nem uma nova ata de reunião. Mantém a rastreabilidade das confirmações posteriores às fontes de 09/11.

## Local e limites

O usuário escolheu criar a documentação na pasta nova `Documents/segurancaAlimentar`, preservando o `.env` existente e o blog de referência. O planejamento aprovado é documental: não criar código Django, ambiente, banco, migrações ou Git nesta fase.

## Padrão arquitetural

Na pergunta sobre o padrão, o usuário selecionou “Padrão do blog”: Django com templates, MVT, regras em services e views derivadas diretamente de View, adaptado ao domínio alimentar. A aprovação do plano também abrange forms para entrada, models para persistência, templates para apresentação e login/logout na view quando dependentes da sessão HTTP. O Admin deve respeitar as regras de negócio.

Essa escolha substitui a situação de proposta atribuída a esses padrões na análise independente de 09/11. A redação detalhada da arquitetura e suas exceções ocorrerá na Etapa 3.

## Autenticação

O usuário selecionou “Login e senha Django”: nome de usuário e senha, usuário customizado e sessão Django; recuperação, MFA e SSO continuam pendentes. O plano aprovado especifica usuário baseado em AbstractUser. Campos adicionais e políticas não foram definidos por essa escolha.

## Escopo das specs

O usuário escolheu detalhar inicialmente fundação e acesso. O plano aprovado prevê três specs: fundação técnica, autenticação e perfis/acesso. As outras funções ficarão em roteiro ligado ao PRD, sem specs completas nesta primeira rodada documental.

## Organização do trabalho

Após aprovar o plano, o usuário solicitou divisão em etapas, uma por vez, sem executar tudo de uma vez. Foram definidas oito etapas, registradas em `docs/etapas.md`. Não haverá avanço automático.

## Autorização desta entrega

Pedido do usuário: “Pode seguir com a etpa 1”. Isso autoriza somente organizar as fontes, consolidar decisões e pendências e criar o estado inicial. Não autoriza iniciar o PRD ou as etapas seguintes nesta mesma execução.
