---
name: python-boas-praticas
description: Especificar, escrever ou revisar Python do sistema alimentar com dados, erros e efeitos explícitos. Use em contratos ou alterações Python autorizados; regras de Django e persistência estão na skill de Django e nas specs.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Python do projeto

Consultar o [estado](../../../docs/state.md), a [arquitetura](../../../docs/arquitetura.md) e somente a spec pertinente ao pedido. Usar a [fundação](../../../docs/specs/0001-fundacao-tecnica.md) para configuração/identidade, a [autenticação](../../../docs/specs/0002-autenticacao.md) para credenciais/sessão e o [acesso](../../../docs/specs/0003-acesso-vinculos-supervisao.md) para perfis/vínculos/designações. Preservar as [decisões confirmadas](../../../docs/decisoes-confirmadas.md) e as [pendências](../../../docs/pendencias.md).

## Contrato e dados

- Conferir P001 antes de usar recurso dependente de versão ou escolher ferramenta. A estrutura e os nomes candidatos das specs não aprovam implementação.
- Expressar entradas/retornos com tipos compreensíveis, sem criar classes, protocolos, DTOs ou camadas por convenção. UUID, nomes de campos, máscaras e limites transcritos não escolhem schema; respeitar P002 e o contrato vigente.
- Separar valores recebidos dos derivados no servidor. Referência válida não prova autorização; ator, autoria e concessão não vêm livremente do formulário.
- Preservar texto e segredo segundo o campo. Não aplicar remoção de espaços ou conversão de caixa indiscriminadamente: a senha segue o contrato próprio da Spec 0002.
- Não manter estado global mutável que misture usuários/inspeções. Não consultar/gravar banco, carregar segredos ou instalar dependências como efeito de importar módulo.

## Efeitos e falhas

- Services concentram regra e ORM explícito da aplicação, sem `request`/`HttpResponse`; a view traduz a resposta HTTP. As exceções nativas de autenticação e forms estão na arquitetura e na skill de Django.
- Separar cálculo verificável de persistência, arquivos e comunicação. Fórmula, pesos, precisão, arredondamento e datas precisam seguir a política aprovada; não adotar números da coleção de origem.
- Tratar falhas previsíveis de forma específica. Não converter exceção de banco/configuração, indisponibilidade ou conflito em sucesso, acesso permitido, lista vazia ou resultado padrão enganoso.
- Retorno de função, envio iniciado ou timeout não comprovam gravação oficial. Preservar a ambiguidade e o contexto de falha sem incluir corpo sensível, senha ou segredo em exceções/logs.
- Não introduzir FastAPI, Flask, SQLAlchemy, Pydantic, Redis ou processamento assíncrono por aparecerem em exemplos externos. Dependência nova precisa de necessidade e decisão no recorte autorizado.

## Verificação e entrega

Usar os cenários pertinentes da spec e a [skill de testes](../testes/SKILL.md); VF/AU/AC/VR continuam futuros até execução com evidência. Verificar comportamento, falhas e efeitos reais, sem testes que apenas reproduzam a implementação. Não instalar lint/tipagem ou executar banco por iniciativa de uma tarefa documental.

Em análise ou documentação, entregar apenas o artefato pedido. Em implementação autorizada, resolver antes os bloqueios aplicáveis e preservar mudanças do usuário e arquivos de ambiente. Relatar o que foi executado e as limitações; atualizar o [Trello](../../../docs/acompanhamento-trello.md) sem marcar requisito implementado pela redação.

Origem: [curadoria](../../../docs/curadoria-skills-agentes.md). Revisão integrada: [Etapa 7](../../../docs/revisao-skills-tecnicas.md).
