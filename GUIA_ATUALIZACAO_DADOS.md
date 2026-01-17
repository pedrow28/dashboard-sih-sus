# 📊 Guia de Atualização Periódica dos Dados - Dashboard SUS

> **Objetivo**: Este documento fornece instruções passo-a-passo para atualizar os dados do Dashboard SUS com novas informações mensais do DATASUS.

---

## 📋 Índice

1. [Visão Geral do Processo](#visão-geral-do-processo)
2. [Pré-requisitos](#pré-requisitos)
3. [Atualização Passo-a-Passo](#atualização-passo-a-passo)
4. [Validação dos Dados](#validação-dos-dados)
5. [Troubleshooting](#troubleshooting)
6. [Automação (Opcional)](#automação-opcional)
7. [Cronograma Sugerido](#cronograma-sugerido)
8. [Checklist Rápida](#checklist-rápida)

---

## 🔄 Visão Geral do Processo

O processo de atualização envolve **3 etapas principais**:

```
┌─────────────────────────────────────────────────────────┐
│ ETAPA 1: Extração de Dados (R)                         │
│ • Executar script R Markdown                            │
│ • Buscar dados do DATASUS                               │
│ • Processar e enriquecer dados                          │
│ • Exportar dados.xlsx                                   │
│ Tempo estimado: 10-15 minutos                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ETAPA 2: Otimização (Python)                           │
│ • Converter Excel para Parquet                          │
│ • Compressão e otimização de tipos                      │
│ • Gerar dados.parquet                                   │
│ Tempo estimado: 2-5 minutos                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ETAPA 3: Validação e Publicação                        │
│ • Validar integridade dos dados                         │
│ • Testar dashboard                                      │
│ • Documentar atualização                                │
│ Tempo estimado: 5 minutos                               │
└─────────────────────────────────────────────────────────┘

TEMPO TOTAL ESTIMADO: 20-25 minutos
```

---

## ✅ Pré-requisitos

### 1. Ambiente R

Certifique-se de que o **R e RStudio** estão instalados e configurados:

```r
# Versão mínima recomendada: R 4.0+
R.version.string

# Pacotes necessários (verificar instalação)
installed.packages()[c("microdatasus", "tidyverse", "writexl", "DT", "plotly"), ]
```

**Se algum pacote estiver faltando, instale:**

```r
# Instalar pacotes ausentes
install.packages(c("tidyverse", "writexl", "DT", "plotly"))

# Pacote microdatasus (pode exigir instalação especial)
install.packages("microdatasus")

# Se houver erro, tente via GitHub:
# install.packages("remotes")
# remotes::install_github("rfsaldanha/microdatasus")
```

### 2. Ambiente Python

Verifique a instalação do ambiente virtual Python:

```bash
# Ativar ambiente virtual
cd C:\Users\pedro\Projetos\dash_sus
venv\Scripts\activate

# Verificar pacotes essenciais
pip list | findstr "pandas pyarrow streamlit"

# Se faltarem, instalar:
pip install -r requirements.txt
```

### 3. Arquivos Auxiliares

Certifique-se de que os seguintes arquivos estão disponíveis:

- ✅ `Painel DataSUS.Rmd` (script R de extração)
- ✅ `converter_para_parquet.py` (script de conversão)
- ✅ `CID-10-SUBCATEGORIAS.CSV` (tabela de doenças CID-10)

> ⚠️ **IMPORTANTE**: O arquivo `CID-10-SUBCATEGORIAS.CSV` deve estar no mesmo diretório ou o caminho deve ser ajustado no script R.

---

## 🔧 Atualização Passo-a-Passo

### ETAPA 1: Extração de Dados via R

#### Passo 1.1: Abrir o Script R

1. Abra o **RStudio**
2. Navegue até: `File > Open File...`
3. Selecione: `C:\Users\pedro\Projetos\dash_sus\Painel DataSUS.Rmd`

#### Passo 1.2: Atualizar Período dos Dados

Localize a seção de extração de dados (aproximadamente linhas 50-60) e **atualize o período desejado**:

```r
# EDITAR ESTAS LINHAS:
dados_raw <- fetch_datasus(
  year_start = 2025,      # ← Ano inicial
  year_end = 2025,        # ← Ano final
  month_start = 1,        # ← Mês inicial (1-12)
  month_end = 7,          # ← Mês final (1-12) **ATUALIZAR AQUI**
  uf = "MG",              # ← Estado (manter "MG")
  information_system = "SIH-RD"  # ← Sistema (manter)
)
```

**Exemplo para atualizar até agosto de 2025:**
```r
month_end = 8,  # ← Mudança de 7 para 8
```

**Exemplo para incluir todo o ano de 2025:**
```r
month_end = 12,  # ← Janeiro a Dezembro
```

#### Passo 1.3: Executar o Script

Existem duas formas de executar:

**Opção A: Executar tudo de uma vez (Recomendado)**
1. Clique em **"Knit"** no topo do RStudio
2. Aguarde o processamento (pode levar 10-15 minutos)
3. Um arquivo HTML será gerado como saída (opcional)

**Opção B: Executar chunk por chunk**
1. Use `Ctrl + Shift + Enter` para executar cada chunk de código
2. Monitore o progresso no console
3. Verifique possíveis erros em cada etapa

#### Passo 1.4: Verificar Saída

Ao final da execução, verifique:

- ✅ Arquivo `dados.xlsx` foi criado/atualizado no diretório do projeto
- ✅ Tamanho do arquivo é consistente (esperado: 150-200 MB)
- ✅ Mensagens no console indicam sucesso
- ✅ Sem erros críticos de download ou processamento

**Exemplo de mensagem de sucesso:**
```
Processando dados SIH...
Enriquecendo com municípios...
Adicionando nomes de procedimentos...
Exportando para Excel...
Concluído! 916208 registros exportados.
```

---

### ETAPA 2: Conversão para Parquet

#### Passo 2.1: Ativar Ambiente Python

Abra o **Terminal/Prompt de Comando** e execute:

```bash
cd C:\Users\pedro\Projetos\dash_sus
venv\Scripts\activate
```

#### Passo 2.2: Executar Conversão

Execute o script de conversão:

```bash
python converter_para_parquet.py dados.xlsx
```

**Saída esperada:**
```
Carregando arquivo Excel: dados.xlsx
Tamanho do arquivo Excel: 167.1 MB
Linhas carregadas: 916208

Otimizando tipos de dados...
Convertendo colunas categóricas...
Convertendo datas...

Salvando em formato Parquet...
Arquivo salvo: dados.parquet
Tamanho do arquivo Parquet: 29.3 MB
Redução de tamanho: 82.5%

Conversão concluída com sucesso!
```

#### Passo 2.3: Verificar Saída

Confirme que o arquivo foi criado:

```bash
# Windows
dir dados.parquet

# Deve mostrar arquivo de ~30 MB com data/hora recente
```

---

### ETAPA 3: Validação e Publicação

#### Passo 3.1: Validação Automática (Script Python)

Crie e execute um script de validação rápida:

```bash
python validar_dados.py
```

**Se o script não existir ainda**, você pode fazer validação manual abrindo o Python:

```python
import pandas as pd

# Carregar dados
df = pd.read_parquet('dados.parquet')

# Validações básicas
print(f"Total de registros: {len(df):,}")
print(f"Período: {df['Data_Internacao'].min()} a {df['Data_Internacao'].max()}")
print(f"Total de municípios: {df['Nome_Municipio_Residencia'].nunique()}")
print(f"Total de estabelecimentos: {df['Nome_Estabelecimento'].nunique()}")
print(f"Valores nulos por coluna:")
print(df.isnull().sum()[df.isnull().sum() > 0])
print("\n✅ Validação concluída!")
```

**Valores esperados para Jan-Jul 2025:**
- Registros: ~916.000 (varia conforme mês final)
- Municípios: ~850 (total de municípios em MG)
- Período: 2025-01-01 a 2025-07-31 (ou data final atualizada)

#### Passo 3.2: Testar Dashboard

Inicie o dashboard para garantir que tudo funciona:

```bash
# Opção 1: Script batch
iniciar_dashboard_v2.bat

# Opção 2: Comando direto
streamlit run dashboard_sus_v2.py
```

**Checklist de testes:**
- ✅ Dashboard abre sem erros
- ✅ Métricas principais carregam corretamente
- ✅ Filtros funcionam
- ✅ Período exibido corresponde aos dados atualizados
- ✅ Gráficos renderizam corretamente
- ✅ Não há mensagens de erro no console

#### Passo 3.3: Documentar Atualização

Registre a atualização em um arquivo de log:

```bash
# Criar/atualizar arquivo HISTORICO_ATUALIZACOES.md
echo "## Atualização [DATA]" >> HISTORICO_ATUALIZACOES.md
echo "- Período dos dados: Janeiro a [MÊS] 2025" >> HISTORICO_ATUALIZACOES.md
echo "- Total de registros: [NÚMERO]" >> HISTORICO_ATUALIZACOES.md
echo "- Responsável: [SEU NOME]" >> HISTORICO_ATUALIZACOES.md
echo "- Observações: [ALGUMA NOTA RELEVANTE]" >> HISTORICO_ATUALIZACOES.md
echo "" >> HISTORICO_ATUALIZACOES.md
```

---

## 🔍 Validação dos Dados

### Checklist de Validação Completa

Execute estas verificações após cada atualização:

#### 1. Integridade Estrutural

```python
import pandas as pd

df = pd.read_parquet('dados.parquet')

# 1. Verificar colunas esperadas
colunas_esperadas = [
    'Data_Internacao', 'Data_Saida', 'Municipio_Residencia',
    'Nome_Municipio_Residencia', 'Nome_Estabelecimento',
    'Procedimento_Realizado', 'Nome_Procedimento_Realizado',
    'Diagnostico_Principal', 'Nome_Doenca', 'Valor_Total',
    'Dias_Permanencia', 'Sexo', 'Idade', 'Morte'
]

faltando = set(colunas_esperadas) - set(df.columns)
if faltando:
    print(f"⚠️ Colunas faltando: {faltando}")
else:
    print("✅ Todas as colunas essenciais presentes")
```

#### 2. Qualidade dos Dados

```python
# 2. Verificar valores nulos críticos
colunas_criticas = ['Data_Internacao', 'Municipio_Residencia', 'Valor_Total']
for col in colunas_criticas:
    nulos = df[col].isnull().sum()
    pct = (nulos / len(df)) * 100
    if pct > 5:
        print(f"⚠️ {col}: {pct:.2f}% nulos (acima do esperado)")
    else:
        print(f"✅ {col}: {pct:.2f}% nulos")

# 3. Verificar intervalo de datas
print(f"\n📅 Período dos dados: {df['Data_Internacao'].min()} a {df['Data_Internacao'].max()}")

# 4. Verificar valores negativos inválidos
if (df['Valor_Total'] < 0).any():
    print("⚠️ Valores negativos detectados em Valor_Total")
else:
    print("✅ Sem valores negativos em Valor_Total")

if (df['Dias_Permanencia'] < 0).any():
    print("⚠️ Valores negativos em Dias_Permanencia")
else:
    print("✅ Sem valores negativos em Dias_Permanencia")

# 5. Verificar categorias esperadas
print(f"\n👥 Sexo: {df['Sexo'].value_counts().to_dict()}")
print(f"💀 Morte: {df['Morte'].value_counts().to_dict()}")
```

#### 3. Comparação com Mês Anterior

```python
# Carregar dados anteriores (se existir backup)
df_anterior = pd.read_parquet('dados_backup.parquet')

print("\n📊 Comparação com versão anterior:")
print(f"Registros anteriores: {len(df_anterior):,}")
print(f"Registros novos: {len(df):,}")
print(f"Diferença: {len(df) - len(df_anterior):,} ({((len(df)/len(df_anterior) - 1) * 100):.2f}%)")
```

---

## ⚠️ Troubleshooting

### Problema 1: Erro ao executar fetch_datasus()

**Sintoma:**
```
Error in fetch_datasus(): Could not connect to server
```

**Soluções:**
1. Verifique sua conexão com a internet
2. Tente novamente em alguns minutos (servidores DATASUS podem estar instáveis)
3. Verifique se o período solicitado está disponível (dados podem ter delay de publicação)
4. Tente baixar um período menor (ex: 1 mês por vez)

**Código alternativo para download em lotes:**
```r
# Baixar mês por mês
dados_completo <- data.frame()

for (mes in 1:7) {
  print(paste("Baixando mês", mes))

  dados_mes <- fetch_datasus(
    year_start = 2025,
    year_end = 2025,
    month_start = mes,
    month_end = mes,
    uf = "MG",
    information_system = "SIH-RD"
  )

  dados_completo <- rbind(dados_completo, dados_mes)
  Sys.sleep(5)  # Pausa de 5 segundos entre requisições
}
```

---

### Problema 2: Erro "CID-10-SUBCATEGORIAS.CSV not found"

**Sintoma:**
```
Error: 'CID-10-SUBCATEGORIAS.CSV' does not exist
```

**Soluções:**
1. Verifique se o arquivo está no diretório correto
2. Baixe novamente de: [fonte do arquivo CID-10]
3. Ajuste o caminho no script R:

```r
# Procure esta linha no Rmd e ajuste o caminho:
cid10 <- read.csv("caminho/completo/para/CID-10-SUBCATEGORIAS.CSV",
                  encoding = "UTF-8")
```

---

### Problema 3: Conversão para Parquet falha

**Sintoma:**
```
pyarrow.lib.ArrowInvalid: Could not convert
```

**Soluções:**
1. Verifique se o arquivo Excel não está aberto em outro programa
2. Confirme que o pyarrow está instalado:
   ```bash
   pip install --upgrade pyarrow
   ```
3. Tente com compressão alternativa:
   ```python
   # Editar converter_para_parquet.py, linha de salvamento:
   df.to_parquet('dados.parquet', compression='gzip')  # Ao invés de snappy
   ```

---

### Problema 4: Dashboard não carrega dados atualizados

**Sintoma:**
Dashboard mostra dados antigos após atualização

**Soluções:**
1. Limpar cache do Streamlit:
   ```bash
   # No navegador, pressione 'C' ou use menu "Clear cache"
   ```
2. Reiniciar completamente o dashboard:
   ```bash
   # Ctrl+C no terminal para parar
   # Executar novamente:
   streamlit run dashboard_sus_v2.py
   ```
3. Verificar se `dados.parquet` foi realmente atualizado:
   ```bash
   # Windows: verificar data de modificação
   dir dados.parquet
   ```

---

### Problema 5: Memória insuficiente

**Sintoma:**
```
MemoryError: Unable to allocate array
```

**Soluções:**
1. Fechar outros programas
2. Processar dados em chunks (editar converter_para_parquet.py):
   ```python
   # Ao invés de:
   df = pd.read_excel('dados.xlsx')

   # Use:
   chunks = pd.read_excel('dados.xlsx', chunksize=100000)
   df = pd.concat(chunks, ignore_index=True)
   ```
3. Aumentar memória virtual do sistema (Windows)

---

## 🤖 Automação (Opcional)

### Opção 1: Script Batch Completo (Windows)

Crie um arquivo `atualizar_dados_completo.bat`:

```batch
@echo off
echo ============================================
echo  ATUALIZACAO AUTOMATICA - DASHBOARD SUS
echo ============================================
echo.

REM Passo 1: Executar script R
echo [1/3] Executando extracao de dados via R...
"C:\Program Files\R\R-4.3.0\bin\Rscript.exe" -e "rmarkdown::render('Painel DataSUS.Rmd')"
if %errorlevel% neq 0 (
    echo ERRO na extracao de dados!
    pause
    exit /b 1
)
echo Extracao concluida!
echo.

REM Passo 2: Converter para Parquet
echo [2/3] Convertendo para Parquet...
call venv\Scripts\activate.bat
python converter_para_parquet.py dados.xlsx
if %errorlevel% neq 0 (
    echo ERRO na conversao!
    pause
    exit /b 1
)
echo Conversao concluida!
echo.

REM Passo 3: Validação
echo [3/3] Validando dados...
python validar_dados.py
echo.

echo ============================================
echo  ATUALIZACAO CONCLUIDA COM SUCESSO!
echo ============================================
pause
```

**Uso:**
```bash
# Duplo clique em atualizar_dados_completo.bat
# Ou via terminal:
atualizar_dados_completo.bat
```

---

### Opção 2: Agendamento via Task Scheduler (Windows)

Para executar automaticamente todo mês:

1. Abra **Task Scheduler** (Agendador de Tarefas)
2. Clique em "Create Basic Task" (Criar Tarefa Básica)
3. Configure:
   - **Nome**: Atualização Dashboard SUS
   - **Trigger**: Monthly (Mensal)
   - **Dia**: 10 (aguardar disponibilização dos dados pelo DATASUS)
   - **Hora**: 03:00 AM
   - **Action**: Start a program
   - **Program**: `C:\Users\pedro\Projetos\dash_sus\atualizar_dados_completo.bat`
4. Salve a tarefa

**Notificação por email (avançado):**
Adicione ao final do script batch:

```batch
REM Enviar email de notificação (requer configuração SMTP)
python enviar_notificacao.py "Atualização concluída com sucesso"
```

---

### Opção 3: Script Python Unificado

Crie `atualizar_pipeline.py`:

```python
import subprocess
import sys
from datetime import datetime

def executar_comando(comando, descricao):
    """Executa comando e retorna status"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {descricao}")
    print('='*60)

    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

    if resultado.returncode != 0:
        print(f"❌ ERRO: {resultado.stderr}")
        return False

    print(f"✅ Concluído!")
    print(resultado.stdout)
    return True

def main():
    # Etapa 1: Executar R
    if not executar_comando(
        'Rscript -e "rmarkdown::render(\'Painel DataSUS.Rmd\')"',
        "Extraindo dados do DATASUS via R"
    ):
        sys.exit(1)

    # Etapa 2: Converter Parquet
    if not executar_comando(
        'python converter_para_parquet.py dados.xlsx',
        "Convertendo para formato Parquet"
    ):
        sys.exit(1)

    # Etapa 3: Validar
    if not executar_comando(
        'python validar_dados.py',
        "Validando integridade dos dados"
    ):
        sys.exit(1)

    print("\n" + "="*60)
    print("🎉 PIPELINE DE ATUALIZAÇÃO CONCLUÍDO COM SUCESSO!")
    print("="*60)

if __name__ == "__main__":
    main()
```

**Uso:**
```bash
python atualizar_pipeline.py
```

---

## 📅 Cronograma Sugerido

### Frequência de Atualização

**Recomendação: Mensal**

- **Dia sugerido**: 10 de cada mês
- **Razão**: DATASUS publica dados com ~1-2 semanas de atraso

### Calendário Anual 2025

| Mês | Data de Atualização | Período Coberto | Status |
|-----|---------------------|-----------------|--------|
| Janeiro | 10/02/2025 | Jan/2025 | ✅ Concluído |
| Fevereiro | 10/03/2025 | Jan-Fev/2025 | ✅ Concluído |
| Março | 10/04/2025 | Jan-Mar/2025 | ✅ Concluído |
| Abril | 10/05/2025 | Jan-Abr/2025 | ✅ Concluído |
| Maio | 10/06/2025 | Jan-Mai/2025 | ✅ Concluído |
| Junho | 10/07/2025 | Jan-Jun/2025 | ✅ Concluído |
| Julho | 10/08/2025 | Jan-Jul/2025 | ✅ Concluído |
| Agosto | 10/09/2025 | Jan-Ago/2025 | 📅 Pendente |
| Setembro | 10/10/2025 | Jan-Set/2025 | 📅 Pendente |
| Outubro | 10/11/2025 | Jan-Out/2025 | 📅 Pendente |
| Novembro | 10/12/2025 | Jan-Nov/2025 | 📅 Pendente |
| Dezembro | 10/01/2026 | 2025 completo | 📅 Pendente |

---

## ✅ Checklist Rápida

Use esta checklist para cada atualização:

### Antes de Começar
- [ ] RStudio instalado e funcionando
- [ ] Python virtual environment ativado
- [ ] Conexão com internet estável
- [ ] Arquivo CID-10-SUBCATEGORIAS.CSV disponível
- [ ] Backup dos dados anteriores realizado

### Durante o Processo
- [ ] Atualizar `month_end` no script R
- [ ] Executar `Painel DataSUS.Rmd` sem erros
- [ ] Verificar geração de `dados.xlsx` (~150-200 MB)
- [ ] Executar `converter_para_parquet.py`
- [ ] Verificar geração de `dados.parquet` (~30 MB)

### Validação
- [ ] Total de registros compatível com período
- [ ] Período de datas correto
- [ ] Sem erros ao abrir dashboard
- [ ] KPIs principais fazem sentido
- [ ] Filtros funcionam corretamente
- [ ] Gráficos renderizam sem erros

### Pós-Atualização
- [ ] Documentar atualização em histórico
- [ ] Fazer backup dos arquivos anteriores
- [ ] Notificar usuários (se aplicável)
- [ ] Atualizar documentação se necessário

---

## 📞 Suporte e Contatos

**Problemas técnicos:**
- Email: pedrowilliamrd@gmail.com
- GitHub Issues: [criar issue no repositório]

**Recursos úteis:**
- Documentação DATASUS: https://datasus.saude.gov.br/
- Pacote microdatasus: https://github.com/rfsaldanha/microdatasus
- Streamlit Docs: https://docs.streamlit.io/

---

## 📝 Histórico de Revisões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 02/11/2025 | Pedro William | Versão inicial do guia |

---

**Última atualização**: Novembro 2025
