# ADR 0002: MVT com services e Django Templates

- **Status:** Proposto.
- **Data:** 2026-11-10.
- **Natureza:** registro de base confirmada, com detalhamento de fronteiras proposto para revisão.
- **Origem:** DC005 e DC006 nas [decisões confirmadas](../decisoes-confirmadas.md); F008 no [índice de fontes](../referencias/README.md).

## Contexto

Os mesmos atos oficiais podem ser acessados por telas e administração técnica. Concentrar regras em uma única tela permite que outra entrada contorne autorização, cálculo ou histórico. O usuário escolheu o padrão da referência: MVT, templates, views próprias derivadas diretamente de `View` e regras/consultas explícitas em services independentes de HTTP.

## Decisão registrada

Views coordenam HTTP; forms validam entrada; services consultam, autorizam e executam os casos de uso; models representam persistência e integridade; templates apresentam. Services não recebem `request` nem retornam resposta HTTP. Mixins de acesso são admitidos. Login/logout dependentes da sessão ficam na view.

O detalhamento proposto na [arquitetura](../arquitetura.md) distingue ORM explícito da aplicação de consultas internas do framework. Validação de `ModelForm`, sessão, autenticação, migrações e ciclo interno do Admin não precisam ser reescritos como services. Não podem, porém, esconder decisões de fiscalização nesses caminhos.

No Admin, ações de negócio usam os mesmos casos de uso. Propõe-se bloquear edição/exclusão direta de modelos críticos até existir integração que preserve as invariantes, sem gravação automática posterior divergente.

## Alternativas e razões

- Regras em views ou forms: tornam difícil garantir comportamento igual em todas as entradas.
- Fluxos centrais em `save()` ou signals: tornam menos explícitos o ator, a autorização e a sequência do ato.
- Frontend separado com API obrigatória: adiciona contratos e operação sem requisito que o exija neste momento.
- Views genéricas próprias: não seguem a escolha expressa de herança direta de `View`.

As razões de manutenção acima são análise técnica; não indicam que essas alternativas foram implementadas ou medidas.

## Consequências

Há mais coordenação explícita e código de view do que em um CRUD automático. A separação permite reutilizar e verificar regras, mas exige contratos claros e cuidado com consultas implícitas na apresentação. O Admin pode ter funções deliberadamente limitadas até haver integração adequada.

## Pendências e verificação futura

Etapas 4 a 7 detalharão contratos, retornos, falhas e convenções. Verificar futuramente ausência de regra de negócio/ORM explícito nas views, independência HTTP dos services e igualdade das invariantes entre entradas. Ainda não existem esses componentes ou testes.

Relacionados: RNF09, RNF10, RS001 e RS009 no [PRD](../prd/0001-sistema-avaliacao-seguranca-alimentar.md).
