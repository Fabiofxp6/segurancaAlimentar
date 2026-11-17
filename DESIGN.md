---
version: alpha
name: Sistema de Avaliação de Segurança Alimentar
description: Linguagem visual da interface web de fiscalização, gestão e atendimento ao estabelecimento.
colors:
  tinta: '#112d50'
  secundaria: '#405b78'
  primary: '#1257a3'
  azul-forte: '#0b4079'
  azul-claro: '#eaf3fd'
  fundo: '#f3f6fa'
  superficie: '#ffffff'
  navegacao: '#112d50'
  borda: '#d5e0eb'
  borda-campo: '#7d91a7'
  salvo: '#006940'
  salvo-fundo: '#e4f8ef'
  aviso: '#845000'
  aviso-fundo: '#fff4dd'
  erro: '#ac202a'
  erro-fundo: '#fff0f0'
typography:
  sans:
    fontFamily: Inter, system-ui, sans-serif
    fontSize: 1rem
    lineHeight: '1.5'
rounded:
  base: 0.625rem
spacing:
  painel: 1.5rem
omitted:
  - section: components
    reason: Os componentes reutilizam os tokens nos estilos compartilhados.
---

## Overview

O sistema organiza as inspeções de segurança alimentar e a consulta aos resultados liberados. A interface segue a identidade azul do protótipo RF-08 e mantém visíveis o contexto da inspeção, a ação principal e o estado de confirmação.

## Colors

Use a navegação azul-marinho para orientar o usuário e superfícies brancas para o conteúdo. Reserve o azul de ação para comandos e atalhos prioritários. Use borda mais escura nos campos editáveis e borda suave para separar registros. Combine verde, âmbar ou vermelho com o texto do estado correspondente em avisos e etiquetas.

## Typography

Use a família sem serifa em títulos, formulários e listas. Dê mais peso ao nome da unidade ou à ação da página e deixe as informações complementares em cor secundária. Use algarismos tabulares em datas, contagens e progresso quando precisarem ser lidos em sequência.

## Layout

No celular, mantenha a barra superior compacta e use abas para alternar entre a resposta e as evidências. No desktop, mostre a navegação lateral por perfil e alinhe as listas de inspeções em colunas. Quando houver espaço, use painéis lado a lado no detalhe, no registro de campo e no resumo. Centralize formulários de acesso e limite a largura dos formulários de preenchimento para manter os rótulos próximos aos campos.

## Elevation & Depth

Separe painéis, registros e campos por bordas. Use a sombra de elevação para indicar que o menu ou o diálogo está sobre o conteúdo.

## Shapes

Use cantos arredondados em painéis e controles. Reserve a forma circular para indicadores compactos, como o progresso do resumo e o ponto que acompanha o texto das etiquetas.

## Components

- **Ações.** Use botão azul para salvar ou confirmar o fluxo, ação contornada para voltar e tratamento de erro para remoções. Em confirmações destrutivas, posicione o foco inicial na opção de voltar.
- **Registros.** Use o cartão inteiro como ligação quando ele representa um único destino. Mostre o texto da ação ou do registro antes dos metadados.
- **Formulários.** Mantenha os rótulos visíveis e o foco por teclado. Quando houver erros, mostre o resumo no início do formulário e permita ir ao primeiro campo indicado.
- **Envios.** Escreva o estado junto ao formulário. Exiba a confirmação de salvamento após o retorno do servidor e mantenha um aviso com ação de verificação quando a conexão cair.
