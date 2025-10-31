# 📊 ESPECIFICAÇÃO TÉCNICA COMPLETA - DASHBOARD SIH/DATASUS JANEIRO-JULHO 2025

## 🎯 INFORMAÇÕES DO PROJETO

**Nome**: Dashboard de Análise de Internações Hospitalares - SUS
**Tecnologia Base**: Streamlit (Python)  
**Fonte de Dados**: SIH/DATASUS (Sistema de Informações Hospitalares)  
**Público-Alvo**: Gestores de saúde, epidemiologistas, reguladores e planejadores  

---

## 📐 ARQUITETURA E ESTRUTURA GERAL

### Layout Principal
- **Sidebar** (barra lateral esquerda):
  - Logo/título do dashboard
  - Filtros globais aplicáveis a todos os painéis
  - Informações sobre os dados carregados
  - Links para documentação/metodologia
  
- **Área principal** (centro):
  - Abas/páginas para cada painel funcional
  - Visualizações e métricas
  - Componentes interativos

### Sistema de Navegação
- Utilizar `st.sidebar` para navegação entre painéis
- Opções de navegação:
  - Radio buttons ou selectbox para escolha do painel
  - Ordem sugerida: Geral → Epidemiológico → Regulação → Estabelecimento → Procedimentos → Populacional → Temporal

---

## 🎨 DESIGN E IDENTIDADE VISUAL

### Paleta de Cores
- **Primária**: Tons de azul (#1f77b4, #2E86AB, #0066CC) - institucional SUS
- **Secundária**: Verde (#27ae60) para indicadores positivos
- **Alerta**: Vermelho (#e74c3c) para mortalidade/indicadores críticos
- **Neutra**: Cinza (#95a5a6) para dados complementares
- **Fundo**: Branco (#FFFFFF) ou cinza muito claro (#F8F9FA)

### Tipografia e Formatação
- Títulos: usar `st.title()` ou markdown `# Título`
- Subtítulos: usar `st.subheader()` ou markdown `## Subtítulo`
- Métricas destacadas: usar `st.metric()` com delta quando aplicável
- Números: formatar com separador de milhares (ex: 1.234.567)
- Valores monetários: formato brasileiro (R$ 1.234,56)
- Percentuais: sempre com 1 casa decimal (ex: 45,3%)

---

## 🔧 FILTROS GLOBAIS (SIDEBAR)

### Estrutura de Filtros

**1. Filtro de Período**
- **Componente**: `st.date_input()` com range
- **Labels**: "Período de Análise" com "Data Inicial" e "Data Final"
- **Comportamento**: 
  - Valor padrão: últimos 12 meses disponíveis
  - Validação: data final > data inicial
  - Formato exibido: dd/mm/aaaa

**2. Filtro de UF**
- **Componente**: `st.multiselect()` ou `st.selectbox()`
- **Label**: "Unidade Federativa"
- **Opções**: Lista de todas as UFs + opção "Todas"
- **Comportamento**: permite seleção múltipla

**3. Filtro de Município**
- **Componente**: `st.multiselect()` com busca
- **Label**: "Município(s)"
- **Comportamento**: 
  - Carrega municípios da UF selecionada
  - Campo de busca integrado
  - Opção "Todos os municípios"
  - Exibir código IBGE + nome

**4. Filtro de Estabelecimento (CNES)**
- **Componente**: `st.multiselect()` com busca
- **Label**: "Estabelecimento(s) de Saúde"
- **Formato**: "CNES - Nome Fantasia"
- **Comportamento**: filtro dinâmico baseado em município selecionado

**5. Filtro de CID**
- **Componente**: `st.multiselect()` com busca
- **Label**: "Diagnóstico Principal (CID-10)"
- **Formato**: "Código - Descrição"
- **Opções**: 
  - Busca por código ou descrição
  - Agrupamento por capítulo CID opcional

**6. Filtro de Procedimento**
- **Componente**: `st.multiselect()` com busca
- **Label**: "Procedimento(s) (SIGTAP)"
- **Formato**: "Código - Descrição"

**7. Filtros Demográficos**
- **Sexo**: `st.multiselect()` - opções: Masculino, Feminino, Ignorado
- **Faixa Etária**: `st.select_slider()` ou multiselect com faixas: 
  - <1 ano, 1-4, 5-9, 10-14, 15-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
- **Raça/Cor**: `st.multiselect()` - categorias do IBGE

**8. Botão de Ação**
- **Componente**: `st.button()` "Aplicar Filtros" (opcional se usar auto-update)
- **Componente**: `st.button()` "Limpar Filtros" - restaura valores padrão

**9. Informações dos Dados**
- Exibir em `st.info()`:
  - Total de registros carregados
  - Período efetivo dos dados
  - Data da última atualização
  - Fonte: "SIH/DATASUS"

---

## 📊 PAINEL 1: GERAL (GESTÃO E FINANÇAS)

### Objetivo
Visão macro dos principais indicadores de gestão e custos das internações.

### Estrutura de Layout

**Seção 1: Cards de KPIs (Linha Superior)**
- Usar `st.columns(5)` para 5 cards lado a lado
- Cada card com `st.metric()`:

1. **Total de Internações**
   - Valor principal: número absoluto formatado
   - Delta: variação % vs. período anterior (verde/vermelho)
   - Ícone sugerido: 🏥

2. **Média de Permanência**
   - Valor: X,X dias
   - Fórmula: `sum(Dias_Permanência) / count(AIH)`
   - Delta: comparativo temporal
   - Ícone: ⏱️

3. **Taxa de Mortalidade Hospitalar**
   - Valor: X,X%
   - Fórmula: `(count(MORTE = 1) / count(*)) * 100`
   - Delta: variação (vermelho se aumentou)
   - Ícone: 💔

4. **Taxa de Uso de UTI**
   - Valor: X,X%
   - Fórmula: `(sum(Dias_UTI) / sum(Dias_Permanência)) * 100`
   - Delta: comparativo
   - Ícone: 🏥

5. **Custo Médio por AIH**
   - Valor: R$ X.XXX,XX
   - Fórmula: `sum(Valor_Total) / count(AIH)`
   - Delta: variação de custo
   - Ícone: 💰

**Seção 2: Série Temporal de Internações**
- **Título**: "Evolução Mensal de Internações"
- **Tipo de Gráfico**: Plotly line chart (`px.line()`)
- **Eixos**:
  - X: Mês/Ano (formato: "Jan/2024")
  - Y: Número de internações
- **Interatividade**: 
  - Hover com data + valor
  - Zoom e pan habilitados
  - Botão de reset
- **Altura**: 400px
- **Opção adicional**: Toggle para exibir média móvel de 3 meses

**Seção 3: Visualizações Lado a Lado**
Usar `st.columns(2)`:

**Coluna Esquerda - Mapa de Calor por Município**
- **Título**: "Distribuição Geográfica de Internações"
- **Tipo**: Choropleth map (`px.choropleth_mapbox()` ou `folium`)
- **Dados**: Internações agregadas por município
- **Escala de cor**: gradiente azul claro → azul escuro
- **Interatividade**:
  - Hover: Nome do município + total de internações + taxa por 1.000 hab
  - Zoom
  - Click para destacar município
- **Mapa base**: OpenStreetMap ou Carto
- **Altura**: 500px

**Coluna Direita - Estimativa de Gastos por Município**
- **Título**: "Top 15 Municípios - Gastos com Internações"
- **Tipo**: Gráfico de barras horizontais (`px.bar()`)
- **Dados**: 
  - Y: Nome do município
  - X: Valor total em R$ (milhões)
  - Cor: gradiente por valor
- **Ordenação**: Decrescente por valor
- **Interatividade**: Hover com valor exato
- **Altura**: 500px

**Seção 4: Tabela Resumo**
- **Título**: "Resumo por Município"
- **Componente**: `st.dataframe()` com altura fixa (400px)
- **Colunas**:
  - Município
  - UF
  - Total de Internações
  - Média Permanência (dias)
  - Mortalidade (%)
  - Custo Total (R$)
  - Custo Médio (R$)
- **Funcionalidades**:
  - Ordenação por qualquer coluna
  - Busca integrada
  - Export para CSV (`st.download_button()`)

---

## 📊 PAINEL 2: EPIDEMIOLÓGICO

### Objetivo
Análise detalhada dos perfis de diagnóstico, morbimortalidade e características dos pacientes.

### Estrutura de Layout

**Seção 1: Cards Epidemiológicos**
- Usar `st.columns(4)`:
  1. **CID Mais Prevalente**: código + descrição + % do total
  2. **Principal Causa de Morte**: CID_MORTE mais frequente + %
  3. **Faixa Etária Modal**: idade mais comum + %
  4. **Comorbidades**: % de casos com CID secundário

**Seção 2: Top 10 Diagnósticos Principais**
- **Título**: "Principais Diagnósticos (CID-10 Principal)"
- **Tipo**: Gráfico de barras horizontais (`px.bar()`)
- **Dados**:
  - Y: Código CID + Descrição abreviada (max 50 chars)
  - X: Número de casos
  - Cor: gradiente por frequência
- **Adicional**: 
  - Percentual em label no final de cada barra
  - Hover detalhado com descrição completa do CID
- **Altura**: 400px
- **Opção de filtro**: Selecionar capítulo CID (dropdown acima do gráfico)

**Seção 3: Análise Demográfica**
Usar `st.columns(2)`:

**Coluna Esquerda - Pirâmide Etária**
- **Título**: "Distribuição Etária por Sexo"
- **Tipo**: Gráfico de barras divergente/pirâmide (`plotly.graph_objects`)
- **Dados**:
  - Eixo Y: Faixas etárias
  - Eixo X: Count (negativo para masculino, positivo para feminino)
  - Cores: azul (masculino) e rosa (feminino)
- **Interatividade**: Hover com valores absolutos e %
- **Altura**: 500px
- **Opção adicional**: Filtro para visualizar pirâmide por CID específico

**Coluna Direita - Distribuição por Sexo**
- **Título**: "Internações por Sexo"
- **Tipo**: Gráfico de pizza (`px.pie()`)
- **Dados**: Count por sexo
- **Cores**: azul (M), rosa (F), cinza (Ignorado)
- **Labels**: % + valor absoluto
- **Altura**: 500px

**Seção 4: Mortalidade Detalhada**
- **Título**: "Análise de Mortalidade Hospitalar"

Usar `st.tabs()` com 3 abas:

**Aba 1: Por CID**
- Gráfico de barras: Top 10 CIDs com maior taxa de mortalidade
- Eixo X: Taxa de mortalidade (%)
- Eixo Y: CID + descrição
- Cor: vermelho gradiente

**Aba 2: Por Faixa Etária**
- Gráfico de linhas: Taxa de mortalidade por faixa etária
- Mostrar tendência crescente com a idade
- Linha de referência: mortalidade média geral

**Aba 3: Por Município**
- Tabela ordenável com:
  - Município
  - Total de Óbitos
  - Taxa de Mortalidade (%)
  - Total de Internações
  - Taxa padronizada (opcional, se disponível)

**Seção 5: Série Temporal por CID**
- **Título**: "Evolução Temporal dos Principais Diagnósticos"
- **Componente**: Seletor de CIDs (`st.multiselect()`) - máximo 5 CIDs
- **Tipo**: Gráfico de linhas múltiplas (`px.line()`)
- **Dados**:
  - X: Mês/Ano
  - Y: Número de casos
  - Cor: Cada CID uma linha diferente
- **Legenda**: Posicionada à direita
- **Altura**: 400px
- **Opção adicional**: Toggle para escala absoluta ou relativa (%)

**Seção 6: Mapa de Mortalidade**
- **Título**: "Taxa de Mortalidade por Município"
- **Tipo**: Choropleth map
- **Escala de cor**: Branco → Vermelho escuro
- **Dados**: Taxa de mortalidade % por município
- **Hover**: Município + taxa + óbitos + internações
- **Altura**: 500px

**Seção 7: Tabela Interativa de Comorbidades**
- **Título**: "Associação CID Principal × CID Secundário"
- **Componente**: `st.dataframe()` com filtros
- **Colunas**:
  - CID Principal (código + descrição)
  - CID Secundário (código + descrição)
  - Frequência (n)
  - % do CID Principal
- **Funcionalidades**: 
  - Busca por CID
  - Export CSV
  - Ordenação por frequência

---

## 📊 PAINEL 3: REGULAÇÃO E TERRITÓRIO

### Objetivo
Analisar fluxos de pacientes entre municípios e identificar padrões de regionalização.

### Estrutura de Layout

**Seção 1: Cards de Regulação**
- Usar `st.columns(3)`:
  1. **Evasão Total**: % de pacientes atendidos fora do município de residência
  2. **Municípios com >50% Evasão**: número absoluto
  3. **Principal Município Receptor**: nome + qtd de pacientes externos

**Seção 2: Mapa de Fluxo de Pacientes**
- **Título**: "Fluxo de Pacientes Entre Municípios"
- **Tipo**: Mapa interativo com linhas de origem-destino
- **Tecnologia**: Plotly `scatter_mapbox()` + linhas ou Folium com plugins
- **Elementos**:
  - Pontos: municípios (tamanho proporcional ao volume)
  - Linhas: fluxo entre origem (residência) e destino (atendimento)
  - Espessura das linhas: proporcional ao volume de pacientes
  - Cor das linhas: gradiente por intensidade
- **Interatividade**:
  - Click em município: destaca fluxos relacionados
  - Hover em linha: origem + destino + n pacientes
  - Controle de zoom e pan
- **Filtros adicionais**: 
  - Slider para volume mínimo de pacientes (ex: mostrar apenas fluxos >100)
  - Toggle "Mostrar apenas evasão" (excluir fluxos intramunicipio)
- **Altura**: 600px

**Seção 3: Matriz de Regulação**
- **Título**: "Matriz Município de Residência × Município de Atendimento"
- **Tipo**: Heatmap (`px.imshow()` ou `sns.heatmap()`)
- **Dados**: 
  - Linhas: Município de Residência (top 20)
  - Colunas: Município de Atendimento (top 20)
  - Valores: Número de internações
  - Escala de cor: Branco → Azul escuro
- **Interatividade**: Hover com valores
- **Altura**: 500px
- **Nota**: Diagonal representa atendimento no próprio município (destacar)

**Seção 4: Análise de Evasão e Atração**
Usar `st.columns(2)`:

**Coluna Esquerda - Top Municípios com Evasão**
- **Título**: "Municípios com Maior Evasão"
- **Tipo**: Barras horizontais
- **Dados**:
  - Y: Município
  - X: % de evasão
  - Cor: vermelho gradiente
- **Limite**: Top 15
- **Hover**: % + n pacientes evadidos + principal destino

**Coluna Direita - Top Municípios Atratores**
- **Título**: "Municípios que Mais Recebem Pacientes Externos"
- **Tipo**: Barras horizontais
- **Dados**:
  - Y: Município
  - X: Número de pacientes externos recebidos
  - Cor: verde gradiente
- **Limite**: Top 15
- **Hover**: n pacientes + % do total de internações

**Seção 5: Bubble Plot - Volume de Internações**
- **Título**: "Análise de Oferta e Demanda por Município"
- **Tipo**: Scatter plot com bolhas (`px.scatter()`)
- **Eixos**:
  - X: Internações Realizadas (oferta)
  - Y: Residentes Internados (demanda)
  - Tamanho: População municipal (se disponível) ou volume total
  - Cor: Taxa de autossuficiência (%)
- **Linha de referência**: Diagonal x=y (autossuficiência perfeita)
- **Quadrantes**:
  - Acima da diagonal: mais demanda que oferta (evasão)
  - Abaixo da diagonal: mais oferta que demanda (atração)
- **Interatividade**: Hover com nome do município + valores
- **Altura**: 500px

**Seção 6: Tabela Detalhada de Estabelecimentos Receptores**
- **Título**: "Estabelecimentos que Mais Recebem Pacientes Externos"
- **Componente**: `st.dataframe()`
- **Colunas**:
  - CNES
  - Nome do Estabelecimento
  - Município
  - Total de Internações
  - Pacientes Externos (n)
  - Pacientes Externos (%)
  - Principais Municípios de Origem (top 3)
- **Ordenação**: Por % de pacientes externos (decrescente)
- **Funcionalidades**: Busca, ordenação, export CSV

---

## 📊 PAINEL 4: POR ESTABELECIMENTO (CNES)

### Objetivo
Análise comparativa de desempenho, perfil e custos dos estabelecimentos de saúde.

### Estrutura de Layout

**Seção 1: Seletor de Estabelecimento**
- **Componente**: `st.selectbox()` grande e destacado
- **Label**: "Selecione um Estabelecimento para Análise Detalhada"
- **Formato**: "CNES - Nome Fantasia - Município/UF"
- **Busca**: Campo de pesquisa integrado
- **Ação**: Ao selecionar, exibe perfil completo abaixo

**Seção 2: Perfil do Estabelecimento Selecionado**
(Exibido quando um CNES é selecionado)

Usar `st.columns(4)` para cards:
1. **Total de Internações**: valor + % do município
2. **Média de Permanência**: dias + comparação com média estadual
3. **Taxa de Mortalidade**: % + comparação com média
4. **Custo Médio AIH**: R$ + comparação

**Seção 3: Ranking de Hospitais**
- **Título**: "Ranking de Estabelecimentos por Volume"
- **Tipo**: Gráfico de barras horizontais (`px.bar()`)
- **Dados**:
  - Y: Nome do estabelecimento (top 20)
  - X: Número de internações
  - Cor: gradiente azul
- **Ordenação**: Decrescente por volume
- **Hover**: CNES + município + valor
- **Altura**: 600px
- **Filtro adicional acima do gráfico**:
  - Dropdown para selecionar critério de ranking:
    - Volume de internações
    - Custo total
    - Média de permanência
    - Taxa de mortalidade

**Seção 4: Análise Comparativa**
Usar `st.columns(2)`:

**Coluna Esquerda - Perfil de Casos por CNES**
- **Título**: "Distribuição de Casos do Estabelecimento Selecionado"
- Usar `st.tabs()` com 3 abas:
  - **Aba 1 - Por CID**: Barras horizontais (top 10 CIDs)
  - **Aba 2 - Por Sexo**: Pizza
  - **Aba 3 - Por Idade**: Histograma de distribuição etária

**Coluna Direita - Comparação com Média**
- **Título**: "Benchmarking do Estabelecimento"
- **Tipo**: Gráfico de radar/spider (`plotly.graph_objects.Scatterpolar`)
- **Dimensões**:
  - Volume de Internações (%)
  - Taxa de Mortalidade (%)
  - Custo Médio (%)
  - Permanência Média (%)
  - Complexidade de Casos (baseado em procedimentos)
- **Linhas**: 
  - Estabelecimento selecionado (azul sólido)
  - Média estadual (cinza tracejado)
- **Altura**: 400px

**Seção 5: Scatter Plot - Custo × Permanência**
- **Título**: "Análise de Eficiência: Custo Médio × Permanência Média"
- **Tipo**: Scatter plot (`px.scatter()`)
- **Eixos**:
  - X: Permanência média (dias)
  - Y: Custo médio por AIH (R$)
  - Tamanho: Volume de internações
  - Cor: Taxa de mortalidade (escala vermelho)
- **Elementos**:
  - Linhas de referência: médias gerais (X e Y)
  - Criando 4 quadrantes
- **Interatividade**: Hover com nome do estabelecimento
- **Altura**: 500px
- **Análise**:
  - Superior direito: Alto custo + longa permanência
  - Inferior esquerdo: Baixo custo + curta permanência

**Seção 6: Tabela Completa de Estabelecimentos**
- **Título**: "Tabela Geral de Estabelecimentos"
- **Componente**: `st.dataframe()` com altura 500px
- **Colunas**:
  - CNES
  - Nome
  - Município
  - UF
  - Total Internações
  - Média Permanência (dias)
  - Taxa Mortalidade (%)
  - Custo Total (R$)
  - Custo Médio (R$)
  - Principal CID
- **Funcionalidades**:
  - Ordenação por qualquer coluna
  - Busca por CNES ou nome
  - Filtro por UF (multiselect acima da tabela)
  - Export CSV
  - Highlight da linha: estabelecimento atualmente selecionado

**Seção 7: Série Temporal do Estabelecimento**
- **Título**: "Evolução Mensal - [Nome do Estabelecimento]"
- **Tipo**: Linha múltipla (`px.line()`)
- **Séries**:
  - Número de internações (eixo Y esquerdo)
  - Taxa de mortalidade % (eixo Y direito)
- **Cores**: azul e vermelho
- **Período**: Todos os meses disponíveis
- **Altura**: 350px

---

## 📊 PAINEL 5: PROCEDIMENTOS

### Objetivo
Análise dos procedimentos hospitalares mais realizados, seus custos e relações com diagnósticos.

### Estrutura de Layout

**Seção 1: Cards de Procedimentos**
- Usar `st.columns(4)`:
  1. **Total de Procedimentos Distintos**: número
  2. **Procedimento Mais Realizado**: código + descrição + n
  3. **Procedimento Mais Caro**: código + valor médio
  4. **Gasto Total com Procedimentos**: R$ (soma)

**Seção 2: Top Procedimentos Realizados**
- **Título**: "Procedimentos Mais Frequentes (SIGTAP)"
- **Tipo**: Barras horizontais (`px.bar()`)
- **Dados**:
  - Y: Código + Descrição do procedimento (top 15)
  - X: Quantidade realizada
  - Cor: gradiente por frequência
- **Hover**: 
  - Código completo
  - Descrição completa
  - Quantidade
  - Valor médio do procedimento
  - Valor total gasto
- **Altura**: 500px

**Seção 3: Análise de Custos por Procedimento**
Usar `st.columns(2)`:

**Coluna Esquerda - Valor Total Gasto**
- **Título**: "Top 15 Procedimentos por Gasto Total"
- **Tipo**: Barras horizontais
- **Dados**:
  - Y: Procedimento
  - X: Valor total (R$ milhões)
  - Cor: gradiente verde → vermelho
- **Ordenação**: Decrescente

**Coluna Direita - Custo Médio por Procedimento**
- **Título**: "Procedimentos Mais Caros (Custo Médio)"
- **Tipo**: Barras horizontais
- **Dados**:
  - Y: Procedimento
  - X: Custo médio (R$)
  - Cor: gradiente
- **Filtro**: Considerar apenas procedimentos com n>50 para evitar outliers

**Seção 4: Heatmap CID × Procedimento**
- **Título**: "Correlação entre Diagnósticos e Procedimentos"
- **Tipo**: Heatmap (`px.imshow()`)
- **Dados**:
  - Linhas: Top 15 CIDs mais prevalentes
  - Colunas: Top 15 procedimentos mais realizados
  - Valores: Frequência de associação (n de vezes que ocorrem juntos)
  - Escala: Amarelo claro → Laranja escuro
- **Interatividade**: Hover com CID + procedimento + n
- **Altura**: 600px
- **Análise**: Identifica quais procedimentos são típicos de cada diagnóstico

**Seção 5: Procedimento Solicitado × Realizado**
- **Título**: "Comparação: Procedimentos Solicitados vs. Realizados"
- **Tipo**: Gráfico de barras agrupadas (`px.bar()` com `barmode='group'`)
- **Dados**:
  - X: Top 15 procedimentos
  - Y: Quantidade
  - Grupos: 
    - Solicitado (azul)
    - Realizado (verde)
- **Métrica adicional**: Calcular e exibir taxa de realização (%) em card acima
- **Altura**: 400px

**Seção 6: Distribuição de Valores**
- **Título**: "Distribuição de Custos dos Procedimentos"
- **Tipo**: Box plot (`px.box()`)
- **Dados**: Valor unitário dos procedimentos
- **Agrupamento**: Por tipo ou grupo de procedimento (se classificação disponível)
- **Elementos**: 
  - Mediana
  - Quartis
  - Outliers
- **Altura**: 400px

**Seção 7: Tabela Detalhada de Procedimentos**
- **Título**: "Tabela Completa de Procedimentos"
- **Componente**: `st.dataframe()`
- **Colunas**:
  - Código SIGTAP
  - Descrição do Procedimento
  - Quantidade Solicitada
  - Quantidade Realizada
  - Taxa de Realização (%)
  - Valor Médio (R$)
  - Valor Total (R$)
  - Principal CID Associado
- **Funcionalidades**:
  - Busca por código ou descrição
  - Ordenação
  - Export CSV
- **Altura**: 400px

---

## 📊 PAINEL 6: POPULACIONAL E EQUIDADE

### Objetivo
Análise das desigualdades e diferenças no acesso e desfecho das internações por grupos populacionais.

### Estrutura de Layout

**Seção 1: Cards de Equidade**
- Usar `st.columns(4)`:
  1. **Raça/Cor Modal**: categoria mais frequente + %
  2. **% Raça/Cor Ignorada**: indicador de qualidade dos dados
  3. **Maior Disparidade**: grupo com maior diferença na taxa de mortalidade
  4. **Cobertura Indígena**: % de internações de indígenas vs. % pop

**Seção 2: Distribuição por Raça/Cor**
- **Título**: "Internações por Raça/Cor"
- **Tipo**: Barras empilhadas ou agrupadas (`px.bar()`)
- **Dados**:
  - X: Categorias (Branca, Preta, Parda, Amarela, Indígena, Ignorada)
  - Y: Número de internações
  - Opção de toggle: valores absolutos ou percentuais
- **Cores**: Usar cores neutras/representativas
- **Altura**: 400px
- **Adicional**: Linha horizontal mostrando distribuição na população geral (para comparação)

**Seção 3: Análise Geográfica da Equidade**
Usar `st.tabs()` com uma aba para cada raça/cor principal:

**Cada Aba contém**:
- **Mapa choropleth** por município
- **Métrica**: Taxa de internação por 10.000 habitantes daquele grupo
- **Escala de cor**: Gradiente específico para cada grupo
- **Hover**: Município + taxa + n absoluto
- **Altura**: 500px por mapa

**Seção 4: Análise de Desfechos por Grupo**
Usar `st.columns(2)`:

**Coluna Esquerda - Tempo de Permanência**
- **Título**: "Tempo Médio de Permanência por Raça/Cor"
- **Tipo**: Box plot (`px.box()`)
- **Dados**:
  - X: Raça/Cor
  - Y: Dias de permanência
- **Elementos**: mediana, quartis, outliers
- **Cores**: Diferenciadas por grupo
- **Análise**: Identifica diferenças no tempo de internação

**Coluna Direita - Taxa de Mortalidade**
- **Título**: "Taxa de Mortalidade Hospitalar por Raça/Cor"
- **Tipo**: Barras horizontais
- **Dados**:
  - Y: Raça/Cor
  - X: Taxa de mortalidade (%)
  - Cor: vermelho gradiente
- **Ordenação**: Decrescente por taxa
- **Linha de referência**: Média geral
- **Destacar**: Grupos acima da média

**Seção 5: Interseccionalidade - Raça × Sexo × Idade**
- **Título**: "Análise Interseccional de Internações"
- **Tipo**: Heatmap ou treemap (`px.treemap()`)
- **Hierarquia** (treemap): Raça/Cor → Sexo → Faixa Etária
- **Tamanho**: Proporção de internações
- **Cor**: Taxa de mortalidade
- **Interatividade**: Click para drill-down
- **Altura**: 500px

**Seção 6: Disparidades em Procedimentos**
- **Título**: "Acesso a Procedimentos de Alta Complexidade por Raça/Cor"
- **Filtro**: Selecionar categoria de procedimento (`st.selectbox()`)
- **Tipo**: Barras agrupadas
- **Dados**:
  - X: Procedimento específico (top 5 da categoria)
  - Y: Taxa por 10.000 internações
  - Grupo: Raça/Cor
- **Análise**: Identifica possíveis desigualdades no acesso
- **Altura**: 400px

**Seção 7: Tabela de Análise Detalhada**
- **Título**: "Indicadores por Raça/Cor - Visão Consolidada"
- **Componente**: `st.dataframe()`
- **Colunas**:
  - Raça/Cor
  - Total Internações
  - % do Total
  - Média Permanência (dias)
  - Taxa Mortalidade (%)
  - Custo Médio (R$)
  - Principal CID
  - % Uso UTI
- **Funcionalidades**: Ordenação, export CSV

**Seção 8: Análise Temporal de Equidade**
- **Título**: "Evolução das Internações por Raça/Cor"
- **Tipo**: Área empilhada (`px.area()`)
- **Dados**:
  - X: Mês/Ano
  - Y: Número de internações
  - Cor: Raça/Cor (cada uma uma área)
- **Opção**: Toggle para valores absolutos ou percentuais (%)
- **Altura**: 400px

---

## 📊 PAINEL 7: TEMPORAL / TENDÊNCIA

### Objetivo
Análise de séries temporais, sazonalidade e tendências de longo prazo.

### Estrutura de Layout

**Seção 1: Cards de Tendência**
- Usar `st.columns(4)`:
  1. **Tendência Geral**: ↗️ ou ↘️ + variação % no período
  2. **Mês com Maior Volume**: mês/ano + n
  3. **Sazonalidade Detectada**: Sim/Não + período (ex: "Pico no inverno")
  4. **Projeção Próximo Mês**: estimativa com IC 95%

**Seção 2: Série Temporal Principal**
- **Título**: "Evolução Completa de Internações no Período"
- **Tipo**: Linha com área preenchida (`px.area()` ou `px.line()` com fill)
- **Dados**:
  - X: Data (mensal)
  - Y: Número de internações
  - Cor: Azul com transparência
- **Elementos adicionais**:
  - Linha de tendência (regressão linear ou LOESS)
  - Média móvel de 3 meses (linha tracejada)
  - Bandas de confiança (se projeção disponível)
- **Interatividade**: Zoom, pan, hover detalhado
- **Altura**: 450px

**Seção 3: Decomposição de Série Temporal**
- **Título**: "Decomposição da Série: Tendência + Sazonalidade + Resíduo"
- **Tipo**: Subplot com 4 gráficos empilhados (`plotly.make_subplots()`)
- **Painéis** (de cima para baixo):
  1. Série Original
  2. Tendência (componente de longo prazo)
  3. Sazonalidade (padrão repetitivo)
  4. Resíduo (variação aleatória)
- **Método**: Decomposição sazonal (statsmodels ou similar)
- **Altura total**: 700px
- **Opção**: Toggle para decomposição aditiva ou multiplicativa

**Seção 4: Análise de Sazonalidade**
Usar `st.columns(2)`:

**Coluna Esquerda - Padrão Sazonal Mensal**
- **Título**: "Padrão Médio Mensal"
- **Tipo**: Barras (`px.bar()`)
- **Dados**:
  - X: Mês (Jan a Dez)
  - Y: Média de internações daquele mês em todos os anos
  - Cor: Gradiente conforme valor
- **Análise**: Identifica meses típicos de pico e baixa

**Coluna Direita - Boxplot por Mês**
- **Título**: "Distribuição de Internações por Mês"
- **Tipo**: Box plot
- **Dados**:
  - X: Mês
  - Y: Internações (todos os anos agregados)
- **Análise**: Mostra variabilidade dentro de cada mês

**Seção 5: Sazonalidade por Causa Específica**
- **Título**: "Análise Sazonal de Doenças Específicas"
- **Filtro**: `st.multiselect()` para escolher CIDs de interesse (máx 5)
  - Sugestões pré-definidas:
    - Doenças respiratórias (J00-J99)
    - Doenças cardiovasculares (I00-I99)
    - Causas externas (S00-T98)
- **Tipo**: Linha múltipla (`px.line()`)
- **Dados**:
  - X: Mês/Ano
  - Y: Número de casos
  - Cor: Cada CID uma linha
- **Normalização**: Opção de mostrar valores indexados (base 100 = média)
- **Altura**: 400px

**Seção 6: Análise de Tendência de Mortalidade**
- **Título**: "Evolução da Taxa de Mortalidade Hospitalar"
- **Tipo**: Linha com banda de confiança
- **Dados**:
  - X: Mês/Ano
  - Y: Taxa de mortalidade (%)
  - Banda: IC 95%
- **Elementos**:
  - Linha de tendência
  - Marca de eventos significativos (se houver, ex: "Mudança de protocolo")
- **Cor**: Vermelho
- **Altura**: 400px

**Seção 7: Heatmap Calendário**
- **Título**: "Calendário de Internações (Heatmap Anual)"
- **Tipo**: Heatmap estilo calendário
- **Dados**:
  - Linhas: Semanas do ano (1-52)
  - Colunas: Dia da semana (Dom-Sáb)
  - Valores: Número de internações
  - Cor: Escala branco → azul escuro
- **Filtro**: Seletor de ano (`st.selectbox()`)
- **Análise**: Padrões semanais e identificação de outliers
- **Altura**: 500px

**Seção 8: Análise de Crescimento/Decrescimento**
- **Título**: "Taxa de Variação Mensal"
- **Tipo**: Barras de variação (`px.bar()`)
- **Dados**:
  - X: Mês/Ano
  - Y: Variação % vs. mês anterior
  - Cor: Verde (positivo) / Vermelho (negativo)
- **Linha de referência**: 0%
- **Altura**: 350px

**Seção 9: Projeção Futura (Opcional)**
- **Título**: "Projeção de Internações (Próximos 6 Meses)"
- **Tipo**: Linha com área de incerteza
- **Dados**:
  - Linha sólida: Dados históricos
  - Linha tracejada: Projeção
  - Área sombreada: Intervalo de confiança 95%
- **Método**: ARIMA, Prophet, ou regressão simples
- **Cores**: Azul (histórico), cinza (projeção)
- **Aviso**: `st.info()` explicando limitações da projeção
- **Altura**: 400px

**Seção 10: Tabela de Estatísticas Descritivas**
- **Título**: "Estatísticas Mensais"
- **Componente**: `st.dataframe()`
- **Colunas**:
  - Mês/Ano
  - Total Internações
  - Variação % MoM
  - Variação % YoY
  - Taxa Mortalidade
  - Custo Total
  - Média Permanência
- **Funcionalidades**: Ordenação, export CSV

---

## 🛠️ FUNCIONALIDADES TRANSVERSAIS

### Sistema de Download de Dados
- **Localização**: Em cada painel, botão `st.download_button()` no topo ou rodapé
- **Formatos disponíveis**:
  - CSV (`,` como separador, encoding UTF-8)
  - Excel (.xlsx) com formatação preservada
- **Opções**:
  - Download de dados filtrados (conforme filtros aplicados)
  - Download de dados completos do painel
  - Nome do arquivo: `[nome_painel]_[data].[extensão]`

### Exportação de Visualizações
- **Método**: Usar funcionalidade nativa do Plotly (botão de camera)
- **Formatos**: PNG (padrão), SVG (qualidade vetorial)
- **Configuração**: `config={'displayModeBar': True, 'displaylogo': False}`

### Sistema de Notificações
- Usar `st.info()`, `st.success()`, `st.warning()`, `st.error()` para:
  - Feedback de ações (ex: "Filtros aplicados com sucesso")
  - Avisos sobre dados (ex: "10 municípios com dados incompletos foram excluídos")
  - Erros de validação (ex: "Período inválido selecionado")

### Metadados e Documentação
- **Aba adicional no menu**: "📚 Sobre o Dashboard"
- **Conteúdo**:
  - **Fonte de dados**: SIH/DATASUS
  - **Período disponível**: Exibir dinamicamente
  - **Tratamento**: Mencionar uso do pacote `microdatasus` ou `PySUS`
  - **Definição dos indicadores**:
    - Taxa de mortalidade = (Óbitos / Total internações) × 100
    - Média de permanência = Soma dias / Total AIHs
    - Custo médio = Valor total / Total AIHs
    - Taxa de UTI = Dias UTI / Total dias × 100
  - **Referências técnicas**:
    - Link para documentação DATASUS
    - Citação acadêmica (ex: Saldanha et al., 2019)
  - **Limitações conhecidas**: Listar eventuais gaps nos dados
  - **Contato/Feedback**: Email ou link para repositório GitHub

### Performance e Otimização
- **Cache de dados**: Usar `@st.cache_data` para:
  - Leitura do arquivo de dados
  - Agregações pesadas
  - Cálculos de indicadores
- **Cache de visualizações**: Quando aplicável
- **Lazy loading**: Carregar painéis sob demanda (não pré-processar todos)
- **Spinner**: `st.spinner()` durante operações demoradas

---

## 📦 REQUISITOS TÉCNICOS

### Bibliotecas Python Necessárias
```python
# Core
streamlit >= 1.28
pandas >= 2.0
numpy >= 1.24

# Visualização
plotly >= 5.17
folium >= 0.14
streamlit-folium >= 0.15

# Análise
statsmodels >= 0.14  # decomposição de séries
scikit-learn >= 1.3  # se usar ML

# Dados
microdatasus >= 2.0  # ou PySUS
openpyxl >= 3.1  # para Excel

# Opcional
prophet >= 1.1  # para projeções avançadas
geopandas >= 0.14  # para mapas avançados
```

### Estrutura de Dados Esperada

**Colunas Essenciais no DataFrame**:
- `ANO_CMPT`: Ano competência
- `MES_CMPT`: Mês competência
- `UF_ZI`: UF de residência
- `MUNIC_RES`: Município de residência (código IBGE)
- `MUNIC_MOV`: Município de atendimento (código IBGE)
- `CNES`: Código do estabelecimento
- `NOME_FANTASIA`: Nome do estabelecimento
- `DIAS_PERM`: Dias de permanência
- `DIAS_UTI`: Dias em UTI
- `MORTE`: Óbito (0=Não, 1=Sim)
- `CID_PRINC`: Diagnóstico principal (CID-10)
- `CID_SECUN`: Diagnóstico secundário
- `CID_MORTE`: Causa do óbito
- `PROC_SOLI`: Procedimento solicitado (SIGTAP)
- `PROC_REA`: Procedimento realizado (SIGTAP)
- `VAL_TOT`: Valor total da AIH
- `SEXO`: Sexo do paciente
- `IDADE`: Idade ou faixa etária
- `RACA_COR`: Raça/Cor (IBGE)

**Tratamento de Dados**:
- Conversão de tipos apropriados
- Tratamento de valores ausentes
- Criação de variáveis derivadas (ex: taxa de mortalidade)
- Merge com tabelas auxiliares (nomes de municípios, descrições CID, etc.)

---

## 🎯 FLUXO DE NAVEGAÇÃO SUGERIDO

1. Usuário abre o dashboard → **Painel Geral** (visão macro)
2. Aplica filtros na sidebar conforme interesse
3. Navega para painéis específicos:
   - Gestor → Geral, Estabelecimento, Custos
   - Epidemiologista → Epidemiológico, Temporal, População
   - Regulador → Regulação e Território
4. Exporta dados e gráficos de interesse
5. Consulta metodologia na aba "Sobre"

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [ ] Estrutura básica do Streamlit com sidebar
- [ ] Sistema de filtros globais funcionais
- [ ] Painel 1: Geral (KPIs + série temporal + mapa)
- [ ] Painel 2: Epidemiológico (CIDs + pirâmide + mortalidade)
- [ ] Painel 3: Regulação (mapa de fluxo + matriz)
- [ ] Painel 4: Estabelecimentos (ranking + perfil + scatter)
- [ ] Painel 5: Procedimentos (top procedures + heatmap CID×Proc)
- [ ] Painel 6: População (raça/cor + equidade)
- [ ] Painel 7: Temporal (séries + sazonalidade + tendência)
- [ ] Funcionalidades de download (CSV e Excel)
- [ ] Aba de documentação/metodologia
- [ ] Otimizações de performance (cache)
- [ ] Testes de responsividade e UX
- [ ] Deploy (Streamlit Cloud, Heroku, ou similar)

---

## 📝 NOTAS FINAIS PARA IMPLEMENTAÇÃO

**Para o Claude Code**:
- Este documento contém especificações DETALHADAS de cada elemento
- Implemente os painéis na ordem sugerida (Geral → Temporal)
- Priorize funcionalidade sobre estética inicialmente
- Use Plotly para TODAS as visualizações (consistência)
- Teste cada filtro para garantir que afeta todos os painéis
- Mantenha código modular (funções separadas para cada gráfico)
- Documente funções complexas com docstrings
- Valide os dados antes de gerar visualizações (evitar crashes)

**Boas práticas Streamlit**:
- Evite recarregar dados a cada interação (use cache)
- Use `st.columns()` para layouts responsivos
- Prefira `st.plotly_chart()` com `use_container_width=True`
- Organize código em múltiplos arquivos se necessário (pages/)

---

**Documento criado para desenvolvimento de Dashboard SIH/DATASUS**  
**Tecnologia**: Streamlit + Python  
**Versão**: 1.0 - Especificação Completa para Implementação