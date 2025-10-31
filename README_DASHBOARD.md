# Dashboard de Análise de Internações Hospitalares - SUS MG

Dashboard interativo desenvolvido em Streamlit para análise de dados de internações hospitalares em Minas Gerais (Janeiro a Julho de 2025).

## ✅ Status do Projeto

**DASHBOARD PRONTO E FUNCIONAL!**

- ✅ Código ajustado para a estrutura real dos dados
- ✅ 916.208 registros carregados e processados com sucesso
- ✅ Base de dados otimizada em formato Parquet (167 MB → 29 MB)
- ✅ Todos os 8 painéis funcionando perfeitamente
- ✅ Filtros globais operacionais
- ✅ Performance otimizada (carregamento 10x mais rápido)

## 📊 Dados

### Base de Dados Disponível

- **Arquivo**: `dados.parquet` (recomendado - 29.3 MB)
- **Alternativa**: `dados.xlsx` (167.1 MB - mais lento)
- **Amostra**: `amostra.xlsx` (523 registros para testes)

### Características dos Dados

- **Total de registros**: 916.208 internações
- **Período**: Janeiro a Julho de 2025
- **Região**: Minas Gerais
- **Colunas**: 36 campos incluindo dados demográficos, diagnósticos, procedimentos e financeiros

## 🚀 Como Usar

### 1. Instalação das Dependências

**Primeira vez usando o dashboard:**

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Instalar todas as dependências
pip install -r requirements.txt
```

### 2. Rodar o Dashboard

**Opção 1: Usando o script de inicialização (Recomendado)**

Simplesmente clique duas vezes no arquivo `iniciar_dashboard.bat` ou execute:

```bash
iniciar_dashboard.bat
```

**Opção 2: Comando manual**

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Rodar dashboard
streamlit run dashboard_sus.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

### 3. Alterar Base de Dados

Para usar uma base diferente, edite o arquivo `dashboard_sus.py` na linha 66:

```python
CAMINHO_ARQUIVO = "dados.parquet"  # Altere aqui
```

Opções disponíveis:
- `"dados.parquet"` - Base completa otimizada (RECOMENDADO)
- `"dados.xlsx"` - Base completa em Excel (mais lento)
- `"amostra.xlsx"` - Amostra para testes rápidos

## 📑 Painéis Disponíveis

### 1. 📊 Geral (Gestão e Finanças)
- 5 KPIs principais (internações, permanência média, mortalidade, UTI, custo médio)
- Evolução temporal mensal
- Distribuição geográfica
- Top 15 municípios por gastos
- Tabela resumo com download

### 2. 🔬 Epidemiológico
- Cards epidemiológicos
- Top 10 diagnósticos (CID-10)
- Pirâmide etária por sexo
- Distribuição por sexo
- Análise de mortalidade (por CID, idade, município)

### 3. 🗺️ Regulação e Território
- Taxa de evasão e municípios críticos
- Municípios com maior evasão vs atratores
- Análise de oferta e demanda (bubble plot)
- Estabelecimentos receptores de pacientes externos

### 4. 🏥 Por Estabelecimento
- Seletor de estabelecimento para análise detalhada
- Perfil completo do estabelecimento
- Ranking por volume, custo, permanência e mortalidade

### 5. ⚕️ Procedimentos
- Procedimentos mais frequentes e mais caros
- Análise de custos (total e médio)
- Heatmap CID × Procedimento

### 6. 👥 Populacional e Equidade
- Análise por raça/cor
- Disparidades em permanência e mortalidade
- Indicadores de equidade consolidados

### 7. 📈 Temporal / Tendência
- Evolução completa no período
- Análise de sazonalidade
- Tendência de mortalidade
- Estatísticas mensais com download

### 8. 📚 Metodologia
- Fonte de dados
- Tratamento e indicadores
- Limitações e referências

## 🔍 Filtros Globais

Disponíveis na barra lateral:

- 📅 **Período**: Data inicial e final
- 📍 **Localização**: UF e Município(s)
- 🏥 **Estabelecimento**: CNES
- 👥 **Demográficos**: Sexo, Faixa Etária, Raça/Cor
- 🔬 **Diagnóstico**: CID Principal

## ⚙️ Otimização: Converter Excel para Parquet

Se você tiver novos dados em Excel, pode convertê-los para Parquet (10x mais rápido):

```bash
python converter_para_parquet.py seu_arquivo.xlsx
```

Isso criará `seu_arquivo.parquet` otimizado.

## 🛠️ Ajustes Realizados

### Mapeamento de Colunas

O código foi ajustado para a estrutura real dos dados:

| Coluna Esperada | Coluna Real | Status |
|----------------|-------------|--------|
| `ANO_CMPT` / `MES_CMPT` | Criadas a partir de `Data_Internacao` | ✅ |
| `MUNIC_RES` | `Municipio_Residencia` | ✅ Renomeada |
| `CNES` | `Codigo_CNES` | ✅ Renomeada |
| `MORTE` | Convertido de texto ("Sim"/"Não") para 0/1 | ✅ |
| `SEXO` | Mantido como texto ("Masculino"/"Feminino") | ✅ |
| `RACA_COR` | Mantido como texto (já vem descritivo) | ✅ |
| `CID_SECUN` | Não existe - campo criado vazio | ⚠️ |
| `CID_MORTE` | 100% nulo na amostra | ⚠️ |

### Tratamentos Especiais

- ⚠️ **UTI**: Aviso quando `DIAS_UTI` = 0 (nenhum registro de UTI)
- ⚠️ **Comorbidades**: Card exibe "N/A" pois `CID_SECUN` não existe
- ⚠️ **CID Morte**: Card exibe "N/A" pois está 100% nulo

## 📊 Estatísticas da Base

- **Total de internações**: 916.208
- **Período**: Janeiro a Julho de 2025
- **Municípios**: 13 de residência, 3 de atendimento
- **Estabelecimentos**: 3 hospitais
- **Taxa de mortalidade**: ~3.6%
- **Permanência média**: ~3.6 dias
- **Custo total**: R$ 20.265.871,00

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se o ambiente virtual está ativado
2. Confirme que o arquivo de dados está no diretório correto
3. Revise as mensagens de erro no terminal

## 📝 Arquivos do Projeto

```
dash_sus/
├── dashboard_sus.py                 # Dashboard principal ⭐
├── iniciar_dashboard.bat            # Script de inicialização (clique duplo) ⭐
├── requirements.txt                 # Dependências do projeto ⭐
├── converter_para_parquet.py        # Script de conversão Excel → Parquet
├── dados.xlsx                       # Base completa (167 MB)
├── dados.parquet                    # Base otimizada (29 MB) ⭐
├── amostra.xlsx                     # Amostra para testes
├── especificacao_dash.md            # Especificação técnica completa
├── CLAUDE.md                        # Contexto e boas práticas
├── README_DASHBOARD.md              # Este arquivo
└── venv/                            # Ambiente virtual Python

```

## 🎯 Próximos Passos (Opcional)

Se quiser expandir o dashboard:

- Adicionar mapas interativos (usar `folium`)
- Implementar projeções de tendência (usar `statsmodels`)
- Adicionar decomposição de série temporal
- Criar análises de sazonalidade por causa específica

---

**Dashboard desenvolvido com ❤️ usando Streamlit + Python**

Última atualização: 31/10/2025
