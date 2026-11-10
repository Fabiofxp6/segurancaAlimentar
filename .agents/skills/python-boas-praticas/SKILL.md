---
name: python-boas-praticas
description: Escrever ou revisar Python do sistema alimentar com contratos claros, erros tratados e efeitos explícitos. Use em alterações Python autorizadas; regras específicas de Django e persistência estão na skill de Django e na arquitetura.
license: Consulte ../../third-party/NOTICE.md e o aviso MIT indicado ali.
---

# Python do projeto

Ler a [arquitetura](../../../docs/arquitetura.md), a spec afetada e o [estado](../../../docs/state.md). Conferir P001 e as dependências declaradas antes de usar recursos de uma versão; a versão de Python continua aberta enquanto não houver decisão registrada.

Escrever funções com responsabilidade clara e nomes compatíveis com o domínio. Usar tipos para tornar entradas e retornos compreensíveis, sem criar camadas, classes ou protocolos apenas para cumprir um modelo genérico. Separar efeitos de persistência, arquivos e comunicação do cálculo que pode ser verificado isoladamente.

Tratar falhas previsíveis de maneira específica e preservar contexto útil. Não capturar toda exceção e devolver sucesso, lista vazia ou resultado padrão que esconda falha oficial. A tradução para HTTP pertence à view; o service não recebe `request` nem retorna resposta HTTP.

Não fazer consulta, gravação ou instalação de dependência ao importar um módulo. Utilizar mecanismos existentes de configuração e manter segredos fora do código e dos registros. Não introduzir FastAPI, Flask, SQLAlchemy, Pydantic, Redis ou processamento assíncrono por estarem nos exemplos da coleção de origem.

Preservar limites e precisão aprovados para cálculo e datas. Fórmula, pesos, arredondamento e tipos físicos ainda abertos precisam de decisão; não adotar os números dos exemplos. Evitar estado global mutável que misture usuários ou inspeções.

Verificar a mudança com os cenários pertinentes da spec e com a [skill de testes](../testes/SKILL.md). Não criar testes que apenas repitam a implementação ou instalar ferramentas de lint/tipos sem necessidade e escopo. Informar o que foi executado e as limitações reais.

Respeitar a etapa e a autorização recebidas e atualizar o [Trello](../../../docs/acompanhamento-trello.md). Esta skill orienta trabalho futuro; sua criação não inicia código.

Origem e adaptações: [registro da curadoria](../../../docs/curadoria-skills-agentes.md).
