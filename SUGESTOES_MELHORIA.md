# 🚀 Sugestões de Expansão e Melhoria - Dashboard SUS

> **Objetivo**: Este documento apresenta um roadmap estruturado de melhorias, expansões e evoluções possíveis para o projeto Dashboard SUS, organizadas por prioridade e esforço estimado.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Matriz de Priorização](#matriz-de-priorização)
3. [Melhorias de Curto Prazo (Quick Wins)](#melhorias-de-curto-prazo-quick-wins)
4. [Automação do Pipeline de Dados](#automação-do-pipeline-de-dados)
5. [Expansões Analíticas Avançadas](#expansões-analíticas-avançadas)
6. [Melhorias de UX/UI](#melhorias-de-uxui)
7. [Integrações e APIs](#integrações-e-apis)
8. [Infraestrutura e Escalabilidade](#infraestrutura-e-escalabilidade)
9. [Alternativas Tecnológicas](#alternativas-tecnológicas)
10. [Roadmap Sugerido](#roadmap-sugerido)

---

## 🎯 Visão Geral

O Dashboard SUS já é uma **aplicação funcional e robusta**, mas há diversas oportunidades de evolução que podem:

- ✅ **Reduzir trabalho manual** através de automação
- ✅ **Aumentar valor analítico** com machine learning e previsões
- ✅ **Melhorar experiência do usuário** com design moderno e responsivo
- ✅ **Expandir alcance** com APIs e integrações
- ✅ **Otimizar custos** com infraestrutura em nuvem

---

## 📊 Matriz de Priorização

```
                    ALTO IMPACTO
                         │
        ┌────────────────┼────────────────┐
        │   QUICK WINS   │  ESTRATÉGICAS  │
        │                │                │
BAIXO   │  • Validação   │  • Automação   │   ALTO
ESFORÇO │  • Scripts     │  • ML/IA       │   ESFORÇO
        │  • Docs        │  • Cloud       │
        ├────────────────┼────────────────┤
        │   BAIXA PRIO   │  GRANDES PROJ  │
        │                │                │
        │  • Temas CSS   │  • Refatoração │
        │  • Emojis      │    completa    │
        └────────────────┴────────────────┘
                    BAIXO IMPACTO
```

---

## ⚡ Melhorias de Curto Prazo (Quick Wins)

### 1. Script de Validação Automática de Dados

**Prioridade**: 🔴 ALTA
**Esforço**: 1-2 horas
**Impacto**: Reduz erros em 80%

**Descrição:**
Criar `validar_dados.py` para verificação automática de qualidade dos dados após atualização.

**Implementação:**

```python
# validar_dados.py
import pandas as pd
import sys
from datetime import datetime

def validar_estrutura(df):
    """Valida estrutura básica do DataFrame"""
    erros = []

    # Colunas obrigatórias
    colunas_obrigatorias = [
        'Data_Internacao', 'Data_Saida', 'Municipio_Residencia',
        'Nome_Municipio_Residencia', 'Valor_Total', 'Diagnostico_Principal'
    ]

    faltando = set(colunas_obrigatorias) - set(df.columns)
    if faltando:
        erros.append(f"Colunas faltando: {faltando}")

    return erros

def validar_qualidade(df):
    """Valida qualidade dos dados"""
    alertas = []

    # Verificar nulos críticos
    for col in ['Data_Internacao', 'Municipio_Residencia']:
        pct_nulos = (df[col].isnull().sum() / len(df)) * 100
        if pct_nulos > 5:
            alertas.append(f"{col}: {pct_nulos:.2f}% nulos (limite: 5%)")

    # Verificar valores inválidos
    if (df['Valor_Total'] < 0).any():
        alertas.append("Valores negativos detectados em Valor_Total")

    if (df['Dias_Permanencia'] < 0).any():
        alertas.append("Valores negativos em Dias_Permanencia")

    # Verificar intervalo de datas esperado
    data_min = df['Data_Internacao'].min()
    data_max = df['Data_Internacao'].max()

    if data_min.year != 2025:
        alertas.append(f"Ano mínimo inesperado: {data_min.year}")

    return alertas

def validar_volumes(df):
    """Valida volumes esperados"""
    info = []

    total_registros = len(df)
    info.append(f"Total de registros: {total_registros:,}")

    # Esperado: ~130k registros por mês
    meses_esperados = (df['Data_Internacao'].max().month -
                       df['Data_Internacao'].min().month + 1)
    registros_esperados = meses_esperados * 130000

    variacao = abs(total_registros - registros_esperados) / registros_esperados
    if variacao > 0.2:  # >20% de variação
        info.append(f"⚠️ Volume fora do esperado: {total_registros:,} "
                    f"(esperado: ~{registros_esperados:,})")
    else:
        info.append(f"✅ Volume dentro do esperado")

    return info

def main():
    print("="*60)
    print("VALIDAÇÃO DE DADOS - DASHBOARD SUS")
    print("="*60 + "\n")

    try:
        # Carregar dados
        print("[1/4] Carregando dados...")
        df = pd.read_parquet('dados.parquet')
        print(f"✅ Carregado: {len(df):,} registros\n")

        # Validar estrutura
        print("[2/4] Validando estrutura...")
        erros_estrutura = validar_estrutura(df)
        if erros_estrutura:
            print("❌ ERROS ENCONTRADOS:")
            for erro in erros_estrutura:
                print(f"  • {erro}")
            sys.exit(1)
        else:
            print("✅ Estrutura OK\n")

        # Validar qualidade
        print("[3/4] Validando qualidade...")
        alertas = validar_qualidade(df)
        if alertas:
            print("⚠️ ALERTAS:")
            for alerta in alertas:
                print(f"  • {alerta}")
        else:
            print("✅ Qualidade OK\n")

        # Validar volumes
        print("[4/4] Validando volumes...")
        infos = validar_volumes(df)
        for info in infos:
            print(f"  • {info}")

        print("\n" + "="*60)
        print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERRO NA VALIDAÇÃO: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Benefícios:**
- Detecta problemas automaticamente
- Economiza tempo de verificação manual
- Previne publicação de dados incorretos

---

### 2. Backup Automático Antes de Atualização

**Prioridade**: 🔴 ALTA
**Esforço**: 30 minutos
**Impacto**: Segurança de dados

**Implementação:**

```python
# backup_dados.py
import shutil
from datetime import datetime
import os

def criar_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    arquivos = ['dados.xlsx', 'dados.parquet']
    pasta_backup = f'backups/backup_{timestamp}'

    os.makedirs(pasta_backup, exist_ok=True)

    for arquivo in arquivos:
        if os.path.exists(arquivo):
            destino = os.path.join(pasta_backup, arquivo)
            shutil.copy2(arquivo, destino)
            print(f"✅ Backup criado: {destino}")

    # Manter apenas últimos 5 backups
    limpar_backups_antigos()

def limpar_backups_antigos(manter=5):
    """Remove backups antigos, mantendo apenas os N mais recentes"""
    backups = sorted([d for d in os.listdir('backups')
                      if d.startswith('backup_')],
                     reverse=True)

    for backup_antigo in backups[manter:]:
        caminho = os.path.join('backups', backup_antigo)
        shutil.rmtree(caminho)
        print(f"🗑️ Removido: {caminho}")

if __name__ == "__main__":
    criar_backup()
```

**Adicionar ao pipeline de atualização:**
```batch
REM Adicionar no início do atualizar_dados_completo.bat:
echo Criando backup...
python backup_dados.py
```

---

### 3. Melhorias no README e Documentação

**Prioridade**: 🟡 MÉDIA
**Esforço**: 1-2 horas
**Impacto**: Facilita onboarding

**Ações:**
- Adicionar badges de status (![Status](https://img.shields.io/badge/status-active-success))
- Incluir screenshots do dashboard
- Criar FAQ (Perguntas Frequentes)
- Documentar variáveis de ambiente
- Adicionar troubleshooting expandido

---

### 4. Filtros Persistentes entre Sessões

**Prioridade**: 🟡 MÉDIA
**Esforço**: 2-3 horas
**Impacto**: Melhora UX

**Implementação:**

```python
# Adicionar ao dashboard_sus_v2.py
import json

def salvar_filtros(filtros):
    """Salva filtros em arquivo local"""
    with open('.filtros_usuario.json', 'w') as f:
        json.dump(filtros, f)

def carregar_filtros():
    """Carrega filtros salvos"""
    try:
        with open('.filtros_usuario.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# No código do dashboard, usar:
filtros_salvos = carregar_filtros()

# Aplicar como default nos widgets
municipio_selecionado = st.selectbox(
    "Município",
    options=municipios,
    index=municipios.index(filtros_salvos.get('municipio', municipios[0]))
)

# Ao mudar filtros:
if st.button("Salvar filtros"):
    salvar_filtros({
        'municipio': municipio_selecionado,
        'data_inicio': data_inicio,
        # ... outros filtros
    })
    st.success("Filtros salvos!")
```

---

### 5. Exportação de Relatórios em PDF

**Prioridade**: 🟡 MÉDIA
**Esforço**: 3-4 horas
**Impacto**: Facilita compartilhamento

**Implementação:**

```python
# Adicionar ao dashboard
from fpdf import FPDF
import plotly.io as pio

def gerar_relatorio_pdf(dados_filtrados, graficos):
    """Gera relatório PDF com gráficos e tabelas"""

    pdf = FPDF()
    pdf.add_page()

    # Cabeçalho
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Relatório Dashboard SUS', ln=True, align='C')

    # Período
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Período: {data_inicio} a {data_fim}', ln=True)

    # KPIs
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Indicadores Principais', ln=True)

    # ... adicionar métricas e gráficos

    # Salvar gráficos como imagens temporárias
    for i, grafico in enumerate(graficos):
        img_path = f'temp_grafico_{i}.png'
        pio.write_image(grafico, img_path)
        pdf.image(img_path, x=10, w=190)

    # Salvar PDF
    pdf_output = f'relatorio_sus_{datetime.now().strftime("%Y%m%d")}.pdf'
    pdf.output(pdf_output)

    return pdf_output

# No dashboard:
if st.button("📄 Gerar Relatório PDF"):
    with st.spinner("Gerando relatório..."):
        pdf_file = gerar_relatorio_pdf(dados_filtrados, [fig1, fig2, fig3])
        st.success(f"Relatório gerado: {pdf_file}")

        # Download
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )
```

**Dependências adicionais:**
```bash
pip install fpdf2 kaleido
```

---

## 🤖 Automação do Pipeline de Dados

### 6. Pipeline Totalmente Automatizado

**Prioridade**: 🔴 ALTA
**Esforço**: 1-2 dias
**Impacto**: Elimina 90% do trabalho manual

**Componentes:**

#### 6.1. Agendamento Mensal Automático

```python
# agendador.py - Usar APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
from datetime import datetime

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day=10, hour=3, minute=0)
def atualizar_dados_mensal():
    """Executa pipeline completo todo dia 10 às 3h da manhã"""

    log_file = f"logs/atualizacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    print(f"[{datetime.now()}] Iniciando atualização automática...")

    # Executar pipeline
    resultado = subprocess.run(
        ['python', 'atualizar_pipeline.py'],
        capture_output=True,
        text=True
    )

    # Salvar log
    with open(log_file, 'w') as f:
        f.write(resultado.stdout)
        f.write(resultado.stderr)

    # Enviar notificação
    if resultado.returncode == 0:
        enviar_notificacao("✅ Atualização concluída com sucesso!")
    else:
        enviar_notificacao(f"❌ Erro na atualização. Ver log: {log_file}")

if __name__ == "__main__":
    print("Agendador iniciado. Aguardando próxima execução...")
    scheduler.start()
```

**Executar como serviço:**
```bash
# Linux: systemd service
# Windows: NSSM (Non-Sucking Service Manager)
nssm install DashboardSUS_Agendador python agendador.py
```

#### 6.2. Notificações Inteligentes

```python
# notificacoes.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(assunto, corpo, destinatarios):
    """Envia email via SMTP"""

    msg = MIMEMultipart()
    msg['From'] = 'dashboard.sus@exemplo.com'
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'html'))

    # Configurar SMTP (exemplo com Gmail)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('seu_email@gmail.com', 'sua_senha_app')
        server.send_message(msg)

def enviar_notificacao_telegram(mensagem):
    """Envia mensagem via Telegram Bot"""
    import requests

    TOKEN = 'seu_token_bot'
    CHAT_ID = 'seu_chat_id'

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': mensagem}

    requests.post(url, data=data)

# Template de email
def template_sucesso(estatisticas):
    return f"""
    <html>
    <body>
        <h2>✅ Atualização do Dashboard SUS Concluída</h2>
        <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>

        <h3>Estatísticas:</h3>
        <ul>
            <li>Total de registros: {estatisticas['total_registros']:,}</li>
            <li>Período: {estatisticas['periodo']}</li>
            <li>Novos registros: {estatisticas['novos_registros']:,}</li>
        </ul>

        <p><a href="http://localhost:8501">Acessar Dashboard</a></p>
    </body>
    </html>
    """
```

---

### 7. Migração para Python Puro (Eliminar Dependência de R)

**Prioridade**: 🟡 MÉDIA
**Esforço**: 2-3 dias
**Impacto**: Simplifica stack tecnológico

**Alternativa: PySUS**

```python
# extracao_pysus.py
from pysus.online_data import SIH
import pandas as pd

def extrair_dados_datasus(uf, ano, mes_inicio, mes_final):
    """Extrai dados SIH usando PySUS (Python nativo)"""

    sih = SIH().load()

    dados_completo = []

    for mes in range(mes_inicio, mes_final + 1):
        print(f"Baixando dados de {mes:02d}/{ano}...")

        # Download
        df = sih.get_files(state=uf, year=ano, month=mes)

        dados_completo.append(df)

    # Concatenar todos os meses
    resultado = pd.concat(dados_completo, ignore_index=True)

    return resultado

# Enriquecimento de dados
def enriquecer_dados(df):
    """Adiciona nomes de municípios, procedimentos, etc."""

    from pysus.utilities.readdbc import read_dbc

    # Baixar tabelas auxiliares
    tab_municipios = pd.read_csv('https://...')  # Fonte de municípios
    tab_sigtap = pd.read_csv('https://...')       # Tabela SIGTAP

    # Joins
    df = df.merge(tab_municipios, left_on='MUNIC_RES', right_on='codigo')
    df = df.merge(tab_sigtap, left_on='PROC_REA', right_on='codigo_proc')

    return df

# Uso
if __name__ == "__main__":
    dados = extrair_dados_datasus(uf='MG', ano=2025, mes_inicio=1, mes_final=7)
    dados_enriquecidos = enriquecer_dados(dados)
    dados_enriquecidos.to_parquet('dados.parquet')
```

**Vantagens:**
- ✅ Elimina necessidade de R
- ✅ Stack 100% Python
- ✅ Mais fácil de deployar
- ✅ Integração mais simples

**Desvantagens:**
- ⚠️ Requer reescrita do pipeline de extração
- ⚠️ PySUS pode ter menos funcionalidades que microdatasus

---

## 🧠 Expansões Analíticas Avançadas

### 8. Previsão de Demanda com Machine Learning

**Prioridade**: 🟡 MÉDIA
**Esforço**: 1 semana
**Impacto**: Alto valor analítico

**Implementação:**

```python
# previsao.py
from prophet import Prophet
import pandas as pd

def prever_internacoes(dados_historicos, periodos_futuros=6):
    """Prevê internações futuras usando Facebook Prophet"""

    # Preparar dados
    df_prophet = dados_historicos.groupby('Data_Internacao').size().reset_index()
    df_prophet.columns = ['ds', 'y']

    # Treinar modelo
    modelo = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )

    modelo.fit(df_prophet)

    # Fazer previsão
    futuro = modelo.make_future_dataframe(periods=periodos_futuros, freq='M')
    previsao = modelo.predict(futuro)

    return previsao

# Adicionar ao dashboard
def painel_previsoes():
    st.header("🔮 Previsões de Demanda")

    # Calcular previsão
    previsao = prever_internacoes(dados, periodos_futuros=6)

    # Visualizar
    fig = go.Figure()

    # Dados históricos
    fig.add_trace(go.Scatter(
        x=dados.groupby('Data_Internacao').size().index,
        y=dados.groupby('Data_Internacao').size().values,
        name='Histórico',
        mode='lines+markers'
    ))

    # Previsão
    fig.add_trace(go.Scatter(
        x=previsao['ds'],
        y=previsao['yhat'],
        name='Previsão',
        line=dict(dash='dash')
    ))

    # Intervalo de confiança
    fig.add_trace(go.Scatter(
        x=previsao['ds'],
        y=previsao['yhat_upper'],
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=previsao['ds'],
        y=previsao['yhat_lower'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        name='Intervalo de confiança'
    ))

    st.plotly_chart(fig)

    # Tabela de previsões
    st.subheader("Previsões Mensais")
    st.dataframe(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(6))
```

**Dependências:**
```bash
pip install prophet
```

---

### 9. Detecção de Anomalias

**Prioridade**: 🟡 MÉDIA
**Esforço**: 3-4 dias
**Impacto**: Identifica surtos e irregularidades

**Implementação:**

```python
# anomalias.py
from sklearn.ensemble import IsolationForest
import numpy as np

def detectar_anomalias_temporais(dados):
    """Detecta padrões anormais em séries temporais"""

    # Agregar por dia
    serie_diaria = dados.groupby('Data_Internacao').agg({
        'Numero_AIH': 'count',
        'Valor_Total': 'sum',
        'Dias_Permanencia': 'mean',
        'Morte': lambda x: (x == 'Sim').sum()
    }).reset_index()

    # Features para detecção
    features = serie_diaria[['Numero_AIH', 'Valor_Total',
                              'Dias_Permanencia', 'Morte']].values

    # Modelo Isolation Forest
    modelo = IsolationForest(contamination=0.05, random_state=42)
    serie_diaria['anomalia'] = modelo.fit_predict(features)

    # Retornar dias anômalos
    anomalias = serie_diaria[serie_diaria['anomalia'] == -1]

    return anomalias

# No dashboard
def painel_anomalias():
    st.header("⚠️ Detecção de Anomalias")

    anomalias = detectar_anomalias_temporais(dados)

    st.warning(f"🔍 Detectadas {len(anomalias)} anomalias no período")

    # Visualizar
    fig = go.Figure()

    # Dados normais
    normais = dados.groupby('Data_Internacao').size()
    fig.add_trace(go.Scatter(
        x=normais.index,
        y=normais.values,
        mode='lines',
        name='Internações'
    ))

    # Marcar anomalias
    fig.add_trace(go.Scatter(
        x=anomalias['Data_Internacao'],
        y=anomalias['Numero_AIH'],
        mode='markers',
        marker=dict(size=15, color='red', symbol='x'),
        name='Anomalias'
    ))

    st.plotly_chart(fig)

    # Tabela de anomalias
    st.subheader("Detalhes das Anomalias")
    st.dataframe(anomalias)
```

---

### 10. Análise de Clusters de Pacientes

**Prioridade**: 🟢 BAIXA
**Esforço**: 1 semana
**Impacto**: Insights sobre perfis de pacientes

**Implementação:**

```python
# clustering.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def clusterizar_pacientes(dados):
    """Agrupa pacientes em clusters por características"""

    # Selecionar features
    features = dados[['Idade', 'Dias_Permanencia', 'Valor_Total']].copy()

    # Codificar variáveis categóricas
    features['Sexo_num'] = dados['Sexo'].map({'Masculino': 1, 'Feminino': 0})
    features['Morte_num'] = dados['Morte'].map({'Sim': 1, 'Não': 0})

    # Normalizar
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features.dropna())

    # K-Means
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)

    dados['cluster'] = clusters

    return dados

# Visualização 3D
def visualizar_clusters_3d(dados_clusterizados):
    fig = px.scatter_3d(
        dados_clusterizados.sample(10000),  # Amostra para performance
        x='Idade',
        y='Dias_Permanencia',
        z='Valor_Total',
        color='cluster',
        title='Clusters de Pacientes (3D)',
        labels={'cluster': 'Grupo'}
    )

    st.plotly_chart(fig)
```

---

## 🎨 Melhorias de UX/UI

### 11. Design System Completo

**Prioridade**: 🟢 BAIXA
**Esforço**: 1 semana
**Impacto**: Profissionalização visual

**Componentes:**

```python
# design_system.py - Componentes reutilizáveis

class DashboardTheme:
    """Tema unificado do dashboard"""

    CORES = {
        'primaria': '#0066CC',
        'secundaria': '#00CC66',
        'alerta': '#FF6B00',
        'perigo': '#CC0000',
        'fundo': '#F8F9FA',
        'texto': '#212529'
    }

    GRADIENTES = {
        'azul': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'verde': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'laranja': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    }

def card_kpi(titulo, valor, delta=None, icone=None):
    """Card de KPI padronizado"""

    cor = 'verde' if delta and delta > 0 else 'vermelho'

    html = f"""
    <div style="
        background: {DashboardTheme.GRADIENTES['azul']};
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white;
    ">
        <div style="font-size: 14px; opacity: 0.9;">{icone} {titulo}</div>
        <div style="font-size: 32px; font-weight: bold; margin: 10px 0;">
            {valor}
        </div>
        {f'<div style="font-size: 14px;">↑ {delta} vs mês anterior</div>' if delta else ''}
    </div>
    """

    return html

# Uso no dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(card_kpi(
        "Total de Internações",
        "916.208",
        delta="+12%",
        icone="🏥"
    ), unsafe_allow_html=True)
```

---

### 12. Modo Escuro (Dark Mode)

**Prioridade**: 🟢 BAIXA
**Esforço**: 1-2 dias
**Impacto**: Conforto visual

```python
# Adicionar toggle no sidebar
tema_escuro = st.sidebar.checkbox("🌙 Modo Escuro")

if tema_escuro:
    st.markdown("""
    <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }

        .stSidebar {
            background-color: #252526;
        }

        /* ... mais estilos ... */
    </style>
    """, unsafe_allow_html=True)
```

---

### 13. Dashboard Responsivo (Mobile)

**Prioridade**: 🟡 MÉDIA
**Esforço**: 3-4 dias
**Impacto**: Acesso mobile

```python
# Detectar dispositivo
import streamlit.components.v1 as components

components.html("""
<script>
    const isMobile = window.innerWidth < 768;
    if (isMobile) {
        window.parent.postMessage({type: 'mobile', value: true}, '*');
    }
</script>
""", height=0)

# Ajustar layout
if 'mobile' in st.session_state and st.session_state.mobile:
    # Layout single-column
    st.write("Layout mobile")
else:
    # Layout multi-column
    col1, col2, col3 = st.columns(3)
```

---

## 🔌 Integrações e APIs

### 14. API REST para Acesso Externo

**Prioridade**: 🟡 MÉDIA
**Esforço**: 1 semana
**Impacto**: Permite integrações

**Implementação com FastAPI:**

```python
# api.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional
from datetime import date

app = FastAPI(title="Dashboard SUS API")

# Cache de dados
@st.cache_data
def carregar_dados_api():
    return pd.read_parquet('dados.parquet')

@app.get("/")
def root():
    return {"message": "Dashboard SUS API v1.0"}

@app.get("/internacoes")
def get_internacoes(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    municipio: Optional[str] = None,
    limit: int = Query(default=1000, le=10000)
):
    """Retorna internações filtradas"""

    df = carregar_dados_api()

    # Aplicar filtros
    if data_inicio:
        df = df[df['Data_Internacao'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        df = df[df['Data_Internacao'] <= pd.to_datetime(data_fim)]
    if municipio:
        df = df[df['Nome_Municipio_Residencia'] == municipio]

    # Limitar
    df = df.head(limit)

    # Retornar JSON
    return JSONResponse(content=df.to_dict(orient='records'))

@app.get("/kpis")
def get_kpis():
    """Retorna KPIs principais"""

    df = carregar_dados_api()

    kpis = {
        'total_internacoes': int(df.shape[0]),
        'valor_total': float(df['Valor_Total'].sum()),
        'media_permanencia': float(df['Dias_Permanencia'].mean()),
        'taxa_mortalidade': float((df['Morte'] == 'Sim').sum() / len(df) * 100)
    }

    return kpis

@app.get("/municipios")
def get_municipios():
    """Lista municípios disponíveis"""

    df = carregar_dados_api()
    municipios = df['Nome_Municipio_Residencia'].unique().tolist()

    return {"municipios": municipios}

# Executar: uvicorn api:app --reload
```

**Uso da API:**
```bash
# Obter KPIs
curl http://localhost:8000/kpis

# Obter internações filtradas
curl "http://localhost:8000/internacoes?municipio=Belo%20Horizonte&limit=10"
```

---

### 15. Integração com Power BI / Tableau

**Prioridade**: 🟢 BAIXA
**Esforço**: 2-3 dias
**Impacto**: Ampliar alcance

**Opções:**

1. **Exportar OData Feed** (via API)
2. **Conector direto** para Parquet
3. **Banco de dados intermediário** (PostgreSQL)

```python
# Exemplo: Endpoint OData
@app.get("/odata/internacoes")
def odata_feed():
    df = carregar_dados_api()

    # Converter para formato OData
    # ... implementação OData v4 ...

    return odata_response
```

---

## ☁️ Infraestrutura e Escalabilidade

### 16. Deploy em Cloud (Streamlit Cloud)

**Prioridade**: 🟡 MÉDIA
**Esforço**: 1-2 dias
**Impacto**: Acesso público

**Passos:**

1. Criar conta em [Streamlit Community Cloud](https://streamlit.io/cloud)
2. Conectar repositório GitHub
3. Configurar `requirements.txt`
4. Adicionar secrets para dados sensíveis

**Arquivos necessários:**

```toml
# .streamlit/config.toml
[server]
maxUploadSize = 500
enableXsrfProtection = true

[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

```python
# .streamlit/secrets.toml
# Não commitar este arquivo!
[data]
parquet_url = "https://storage.example.com/dados.parquet"

[email]
smtp_server = "smtp.gmail.com"
smtp_user = "seu_email@gmail.com"
smtp_password = "senha_app"
```

---

### 17. Banco de Dados para Dados Históricos

**Prioridade**: 🟡 MÉDIA
**Esforço**: 1 semana
**Impacto**: Escalabilidade

**Migrar de arquivos para PostgreSQL/DuckDB:**

```python
# db_setup.py
import duckdb

def criar_banco():
    """Cria banco DuckDB otimizado"""

    con = duckdb.connect('dashboard_sus.db')

    # Criar tabela
    con.execute("""
        CREATE TABLE IF NOT EXISTS internacoes (
            id INTEGER PRIMARY KEY,
            data_internacao DATE,
            data_saida DATE,
            municipio_residencia VARCHAR,
            nome_municipio_residencia VARCHAR,
            valor_total DECIMAL(10,2),
            dias_permanencia INTEGER,
            diagnostico_principal VARCHAR,
            nome_doenca VARCHAR,
            sexo VARCHAR,
            idade INTEGER,
            morte BOOLEAN
        )
    """)

    # Importar parquet
    con.execute("""
        INSERT INTO internacoes
        SELECT * FROM read_parquet('dados.parquet')
    """)

    # Criar índices
    con.execute("CREATE INDEX idx_data ON internacoes(data_internacao)")
    con.execute("CREATE INDEX idx_municipio ON internacoes(municipio_residencia)")

    con.close()

# No dashboard, substituir:
# df = pd.read_parquet('dados.parquet')
# Por:
con = duckdb.connect('dashboard_sus.db')
df = con.execute("SELECT * FROM internacoes WHERE data_internacao >= '2025-01-01'").df()
```

**Vantagens:**
- ✅ Queries SQL otimizadas
- ✅ Suporta dados históricos de múltiplos anos
- ✅ Menor uso de memória RAM
- ✅ Consultas mais rápidas

---

### 18. CI/CD Pipeline

**Prioridade**: 🟢 BAIXA
**Esforço**: 2-3 dias
**Impacto**: Automação de deploy

**GitHub Actions:**

```yaml
# .github/workflows/deploy.yml
name: Deploy Dashboard

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        run: pytest tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Streamlit Cloud
        run: |
          # Trigger deploy webhook
          curl -X POST ${{ secrets.STREAMLIT_DEPLOY_HOOK }}
```

---

## 🔄 Alternativas Tecnológicas

### 19. Migração para Dash/Plotly (Alternativa ao Streamlit)

**Prioridade**: 🟢 BAIXA
**Esforço**: 2-3 semanas
**Impacto**: Maior controle e customização

**Prós:**
- ✅ Mais controle sobre layout
- ✅ Melhor performance com grandes datasets
- ✅ Callbacks mais poderosos

**Contras:**
- ❌ Curva de aprendizado maior
- ❌ Mais código boilerplate

---

### 20. Modernização com Shiny for Python

**Prioridade**: 🟢 BAIXA
**Esforço**: 2-3 semanas
**Impacto**: Framework emergente

Shiny for Python é uma alternativa moderna ao Streamlit, com recursos reativos avançados.

---

## 📅 Roadmap Sugerido

### Fase 1: Estabilização (1-2 semanas)
- ✅ Script de validação automática (#1)
- ✅ Backup automático (#2)
- ✅ Melhorias na documentação (#3)

### Fase 2: Automação (1 mês)
- 🔄 Pipeline totalmente automatizado (#6)
- 🔄 Notificações inteligentes (#6.2)
- 🔄 Migração para Python puro (#7) - OPCIONAL

### Fase 3: Analytics Avançado (2 meses)
- 🔮 Previsão de demanda (#8)
- ⚠️ Detecção de anomalias (#9)
- 📊 Análise de clusters (#10) - OPCIONAL

### Fase 4: Expansão (3 meses)
- 🔌 API REST (#14)
- ☁️ Deploy em cloud (#16)
- 💾 Banco de dados (#17)

### Fase 5: Refinamento (ongoing)
- 🎨 Melhorias de UX/UI (#11, #12, #13)
- 🔗 Integrações (#15)
- 🚀 CI/CD (#18)

---

## 💰 Estimativa de Esforço Total

| Categoria | Horas | Custo (R$ 100/h) |
|-----------|-------|------------------|
| Quick Wins | 10h | R$ 1.000 |
| Automação | 60h | R$ 6.000 |
| Analytics | 120h | R$ 12.000 |
| Infraestrutura | 80h | R$ 8.000 |
| UX/UI | 60h | R$ 6.000 |
| **TOTAL** | **330h** | **R$ 33.000** |

---

## 📞 Próximos Passos

1. **Revisar este documento** e priorizar melhorias
2. **Definir orçamento** e cronograma
3. **Começar com Quick Wins** para ganhos rápidos
4. **Planejar Fase 2** (Automação) como próxima etapa estratégica
5. **Considerar contratar** desenvolvedor/analista para features avançadas

---

**Última atualização**: Novembro 2025
**Autor**: Pedro William
**Contato**: pedrowilliamrd@gmail.com
