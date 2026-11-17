# I03 — Cadastros, perfis e vínculos

Etapa verificada no ambiente local em 15/11/2026. A entrega reúne cadastro de estabelecimentos, manutenção de contas comuns, concessão técnica do perfil Administrador e vínculo com unidade. A supervisão por ação segue no recorte I05.

## Fluxos entregues

| Fluxo | Comportamento |
|---|---|
| `/gestao/estabelecimentos/` | Administrador ativo lista, cadastra, consulta, edita e inativa. Nome obrigatório, documento textual e chave preservada na inativação. [Spec 0004](specs/0004-cadastro-estabelecimentos.md) |
| `/gestao/usuarios/` | Administrador ativo mantém nome, perfil permitido e situação de contas de Fiscalização e Estabelecimento. O nome de usuário é definido no cadastro. Conta nova começa inativa. A ativação exige credencial já configurada. DC039 acrescentou a opção de definir a senha no cadastro ou depois, pela web. |
| `provisionar_administrador` | Equipe técnica concede o perfil a uma conta dedicada, ativa, com senha configurada e ainda sem perfil. O servidor registra o operador técnico, o alvo, a data e o perfil concedido. A repetição para a mesma conta mantém o registro original. |
| `/gestao/usuarios/<id>/vinculo/` | Administrador ativo atribui, troca ou encerra a unidade vinculada à conta de Estabelecimento. Cada conta pode ter um vínculo aberto, e a mesma unidade pode ter várias contas. O vínculo pode ser preparado antes da ativação. |
| `/conta/estabelecimento/<id>/` | Conta ativa de Estabelecimento vê apenas o nome da unidade ativa vinculada. O acesso é consultado no banco a cada requisição. Unidade alheia, inexistente ou com vínculo encerrado recebe a mesma página 404. |

O sistema encerra o vínculo anterior na mesma transação que cria o próximo. Mudança do perfil Estabelecimento encerra seu vínculo. Inativar uma conta ou unidade bloqueia o acesso enquanto estiver inativa. Ao reativar, um vínculo que permaneceu aberto volta a valer. A remoção definitiva do acesso à unidade é feita encerrando o vínculo.

Alterações de cadastros e vínculos registram autoria, data e dados pertinentes. A versão do cadastro também protege a gestão de vínculos contra alterações desatualizadas. As chaves de usuário, unidade e operador web preservam a autoria histórica. A concessão administrativa registra a conta do sistema operacional informada pelo ambiente do comando. [Spec 0003](specs/0003-acesso-vinculos-supervisao.md) · [DC027](decisoes-confirmadas.md#dc027-perfis-e-vínculos-na-i03)

## Evidências

| Referência | Resultado |
|---|---|
| RF003 e AC01–AC02 | Cadastro, consulta, edição, inativação, rejeição de nome inválido e preservação de zeros iniciais verificados. |
| RF002 parcial e AC03–AC07 | Verificados perfil concedível, negativa de autoelevação via web, conta inativa, concessão técnica registrável e repetição sem duplicar histórico. |
| AC13–AC14, AC30–AC35 | Verificados acesso por URL à unidade própria, negativa para unidade alheia, remoção na mesma sessão, CSRF, concorrência em duas transações, repetição sem criar vínculo duplicado, conflito de versão e reversão da troca após falha de banco simulada. |
| AC36 e continuidade | Migração aditiva preservou a senha e o histórico de autoria de contas preexistentes. A representação continua com três perfis-base e um vínculo aberto por conta de Estabelecimento. |

A suíte executou **39 testes no PostgreSQL isolado**, incluindo 10 adicionados para vínculos e concessão administrativa. A navegação em Chromium a 360 px conferiu atribuição do vínculo, página da unidade própria, negativa para outra unidade e encerramento na mesma sessão.

## Atualização da gestão de senhas

A configuração e a redefinição administrativas foram verificadas com os 128 testes da suíte e em Chromium, incluindo a invalidação da sessão anterior na solicitação seguinte, o ingresso com a senha nova e as negativas de acesso. Histórico e respostas preservam o sigilo do valor e seu hash. [Trello](https://trello.com/c/gWdTEHws)

## Pendências operacionais

- P002 mantém abertas as regras cadastrais adicionais de documento e contato e os procedimentos operacionais de revogação de Administrador.
- P014 mantém em aberto o canal de entrega de credenciais reais, a política de senha e os efeitos de reativação sobre sessões antigas. A ativação continua separada. DC039 acrescentou a configuração de credencial pelo Administrador na própria gestão de usuários.
- P017, P019 e P020 mantêm em revisão a retenção e consulta a histórico, a homologação em dispositivos e o tratamento geral de resposta perdida. A verificação de repetição desta etapa cobre vínculo e concessão administrativa.
- A conferência de histórico de identificação em uma inspeção real depende da relação com a inspeção na I05.

O [preparo local](../README.md#demonstrar-a-gestão-no-ambiente-local) mostra como testar com dados fictícios. O [cartão da I03](https://trello.com/c/di9RwaAR) registra o fechamento. A I04 depende de autorização e das regras de checklist em P009.
