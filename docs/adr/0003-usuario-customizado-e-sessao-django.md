# ADR 0003: Usuário customizado e sessão Django

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** registro de base já confirmada, sem aprovação de políticas adicionais.
- **Origem:** DC007 nas [decisões confirmadas](../decisoes-confirmadas.md); F008 no [índice de fontes](../referencias/README.md).

## Contexto

O sistema precisa identificar usuários e relacioná-los aos acessos de Fiscalização, Administrador e Estabelecimento. O usuário escolheu login por nome de usuário e senha, usuário customizado baseado em `AbstractUser` e sessão Django.

## Decisão registrada

Usar essa base de identidade e sessão. Login/logout ligados à sessão pertencem à camada HTTP; verificação do escopo de negócio continua nos services. Perfil de negócio, acesso ao Admin e superusuário técnico são conceitos distintos. Supervisor é designação de fiscal por ação, não um quarto perfil ou autorização global.

Como consequência técnica, planejar o usuário customizado antes das primeiras migrações da aplicação de identidade. A documentação do Django exige que o modelo configurado como usuário seja criado na primeira migração de seu app. Essa referência não escolhe a versão do projeto. [Customização de autenticação no Django](https://docs.djangoproject.com/en/stable/topics/auth/customizing/).

## Alternativas e razões

- Usuário padrão e substituição posterior: não segue a escolha já feita e cria uma mudança estrutural futura desnecessária.
- Identidade externa, token de API ou SSO como base obrigatória: não foram escolhidos para a aplicação web atual.
- Modelo físico de perfis, grupos ou vínculos definido agora: anteciparia as decisões de P002 e da Etapa 6.

A preocupação com mudanças posteriores é análise técnica desta documentação, não resultado de migração executada.

## Consequências

A identidade precisa ser considerada desde a fundação e referenciada de modo consistente pelos demais módulos. A equipe mantém os fluxos de sessão e credenciais; essa base não resolve recuperação de conta, tentativas, MFA ou revogação sozinha como política do produto.

## Pendências e verificação futura

P002 mantém campos, identificadores e vínculos abertos. P014 mantém políticas complementares de acesso. As Etapas 4, 5 e 6 detalharão a fundação, autenticação e permissões. Verificar futuramente acesso ativo/inativo, encerramento de sessão, identidade usada pelo service e isolamento por vínculo. Não há modelo ou migração criado neste ADR.

Relacionados: RF001, RF002, RS003 e RS004 no [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md); [arquitetura](../arquitetura.md).
