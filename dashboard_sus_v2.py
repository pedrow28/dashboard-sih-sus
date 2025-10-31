"""
Dashboard de Análise de Internações Hospitalares - SIH/DATASUS
Desenvolvido em Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Dashboard SIH/DATASUS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Design moderno e profissional
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Configurações gerais */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        padding: 0rem 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Estilo dos cards/métricas */
    .stMetric {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        padding: 20px;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1),
                    0 3px 6px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15),
                    0 5px 10px rgba(0, 0, 0, 0.1);
    }

    /* Títulos principais */
    h1 {
        color: #1e3a8a;
        font-weight: 700;
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Subtítulos */
    h2 {
        color: #1e40af;
        font-weight: 600;
        font-size: 1.8rem !important;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }

    h3 {
        color: #2563eb;
        font-weight: 600;
        font-size: 1.3rem !important;
    }

    /* Tabs - Navegação principal */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f1f5f9;
        border-radius: 10px;
        color: #475569;
        font-weight: 500;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e7ff;
        color: #3730a3;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
    }

    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 700 !important;
    }

    .css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
        color: #e0e7ff;
    }

    /* Labels dos filtros na sidebar em branco negritado */
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 700 !important;
    }

    /* Dataframes */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.6);
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }

    /* Inputs e selects */
    .stSelectbox, .stMultiSelect, .stDateInput {
        border-radius: 10px;
    }

    /* Divisores */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
    }

    /* Métricas - valores */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Cards de aviso */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }

    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÃO PARA CARREGAR DADOS
# ============================================================================

@st.cache_data
def carregar_dados():
    """
    Carrega os dados do SIH/DATASUS

    ⚠️ ALTERE O CAMINHO DO ARQUIVO AQUI ⚠️
    """

    # ====================================================================
    # 🔴 ALTERE O CAMINHO DO SEU ARQUIVO AQUI 🔴
    # ====================================================================
    CAMINHO_ARQUIVO = "dados.parquet"  # ← ALTERE AQUI
    # Exemplos:
    # CAMINHO_ARQUIVO = "amostra.xlsx"  # Para testar com amostra
    # CAMINHO_ARQUIVO = "dados.xlsx"  # Base completa em Excel (mais lento)
    # CAMINHO_ARQUIVO = "dados.parquet"  # Base completa em Parquet (RECOMENDADO - 10x mais rápido!)
    # CAMINHO_ARQUIVO = "C:/Users/SeuUsuario/Documents/dados.parquet"  # Windows com caminho absoluto
    # ====================================================================

    try:
        # Detecta o tipo de arquivo pela extensão
        if CAMINHO_ARQUIVO.endswith('.csv'):
            df = pd.read_csv(CAMINHO_ARQUIVO, encoding='utf-8', low_memory=False)
        elif CAMINHO_ARQUIVO.endswith('.parquet'):
            df = pd.read_parquet(CAMINHO_ARQUIVO)
        elif CAMINHO_ARQUIVO.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(CAMINHO_ARQUIVO)
        else:
            st.error("Formato de arquivo não suportado. Use CSV, Parquet ou Excel.")
            return None

        # ====================================================================
        # RENOMEAR COLUNAS PARA ESTRUTURA ESPERADA
        # ====================================================================

        # Mapeamento das colunas reais para a estrutura esperada
        colunas_renomear = {
            'UF_Residencia': 'UF_ZI',
            'Municipio_Residencia': 'MUNIC_RES',
            'Nome_Municipio_Residencia': 'NOME_MUNIC_RES',
            'Municipio_Atendimento': 'MUNIC_MOV',
            'Nome_Municipio_Atendimento': 'NOME_MUNIC_MOV',
            'Codigo_CNES': 'CNES',
            'Nome_Estabelecimento': 'NOME_FANTASIA',
            'Dias_Permanencia': 'DIAS_PERM',
            'Dias_UTI_Mes': 'DIAS_UTI',
            'Diagnostico_Principal': 'DIAG_PRINC',
            'Nome_Doenca': 'NOME_CID_PRINC',
            'Procedimento_Solicitado': 'PROC_SOLI',
            'Nome_Procedimento_Solicitado': 'NOME_PROC_SOLI',
            'Procedimento_Realizado': 'PROC_REA',
            'Nome_Procedimento_Realizado': 'NOME_PROC_REA',
            'Valor_Total': 'VAL_TOT',
            'Data_Internacao': 'DT_INTER',
            'Data_Saida': 'DT_SAIDA',
            'Data_Nascimento': 'DT_NASC',
            'Sexo': 'SEXO',
            'Idade': 'IDADE',
            'Raca_Cor': 'RACA_COR_COD',
            'Nome_Raca_Cor': 'RACA_COR',
            'Morte': 'MORTE_TXT',
            'CID_Notificacao': 'CID_MORTE'
        }

        # Renomear apenas as colunas que existem
        colunas_existentes = {k: v for k, v in colunas_renomear.items() if k in df.columns}
        df = df.rename(columns=colunas_existentes)

        # ====================================================================
        # PROCESSAMENTO E LIMPEZA DOS DADOS
        # ====================================================================

        # Converte colunas de data
        if 'DT_INTER' in df.columns:
            df['DT_INTER'] = pd.to_datetime(df['DT_INTER'], errors='coerce')

            # Criar colunas de competência a partir da data de internação
            df['ANO_CMPT'] = df['DT_INTER'].dt.year
            df['MES_CMPT'] = df['DT_INTER'].dt.month
            df['DATA_CMPT'] = df['DT_INTER']
        elif 'ANO_CMPT' in df.columns and 'MES_CMPT' in df.columns:
            # Se já existir ANO_CMPT e MES_CMPT (estrutura alternativa)
            df['DATA_CMPT'] = pd.to_datetime(
                df['ANO_CMPT'].astype(str) + '-' + df['MES_CMPT'].astype(str).str.zfill(2) + '-01',
                errors='coerce'
            )

        # Converter outras datas
        if 'DT_SAIDA' in df.columns:
            df['DT_SAIDA'] = pd.to_datetime(df['DT_SAIDA'], errors='coerce')
        if 'DT_NASC' in df.columns:
            df['DT_NASC'] = pd.to_datetime(df['DT_NASC'], errors='coerce')

        # Converte valores numéricos
        colunas_numericas = ['DIAS_PERM', 'DIAS_UTI', 'VAL_TOT', 'IDADE']
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Trata coluna MORTE (converter de texto "Sim"/"Não" para 0/1)
        if 'MORTE_TXT' in df.columns:
            df['MORTE'] = df['MORTE_TXT'].map({'Não': 0, 'Sim': 1}).fillna(0).astype(int)
        elif 'MORTE' in df.columns:
            # Se já existir MORTE como numérico
            df['MORTE'] = pd.to_numeric(df['MORTE'], errors='coerce').fillna(0).astype(int)

        # Trata sexo (já vem como texto "Masculino"/"Feminino")
        if 'SEXO' in df.columns:
            # Converter para string primeiro para evitar problemas com categorical
            if df['SEXO'].dtype.name == 'category':
                df['SEXO'] = df['SEXO'].astype(str)

            # Se vier como código numérico
            if df['SEXO'].dtype in ['int64', 'float64']:
                df['SEXO'] = df['SEXO'].map({1: 'Masculino', 3: 'Feminino', 0: 'Ignorado'}).fillna('Ignorado')
            else:
                # Se já vier como texto, apenas garantir valores
                df['SEXO'] = df['SEXO'].fillna('Ignorado')

        # Trata raça/cor
        if 'RACA_COR' in df.columns:
            # Converter para string primeiro para evitar problemas com categorical
            if df['RACA_COR'].dtype.name == 'category':
                df['RACA_COR'] = df['RACA_COR'].astype(str)

            # Se vier como código numérico, mapear
            if df['RACA_COR'].dtype in ['int64', 'float64']:
                df['RACA_COR'] = df['RACA_COR'].map({
                    1: 'Branca',
                    2: 'Preta',
                    3: 'Parda',
                    4: 'Amarela',
                    5: 'Indígena',
                    9: 'Ignorada'
                }).fillna('Ignorada')
            else:
                # Se já vier como texto, apenas garantir que não há nulos
                df['RACA_COR'] = df['RACA_COR'].fillna('Ignorada')
        elif 'RACA_COR_COD' in df.columns and 'RACA_COR' not in df.columns:
            # Se só tiver o código, criar a coluna de texto
            df['RACA_COR'] = df['RACA_COR_COD'].map({
                1: 'Branca',
                2: 'Preta',
                3: 'Parda',
                4: 'Amarela',
                5: 'Indígena',
                9: 'Ignorada'
            }).fillna('Ignorada')

        # Criar coluna CID_PRINC (alias para DIAG_PRINC)
        if 'DIAG_PRINC' in df.columns:
            df['DIAG_PRINC'] = df['DIAG_PRINC'].astype(str)
            df['CID_PRINC'] = df['DIAG_PRINC']

        # Criar coluna CID_SECUN vazia (não existe na base real)
        df['CID_SECUN'] = None

        # Cria faixas etárias
        if 'IDADE' in df.columns:
            df['FAIXA_ETARIA'] = pd.cut(
                df['IDADE'],
                bins=[0, 1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 120],
                labels=['<1', '1-4', '5-9', '10-14', '15-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
            )

        # Remove valores inválidos
        if 'DATA_CMPT' in df.columns:
            df = df.dropna(subset=['DATA_CMPT'])

            # ====================================================================
            # FILTRAR APENAS INTERNAÇÕES DE JANEIRO A JULHO DE 2025
            # ====================================================================
            data_inicio = pd.to_datetime('2025-01-01')
            data_fim = pd.to_datetime('2025-07-31')

            total_antes = len(df)
            df = df[(df['DATA_CMPT'] >= data_inicio) & (df['DATA_CMPT'] <= data_fim)]
            total_depois = len(df)

        # Remove linhas com valores críticos ausentes
        colunas_criticas = ['MUNIC_RES', 'MUNIC_MOV']
        for col in colunas_criticas:
            if col in df.columns:
                df = df.dropna(subset=[col])

        return df

    except FileNotFoundError:
        st.error(f"❌ Arquivo não encontrado: {CAMINHO_ARQUIVO}")
        st.info("Por favor, verifique o caminho do arquivo no código (função carregar_dados)")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.info(f"💡 Detalhes do erro para debug: {type(e).__name__}")
        return None

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def formatar_numero(valor):
    """Formata número com separador de milhares"""
    return f"{valor:,.0f}".replace(",", ".")

def formatar_moeda(valor):
    """Formata valor monetário em R$"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_percentual(valor):
    """Formata percentual com 1 casa decimal"""
    return f"{valor:.1f}%"

def calcular_delta_percentual(atual, anterior):
    """Calcula variação percentual"""
    if anterior == 0:
        return 0
    return ((atual - anterior) / anterior) * 100

# ============================================================================
# FILTROS GLOBAIS NA SIDEBAR
# ============================================================================

def criar_filtros_sidebar(df):
    """Cria todos os filtros globais na sidebar"""

    st.sidebar.markdown("<h1 style='color: white !important;'>🏥 Dashboard SIH/DATASUS</h1>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.sidebar.header("🔍 Filtros")
    
    filtros = {}
    
    # Filtro de Período
    if 'DATA_CMPT' in df.columns:
        st.sidebar.subheader("📅 Período")
        data_min = df['DATA_CMPT'].min().date()
        data_max = df['DATA_CMPT'].max().date()

        col1, col2 = st.sidebar.columns(2)
        with col1:
            filtros['data_inicio'] = st.date_input(
                "Data Inicial",
                value=data_min,  # Usar data_min em vez de calcular 365 dias atrás
                min_value=data_min,
                max_value=data_max,
                help="Dados filtrados para janeiro-julho/2025"
            )
        with col2:
            filtros['data_fim'] = st.date_input(
                "Data Final",
                value=data_max,
                min_value=data_min,
                max_value=data_max,
                help="Dados filtrados para janeiro-julho/2025"
            )
    
    # Filtros de Município (separados por residência e atendimento)
    st.sidebar.subheader("📍 Municípios")

    if 'NOME_MUNIC_RES' in df.columns:
        municipios_res = sorted(df['NOME_MUNIC_RES'].dropna().unique())
        filtros['municipio_residencia'] = st.sidebar.multiselect(
            "Município de Residência",
            options=municipios_res,
            default=None,
            help="Município onde o paciente reside"
        )

    if 'NOME_MUNIC_MOV' in df.columns:
        municipios_atend = sorted(df['NOME_MUNIC_MOV'].dropna().unique())
        filtros['municipio_atendimento'] = st.sidebar.multiselect(
            "Município de Atendimento",
            options=municipios_atend,
            default=None,
            help="Município onde a internação foi realizada"
        )
    
    # Filtro de Estabelecimento
    if 'CNES' in df.columns:
        st.sidebar.subheader("🏥 Estabelecimento")
        if 'NOME_FANTASIA' in df.columns:
            cnes_options = df[['CNES', 'NOME_FANTASIA']].drop_duplicates().copy()
            # Converter para string para evitar problemas com categorical
            cnes_options['NOME_FANTASIA'] = cnes_options['NOME_FANTASIA'].astype(str)
            cnes_options['display'] = cnes_options['CNES'].astype(str) + ' - ' + cnes_options['NOME_FANTASIA'].fillna('')
            filtros['cnes'] = st.sidebar.multiselect(
                "Estabelecimento(s)",
                options=cnes_options['CNES'].tolist(),
                format_func=lambda x: cnes_options[cnes_options['CNES'] == x]['display'].iloc[0] if len(cnes_options[cnes_options['CNES'] == x]) > 0 else str(x)
            )
        else:
            filtros['cnes'] = st.sidebar.multiselect(
                "CNES",
                options=sorted(df['CNES'].dropna().unique())
            )
    
    # Filtros Demográficos
    st.sidebar.subheader("👥 Demográficos")
    
    if 'SEXO' in df.columns:
        filtros['sexo'] = st.sidebar.multiselect(
            "Sexo",
            options=['Masculino', 'Feminino', 'Ignorado'],
            default=None
        )
    
    if 'FAIXA_ETARIA' in df.columns:
        filtros['faixa_etaria'] = st.sidebar.multiselect(
            "Faixa Etária",
            options=['<1', '1-4', '5-9', '10-14', '15-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80+'],
            default=None
        )
    
    if 'RACA_COR' in df.columns:
        filtros['raca_cor'] = st.sidebar.multiselect(
            "Raça/Cor",
            options=['Branca', 'Preta', 'Parda', 'Amarela', 'Indígena', 'Ignorada'],
            default=None
        )
    
    # Filtro de CID
    if 'DIAG_PRINC' in df.columns or 'CID_PRINC' in df.columns:
        st.sidebar.subheader("🔬 Diagnóstico")
        col_cid = 'DIAG_PRINC' if 'DIAG_PRINC' in df.columns else 'CID_PRINC'
        cids = sorted(df[col_cid].dropna().unique())
        filtros['cid'] = st.sidebar.multiselect(
            "CID Principal",
            options=cids
        )
    
    # Botões de ação
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("🔄 Limpar Filtros", use_container_width=True):
            st.rerun()
    
    # Informações dos dados
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Informações")
    st.sidebar.info(f"""
    **Total de registros:** {formatar_numero(len(df))}  
    **Período:** {df['DATA_CMPT'].min().strftime('%m/%Y') if 'DATA_CMPT' in df.columns else 'N/A'} - {df['DATA_CMPT'].max().strftime('%m/%Y') if 'DATA_CMPT' in df.columns else 'N/A'}  
    **Fonte:** SIH/DATASUS
    """)
    
    return filtros

def aplicar_filtros(df, filtros):
    """Aplica os filtros selecionados ao dataframe"""
    
    df_filtrado = df.copy()
    
    # Filtro de período
    if 'data_inicio' in filtros and 'data_fim' in filtros and 'DATA_CMPT' in df.columns:
        df_filtrado = df_filtrado[
            (df_filtrado['DATA_CMPT'].dt.date >= filtros['data_inicio']) &
            (df_filtrado['DATA_CMPT'].dt.date <= filtros['data_fim'])
        ]
    
    # Filtro de município de residência
    if filtros.get('municipio_residencia') and 'NOME_MUNIC_RES' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['NOME_MUNIC_RES'].isin(filtros['municipio_residencia'])]

    # Filtro de município de atendimento
    if filtros.get('municipio_atendimento') and 'NOME_MUNIC_MOV' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['NOME_MUNIC_MOV'].isin(filtros['municipio_atendimento'])]
    
    # Filtro de CNES
    if filtros.get('cnes') and 'CNES' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['CNES'].isin(filtros['cnes'])]
    
    # Filtro de sexo
    if filtros.get('sexo') and 'SEXO' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['SEXO'].isin(filtros['sexo'])]
    
    # Filtro de faixa etária
    if filtros.get('faixa_etaria') and 'FAIXA_ETARIA' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['FAIXA_ETARIA'].isin(filtros['faixa_etaria'])]
    
    # Filtro de raça/cor
    if filtros.get('raca_cor') and 'RACA_COR' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['RACA_COR'].isin(filtros['raca_cor'])]
    
    # Filtro de CID
    if filtros.get('cid'):
        col_cid = 'DIAG_PRINC' if 'DIAG_PRINC' in df.columns else 'CID_PRINC'
        if col_cid in df.columns:
            df_filtrado = df_filtrado[df_filtrado[col_cid].isin(filtros['cid'])]
    
    return df_filtrado

# ============================================================================
# PAINEL 0: INICIAL (BEM-VINDO E INSTRUÇÕES)
# ============================================================================

def painel_inicial():
    """Painel inicial com instruções de uso do dashboard"""

    st.title("🏥 Bem-vindo ao Dashboard SIH/DATASUS - Internações MG 2025")

    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;'>
        <h2 style='color: white; margin-top: 0;'>📊 Sobre este Dashboard</h2>
        <p style='font-size: 1.1rem; line-height: 1.6;'>
        Este dashboard apresenta uma análise completa e interativa das <strong>internações hospitalares</strong>
        realizadas em <strong>Minas Gerais</strong> no período de <strong>janeiro a julho de 2025</strong>,
        com dados do Sistema de Informações Hospitalares do SUS (SIH/DATASUS).
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 **Objetivo**

        Fornecer insights estratégicos para:
        - 📈 **Gestores de saúde pública**
        - 🏥 **Administradores hospitalares**
        - 🔬 **Pesquisadores e epidemiologistas**
        - 👨‍⚕️ **Profissionais de saúde**
                    

        ---

        ### 📑 **Abas Disponíveis**

        **📊 Geral** - Visão geral de indicadores-chave, evolução temporal e custos

        **🔬 Epidemiológico** - Análise de doenças, mortalidade, perfil demográfico

        **🗺️ Regulação** - Fluxo de pacientes, evasão e recepção entre municípios

        **🏥 Estabelecimentos** - Análise por hospital/estabelecimento de saúde

        **⚕️ Procedimentos** - Procedimentos realizados, custos e frequências

        **👥 Equidade** - Análise de equidade racial e populacional

        **📚 Metodologia** - Fontes de dados, indicadores e contatos
        """)

    with col2:
        st.markdown("""
        ### 🔍 **Como Usar os Filtros**

        **Localização à esquerda:** Use a barra lateral para aplicar filtros globais

        **📅 Período**
        - Selecione o intervalo de datas desejado
        - Por padrão: janeiro a julho/2025

        **📍 Municípios**
        - **Residência:** Onde o paciente mora
        - **Atendimento:** Onde foi internado

        **👥 Demográficos**
        - Sexo, faixa etária, raça/cor

        **🏥 Estabelecimento**
        - Filtre por hospital específico (CNES)

        **🔬 Diagnóstico**
        - Filtre por CID-10 (doença)

        ---

        ### ⚡ **Dicas de Navegação**

        ✅ **Filtros são globais** - aplicam-se a todas as abas

        ✅ **Gráficos interativos** - clique, arraste e dê zoom

        ✅ **Hover para detalhes** - passe o mouse sobre os gráficos

        ✅ **Download de dados** - botões de CSV disponíveis em várias análises

        ✅ **Responsivo** - funciona em desktop e tablet
        """)

    st.markdown("---")

    # Informações importantes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background-color: #dbeafe; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6;'>
            <h4 style='color: #1e40af; margin-top: 0;'>📊 Dados Utilizados</h4>
            <p style='color: #1e3a8a;'>
            <strong>Fonte:</strong> SIH/DATASUS<br>
            <strong>Período:</strong> Jan-Jul/2025<br>
            <strong>Local:</strong> Minas Gerais<br>
            <strong>Tipo:</strong> Internações hospitalares
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color: #dcfce7; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981;'>
            <h4 style='color: #047857; margin-top: 0;'>✨ Recursos</h4>
            <p style='color: #065f46;'>
            ✅ 7 painéis temáticos<br>
            ✅ Visualizações interativas<br>
            ✅ Filtros dinâmicos<br>
            ✅ Export de dados (CSV)
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background-color: #fef3c7; padding: 20px; border-radius: 10px; border-left: 5px solid #f59e0b;'>
            <h4 style='color: #92400e; margin-top: 0;'>📧 Contato</h4>
            <p style='color: #78350f;'>
            <strong>Email:</strong><br>
            pedrowilliamrd@gmail.com<br><br>
            <strong>Mais info:</strong> Aba Metodologia
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.info("💡 **Comece explorando:** Selecione uma das abas acima para iniciar sua análise!")

# ============================================================================
# PAINEL 1: GERAL (GESTÃO E FINANÇAS)
# ============================================================================

def painel_geral(df):
    """Painel de visão geral - gestão e finanças"""
    
    st.title("📊 Painel Geral - Gestão e Finanças")
    st.markdown("---")
    
    # KPIs principais

    
    
    total_internacoes = len(df)
    st.metric(
        label="🏥 Total de Internações",
        value=formatar_numero(total_internacoes)
    )
    
    
    if 'DIAS_PERM' in df.columns:
        media_permanencia = df['DIAS_PERM'].mean()
        st.metric(
            label="⏱️ Média de Permanência",
            value=f"{media_permanencia:.1f} dias"
        )
    
    
    if 'MORTE' in df.columns:
        taxa_mortalidade = (df['MORTE'].sum() / len(df)) * 100
        st.metric(
            label="💔 Taxa de Mortalidade",
            value=formatar_percentual(taxa_mortalidade)
        )
    
    
    if 'DIAS_UTI' in df.columns and 'DIAS_PERM' in df.columns:
        dias_uti = df['DIAS_UTI'].sum()
        dias_total = df['DIAS_PERM'].sum()
        taxa_uti = (dias_uti / dias_total * 100) if dias_total > 0 else 0

        # Adicionar aviso se não houver UTI
        help_text = "⚠️ Nenhum registro de UTI no período" if dias_uti == 0 else None

        st.metric(
            label="🏥 Taxa de Uso de UTI",
            value=formatar_percentual(taxa_uti),
            help=help_text
        )
    
    
    if 'VAL_TOT' in df.columns:
        custo_medio = df['VAL_TOT'].mean()
        st.metric(
            label="💰 Custo Médio por AIH",
            value=formatar_moeda(custo_medio)
        )
    
    st.markdown("---")
    
    # Série temporal
    if 'DATA_CMPT' in df.columns:
        st.subheader("📈 Evolução Mensal de Internações")
        st.markdown("*Gráfico de barras mostrando a evolução do volume de internações ao longo dos meses*")

        df_temporal = df.groupby(df['DATA_CMPT'].dt.to_period('M')).size().reset_index(name='Total')
        df_temporal['DATA_CMPT'] = df_temporal['DATA_CMPT'].dt.to_timestamp()

        fig_temporal = px.bar(
            df_temporal,
            x='DATA_CMPT',
            y='Total',
            title='',
            labels={'DATA_CMPT': 'Período', 'Total': 'Número de Internações'},
            color='Total',
            color_continuous_scale='Blues',
            text='Total'
        )
        fig_temporal.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_temporal.update_layout(height=400, hovermode='x unified', showlegend=False)

        st.plotly_chart(fig_temporal, use_container_width=True)
    
    st.markdown("---")
    
    # Visualizações lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Distribuição Geográfica de Internações")
        st.markdown("*Treemap mostrando a distribuição de internações por município de residência*")

        if 'NOME_MUNIC_RES' in df.columns:
            df_municipio = df.groupby('NOME_MUNIC_RES').size().reset_index(name='Total')
            df_municipio = df_municipio.nlargest(15, 'Total')

            fig_mapa = px.treemap(
                df_municipio,
                path=['NOME_MUNIC_RES'],
                values='Total',
                title='',
                color='Total',
                color_continuous_scale='Blues'
            )
            fig_mapa.update_traces(textinfo='label+value')
            fig_mapa.update_layout(height=500)
            st.plotly_chart(fig_mapa, use_container_width=True)
        else:
            st.info("Coluna NOME_MUNIC_RES não disponível")
    
    with col2:
        st.subheader("💸 Top 15 Municípios - Gastos com Internações")
        st.markdown("*Gráfico de colunas mostrando os municípios com maiores gastos em internações*")

        if 'NOME_MUNIC_RES' in df.columns and 'VAL_TOT' in df.columns:
            df_gastos = df.groupby('NOME_MUNIC_RES')['VAL_TOT'].sum().reset_index()
            df_gastos = df_gastos.nlargest(15, 'VAL_TOT')
            df_gastos['VAL_TOT_MI'] = df_gastos['VAL_TOT'] / 1_000_000

            fig_gastos = px.bar(
                df_gastos,
                x='NOME_MUNIC_RES',
                y='VAL_TOT_MI',
                title='',
                labels={'NOME_MUNIC_RES': 'Município', 'VAL_TOT_MI': 'Valor (R$ Milhões)'},
                color='VAL_TOT_MI',
                color_continuous_scale='Greens',
                text='VAL_TOT_MI'
            )
            fig_gastos.update_traces(texttemplate='R$ %{text:.2f}M', textposition='outside')
            fig_gastos.update_layout(height=500, showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_gastos, use_container_width=True)
        else:
            st.info("Colunas NOME_MUNIC_RES ou VAL_TOT não disponíveis")
    
    st.markdown("---")
    
    # Tabela resumo
    st.subheader("📋 Resumo por Município")

    if 'NOME_MUNIC_RES' in df.columns:
        # Agregar dados por município
        resumo = df.groupby('NOME_MUNIC_RES').agg({
            'NOME_MUNIC_RES': 'count',
            'DIAS_PERM': 'mean' if 'DIAS_PERM' in df.columns else 'count',
            'MORTE': 'sum' if 'MORTE' in df.columns else 'count',
            'VAL_TOT': ['sum', 'mean'] if 'VAL_TOT' in df.columns else 'count'
        }).reset_index()
        
        # Renomear colunas
        resumo.columns = ['Município', 'Total_Internações', 'Média_Permanência', 'Total_Óbitos', 'Custo_Total', 'Custo_Médio']
        
        # Calcular taxa de mortalidade
        if 'Total_Óbitos' in resumo.columns:
            resumo['Mortalidade_%'] = (resumo['Total_Óbitos'] / resumo['Total_Internações'] * 100).round(1)
        
        # Formatar valores
        resumo_display = resumo.copy()
        if 'Média_Permanência' in resumo_display.columns:
            resumo_display['Média_Permanência'] = resumo_display['Média_Permanência'].round(1)
        if 'Custo_Total' in resumo_display.columns:
            resumo_display['Custo_Total'] = resumo_display['Custo_Total'].apply(lambda x: formatar_moeda(x))
        if 'Custo_Médio' in resumo_display.columns:
            resumo_display['Custo_Médio'] = resumo_display['Custo_Médio'].apply(lambda x: formatar_moeda(x))
        
        st.dataframe(resumo_display, height=400, use_container_width=True)
        
        # Botão de download
        csv = resumo.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"resumo_municipios_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# ============================================================================
# PAINEL 2: EPIDEMIOLÓGICO
# ============================================================================

def painel_epidemiologico(df):
    """Painel de análise epidemiológica"""
    
    st.title("🔬 Painel Epidemiológico")
    st.markdown("---")
    
    # Determinar coluna de CID
    col_cid = 'DIAG_PRINC' if 'DIAG_PRINC' in df.columns else 'CID_PRINC' if 'CID_PRINC' in df.columns else None
    
    # Cards epidemiológicos
    
    

    if 'NOME_CID_PRINC' in df.columns:
        cid_prevalente = df['NOME_CID_PRINC'].mode()[0] if len(df['NOME_CID_PRINC'].mode()) > 0 else 'N/A'
        st.metric(
            label="🦠 Doença Mais Prevalente",
            value=str(cid_prevalente)
        )
    elif col_cid and col_cid in df.columns:
        cid_prevalente = df[col_cid].mode()[0] if len(df[col_cid].mode()) > 0 else 'N/A'
        st.metric(
            label="🦠 CID Mais Prevalente",
            value=str(cid_prevalente)
        )

    
    # Usar CID principal dos casos que resultaram em morte
    if 'NOME_CID_PRINC' in df.columns and 'MORTE' in df.columns:
        df_obitos = df[df['MORTE'] == 1]
        if len(df_obitos) > 0:
            cid_morte = df_obitos['NOME_CID_PRINC'].mode()
            cid_morte_valor = cid_morte[0] if len(cid_morte) > 0 else 'N/A'
            st.metric(
                label="☠️ CID Mais Freq. em Óbitos",
                value=str(cid_morte_valor),
                help="Diagnóstico principal mais frequente nas internações que resultaram em óbito"
            )
        else:
            st.metric(
                label="☠️ CID Mais Freq. em Óbitos",
                value="Sem óbitos"
            )
    elif col_cid and col_cid in df.columns and 'MORTE' in df.columns:
        df_obitos = df[df['MORTE'] == 1]
        if len(df_obitos) > 0:
            cid_morte = df_obitos[col_cid].mode()
            cid_morte_valor = cid_morte[0] if len(cid_morte) > 0 else 'N/A'
            st.metric(
                label="☠️ CID Mais Freq. em Óbitos",
                value=str(cid_morte_valor),
                help="Diagnóstico principal mais frequente nas internações que resultaram em óbito"
            )
        else:
            st.metric(
                label="☠️ CID Mais Freq. em Óbitos",
                value="Sem óbitos"
            )
    else:
        st.metric(
            label="☠️ CID Mais Freq. em Óbitos",
            value="N/A",
            help="Dados de óbitos não disponíveis"
        )
    
    
    if 'FAIXA_ETARIA' in df.columns:
        faixa_modal = df['FAIXA_ETARIA'].mode()[0] if len(df['FAIXA_ETARIA'].mode()) > 0 else 'N/A'
        st.metric(
            label="👤 Faixa Etária Modal",
            value=str(faixa_modal)
        )
    
    
    if 'CID_SECUN' in df.columns and df['CID_SECUN'].notna().sum() > 0:
        perc_comorbidade = (df['CID_SECUN'].notna().sum() / len(df) * 100)
        st.metric(
            label="🔗 % com Comorbidades",
            value=formatar_percentual(perc_comorbidade)
        )
    else:
        st.metric(
            label="🔗 % com Comorbidades",
            value="N/A",
            help="CID secundário não disponível na base de dados"
        )
    
    st.markdown("---")
    
    # Top 10 Diagnósticos
    st.subheader("🦠 Principais Diagnósticos (CID-10 Principal)")
    st.markdown("*Top 10 doenças com maior número de internações*")

    if 'NOME_CID_PRINC' in df.columns:
        top_cids = df['NOME_CID_PRINC'].value_counts().head(10).reset_index()
        top_cids.columns = ['Doença', 'Total']
        top_cids['Percentual'] = (top_cids['Total'] / len(df) * 100).round(1)

        fig_cids = px.bar(
            top_cids,
            y='Doença',
            x='Total',
            orientation='h',
            title='',
            labels={'Doença': 'Diagnóstico', 'Total': 'Número de Casos'},
            color='Total',
            color_continuous_scale='Reds',
            text='Percentual'
        )
        fig_cids.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_cids.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cids, use_container_width=True)
    elif col_cid and col_cid in df.columns:
        top_cids = df[col_cid].value_counts().head(10).reset_index()
        top_cids.columns = ['CID', 'Total']
        top_cids['Percentual'] = (top_cids['Total'] / len(df) * 100).round(1)

        fig_cids = px.bar(
            top_cids,
            y='CID',
            x='Total',
            orientation='h',
            title='',
            labels={'CID': 'Diagnóstico (CID)', 'Total': 'Número de Casos'},
            color='Total',
            color_continuous_scale='Reds',
            text='Percentual'
        )
        fig_cids.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_cids.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cids, use_container_width=True)
    else:
        st.warning("Coluna de CID principal não encontrada nos dados")
    
    st.markdown("---")
    
    # Análise demográfica
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Distribuição Etária por Sexo")
        
        if 'FAIXA_ETARIA' in df.columns and 'SEXO' in df.columns:
            df_piramide = df.groupby(['FAIXA_ETARIA', 'SEXO']).size().reset_index(name='Total')
            df_piramide_masc = df_piramide[df_piramide['SEXO'] == 'Masculino'].copy()
            df_piramide_masc['Total'] = -df_piramide_masc['Total']
            df_piramide_fem = df_piramide[df_piramide['SEXO'] == 'Feminino']
            
            fig_piramide = go.Figure()
            
            fig_piramide.add_trace(go.Bar(
                y=df_piramide_masc['FAIXA_ETARIA'],
                x=df_piramide_masc['Total'],
                name='Masculino',
                orientation='h',
                marker=dict(color='#1f77b4')
            ))
            
            fig_piramide.add_trace(go.Bar(
                y=df_piramide_fem['FAIXA_ETARIA'],
                x=df_piramide_fem['Total'],
                name='Feminino',
                orientation='h',
                marker=dict(color='#ff69b4')
            ))
            
            fig_piramide.update_layout(
                barmode='relative',
                height=500,
                xaxis=dict(title='População'),
                yaxis=dict(title='Faixa Etária'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02)
            )
            
            st.plotly_chart(fig_piramide, use_container_width=True)
        else:
            st.info("Colunas FAIXA_ETARIA ou SEXO não disponíveis")
    
    with col2:
        st.subheader("⚧ Internações por Sexo")
        
        if 'SEXO' in df.columns:
            df_sexo = df['SEXO'].value_counts().reset_index()
            df_sexo.columns = ['Sexo', 'Total']
            
            colors_sexo = {'Masculino': '#1f77b4', 'Feminino': '#ff69b4', 'Ignorado': '#95a5a6'}
            
            fig_sexo = px.pie(
                df_sexo,
                values='Total',
                names='Sexo',
                title='',
                color='Sexo',
                color_discrete_map=colors_sexo
            )
            fig_sexo.update_traces(textposition='inside', textinfo='percent+label')
            fig_sexo.update_layout(height=500)
            st.plotly_chart(fig_sexo, use_container_width=True)
        else:
            st.info("Coluna SEXO não disponível")
    
    st.markdown("---")
    
    # Análise de Mortalidade
    st.subheader("💀 Análise de Mortalidade Hospitalar")

    if 'MORTE' in df.columns:
        tab1, tab2, tab3, tab4 = st.tabs(["Por CID", "Por Faixa Etária", "Por Município", "Por Raça/Cor"])

        with tab1:
            if 'NOME_CID_PRINC' in df.columns:
                df_mort_cid = df.groupby('NOME_CID_PRINC').agg({
                    'MORTE': ['sum', 'count']
                }).reset_index()
                df_mort_cid.columns = ['Doença', 'Óbitos', 'Total']
                df_mort_cid['Taxa_Mortalidade'] = (df_mort_cid['Óbitos'] / df_mort_cid['Total'] * 100)
                df_mort_cid = df_mort_cid[df_mort_cid['Total'] >= 10]  # Filtrar doenças com poucos casos
                df_mort_cid = df_mort_cid.nlargest(10, 'Taxa_Mortalidade')

                fig_mort_cid = px.bar(
                    df_mort_cid,
                    y='Doença',
                    x='Taxa_Mortalidade',
                    orientation='h',
                    title='Top 10 Doenças com Maior Taxa de Mortalidade',
                    labels={'Doença': 'Diagnóstico', 'Taxa_Mortalidade': 'Taxa de Mortalidade (%)'},
                    color='Taxa_Mortalidade',
                    color_continuous_scale='Reds'
                )
                fig_mort_cid.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_mort_cid, use_container_width=True)
            elif col_cid and col_cid in df.columns:
                df_mort_cid = df.groupby(col_cid).agg({
                    'MORTE': ['sum', 'count']
                }).reset_index()
                df_mort_cid.columns = ['CID', 'Óbitos', 'Total']
                df_mort_cid['Taxa_Mortalidade'] = (df_mort_cid['Óbitos'] / df_mort_cid['Total'] * 100)
                df_mort_cid = df_mort_cid[df_mort_cid['Total'] >= 10]  # Filtrar CIDs com poucos casos
                df_mort_cid = df_mort_cid.nlargest(10, 'Taxa_Mortalidade')
                
                fig_mort_cid = px.bar(
                    df_mort_cid,
                    y='CID',
                    x='Taxa_Mortalidade',
                    orientation='h',
                    title='Top 10 CIDs com Maior Taxa de Mortalidade',
                    labels={'CID': 'Diagnóstico', 'Taxa_Mortalidade': 'Taxa de Mortalidade (%)'},
                    color='Taxa_Mortalidade',
                    color_continuous_scale='Reds'
                )
                fig_mort_cid.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_mort_cid, use_container_width=True)
        
        with tab2:
            if 'FAIXA_ETARIA' in df.columns:
                df_mort_idade = df.groupby('FAIXA_ETARIA').agg({
                    'MORTE': ['sum', 'count']
                }).reset_index()
                df_mort_idade.columns = ['Faixa_Etária', 'Óbitos', 'Total']
                df_mort_idade['Taxa_Mortalidade'] = (df_mort_idade['Óbitos'] / df_mort_idade['Total'] * 100)
                
                fig_mort_idade = px.line(
                    df_mort_idade,
                    x='Faixa_Etária',
                    y='Taxa_Mortalidade',
                    title='Taxa de Mortalidade por Faixa Etária',
                    labels={'Faixa_Etária': 'Faixa Etária', 'Taxa_Mortalidade': 'Taxa de Mortalidade (%)'},
                    markers=True
                )
                fig_mort_idade.update_traces(line_color='#e74c3c', line_width=3)
                fig_mort_idade.update_layout(height=400)
                st.plotly_chart(fig_mort_idade, use_container_width=True)
        
        with tab3:
            if 'NOME_MUNIC_RES' in df.columns:
                df_mort_mun = df.groupby('NOME_MUNIC_RES').agg({
                    'MORTE': ['sum', 'count']
                }).reset_index()
                df_mort_mun.columns = ['Município', 'Óbitos', 'Total_Internações']
                df_mort_mun['Taxa_Mortalidade_%'] = (df_mort_mun['Óbitos'] / df_mort_mun['Total_Internações'] * 100).round(1)
                df_mort_mun = df_mort_mun.sort_values('Taxa_Mortalidade_%', ascending=False)

                st.dataframe(df_mort_mun, height=400, use_container_width=True)

        with tab4:
            if 'RACA_COR' in df.columns:
                df_mort_raca = df.groupby('RACA_COR').agg({
                    'MORTE': ['sum', 'count']
                }).reset_index()
                df_mort_raca.columns = ['Raça_Cor', 'Óbitos', 'Total']
                df_mort_raca['Taxa_Mortalidade'] = (df_mort_raca['Óbitos'] / df_mort_raca['Total'] * 100)

                fig_mort_raca = px.bar(
                    df_mort_raca,
                    x='Raça_Cor',
                    y='Taxa_Mortalidade',
                    title='Taxa de Mortalidade por Raça/Cor',
                    labels={'Raça_Cor': 'Raça/Cor', 'Taxa_Mortalidade': 'Taxa de Mortalidade (%)'},
                    color='Taxa_Mortalidade',
                    color_continuous_scale='Reds',
                    text='Taxa_Mortalidade'
                )
                fig_mort_raca.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_mort_raca.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_mort_raca, use_container_width=True)

# ============================================================================
# PAINEL 3: REGULAÇÃO E TERRITÓRIO
# ============================================================================

def painel_regulacao(df):
    """Painel de análise de fluxo e regulação"""
    
    st.title("🗺️ Painel de Regulação e Território")
    st.markdown("---")
    
    # Cards de regulação - Um embaixo do outro
    if 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        evasao = (df['MUNIC_RES'] != df['MUNIC_MOV']).sum()
        perc_evasao = (evasao / len(df) * 100)
        st.metric(
            label="🚑 Evasão Total",
            value=formatar_percentual(perc_evasao),
            help="Percentual de pacientes que buscam atendimento fora do município de residência"
        )

    if 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        evasao_por_mun = df[df['MUNIC_RES'] != df['MUNIC_MOV']].groupby('MUNIC_RES').size()
        total_por_mun = df.groupby('MUNIC_RES').size()
        perc_evasao_mun = (evasao_por_mun / total_por_mun * 100)
        municipios_alta_evasao = (perc_evasao_mun > 50).sum()
        st.metric(
            label="⚠️ Municípios >50% Evasão",
            value=municipios_alta_evasao,
            help="Número de municípios onde mais da metade dos pacientes buscam atendimento em outros municípios"
        )

    if 'NOME_MUNIC_MOV' in df.columns and 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        df_externos = df[df['MUNIC_RES'] != df['MUNIC_MOV']]
        if len(df_externos) > 0:
            principal_receptor = df_externos['NOME_MUNIC_MOV'].mode()[0] if len(df_externos) > 0 else 'N/A'
            st.metric(
                label="🏥 Principal Município Receptor",
                value=str(principal_receptor),
                help="Município que mais recebe pacientes de outros municípios"
            )
    
    st.markdown("---")
    
    # Análise de evasão e atração - Gráficos de barras um embaixo do outro
    st.subheader("🚪 Municípios com Maior Evasão")
    st.markdown("*Volume absoluto de pacientes que buscam atendimento fora do município*")

    if 'NOME_MUNIC_RES' in df.columns and 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        df_evasao = df[df['MUNIC_RES'] != df['MUNIC_MOV']].groupby('NOME_MUNIC_RES').size().reset_index(name='Evadidos')
        df_evasao = df_evasao.nlargest(15, 'Evadidos')

        fig_evasao = px.bar(
            df_evasao,
            y='NOME_MUNIC_RES',
            x='Evadidos',
            orientation='h',
            title='',
            labels={'NOME_MUNIC_RES': 'Município', 'Evadidos': 'Número de Pacientes Evadidos'},
            color='Evadidos',
            color_continuous_scale='Reds',
            text='Evadidos'
        )
        fig_evasao.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_evasao.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_evasao, use_container_width=True)

    st.markdown("---")

    st.subheader("🏥 Municípios que Mais Recebem Pacientes Externos")
    st.markdown("*Volume absoluto de pacientes vindos de outros municípios*")

    if 'NOME_MUNIC_MOV' in df.columns and 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        df_atrator = df[df['MUNIC_RES'] != df['MUNIC_MOV']].groupby('NOME_MUNIC_MOV').size().reset_index(name='Pacientes_Externos')
        df_atrator = df_atrator.nlargest(15, 'Pacientes_Externos')

        fig_atrator = px.bar(
            df_atrator,
            y='NOME_MUNIC_MOV',
            x='Pacientes_Externos',
            orientation='h',
            title='',
            labels={'NOME_MUNIC_MOV': 'Município', 'Pacientes_Externos': 'Pacientes Recebidos'},
            color='Pacientes_Externos',
            color_continuous_scale='Greens',
            text='Pacientes_Externos'
        )
        fig_atrator.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_atrator.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_atrator, use_container_width=True)
    
    st.markdown("---")
    
    # Bubble plot
    st.subheader("📊 Análise de Oferta e Demanda por Município")
    
    if 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        df_demanda = df.groupby('MUNIC_RES').size().reset_index(name='Demanda')
        df_oferta = df.groupby('MUNIC_MOV').size().reset_index(name='Oferta')
        
        df_bubble = df_demanda.merge(df_oferta, left_on='MUNIC_RES', right_on='MUNIC_MOV', how='outer').fillna(0)
        df_bubble['Município'] = df_bubble['MUNIC_RES'].fillna(df_bubble['MUNIC_MOV'])
        df_bubble['Autossuficiência'] = (df_bubble['Oferta'] / df_bubble['Demanda'] * 100).fillna(0)
        df_bubble = df_bubble[df_bubble['Demanda'] > 0]
        
        fig_bubble = px.scatter(
            df_bubble,
            x='Oferta',
            y='Demanda',
            size='Demanda',
            color='Autossuficiência',
            hover_data=['Município'],
            title='',
            labels={'Oferta': 'Internações Realizadas (Oferta)', 'Demanda': 'Residentes Internados (Demanda)'},
            color_continuous_scale='RdYlGn'
        )
        
        # Linha de referência (autossuficiência perfeita)
        max_val = max(df_bubble['Oferta'].max(), df_bubble['Demanda'].max())
        fig_bubble.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Autossuficiência',
            line=dict(dash='dash', color='gray')
        ))
        
        fig_bubble.update_layout(height=500)
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela de estabelecimentos receptores
    st.subheader("🏥 Estabelecimentos que Mais Recebem Pacientes Externos")
    st.markdown("*Top 20 estabelecimentos com maior percentual de pacientes externos*")

    if 'CNES' in df.columns and 'MUNIC_RES' in df.columns and 'MUNIC_MOV' in df.columns:
        df_externos = df[df['MUNIC_RES'] != df['MUNIC_MOV']]

        df_estab = df.groupby('CNES').size().reset_index(name='Total_Internações')
        df_estab_ext = df_externos.groupby('CNES').size().reset_index(name='Pacientes_Externos')

        df_estab = df_estab.merge(df_estab_ext, on='CNES', how='left').fillna(0)
        df_estab['Perc_Externos'] = (df_estab['Pacientes_Externos'] / df_estab['Total_Internações'] * 100).round(1)

        if 'NOME_FANTASIA' in df.columns and 'NOME_MUNIC_MOV' in df.columns:
            df_nome = df[['CNES', 'NOME_FANTASIA', 'NOME_MUNIC_MOV']].drop_duplicates('CNES')
            df_estab = df_estab.merge(df_nome, on='CNES', how='left')
        elif 'NOME_FANTASIA' in df.columns:
            df_nome = df[['CNES', 'NOME_FANTASIA', 'MUNIC_MOV']].drop_duplicates('CNES')
            df_estab = df_estab.merge(df_nome, on='CNES', how='left')

        df_estab = df_estab.sort_values('Perc_Externos', ascending=False).head(20)

        st.dataframe(df_estab, height=400, use_container_width=True)

# ============================================================================
# PAINEL 4: POR ESTABELECIMENTO
# ============================================================================

def painel_estabelecimento(df):
    """Painel de análise por estabelecimento (CNES)"""
    
    st.title("🏥 Painel por Estabelecimento (CNES)")
    st.markdown("---")
    
    if 'CNES' not in df.columns:
        st.warning("Coluna CNES não disponível nos dados")
        return
    
    # Seletor de estabelecimento
    st.subheader("🔍 Selecione um Estabelecimento para Análise Detalhada")
    
    if 'NOME_FANTASIA' in df.columns:
        df_cnes = df[['CNES', 'NOME_FANTASIA', 'MUNIC_MOV']].drop_duplicates('CNES').dropna().copy()
        # Converter para string para evitar erro com categorical
        df_cnes['NOME_FANTASIA'] = df_cnes['NOME_FANTASIA'].astype(str)
        df_cnes['MUNIC_MOV'] = df_cnes['MUNIC_MOV'].astype(str)
        df_cnes['display'] = df_cnes['CNES'].astype(str) + ' - ' + df_cnes['NOME_FANTASIA'] + ' (' + df_cnes['MUNIC_MOV'] + ')'
        
        cnes_selecionado = st.selectbox(
            "Estabelecimento",
            options=df_cnes['CNES'].tolist(),
            format_func=lambda x: df_cnes[df_cnes['CNES'] == x]['display'].iloc[0] if len(df_cnes[df_cnes['CNES'] == x]) > 0 else str(x)
        )
    else:
        cnes_selecionado = st.selectbox(
            "CNES",
            options=sorted(df['CNES'].dropna().unique())
        )
    
    if cnes_selecionado:
        df_cnes_sel = df[df['CNES'] == cnes_selecionado]
        
        st.markdown("---")
        
        # Perfil do estabelecimento
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_int = len(df_cnes_sel)
            st.metric(
                label="📊 Total de Internações",
                value=formatar_numero(total_int)
            )
        
        with col2:
            if 'DIAS_PERM' in df.columns:
                media_perm = df_cnes_sel['DIAS_PERM'].mean()
                st.metric(
                    label="⏱️ Média de Permanência",
                    value=f"{media_perm:.1f} dias"
                )
        
        with col3:
            if 'MORTE' in df.columns:
                taxa_mort = (df_cnes_sel['MORTE'].sum() / len(df_cnes_sel) * 100)
                st.metric(
                    label="💔 Taxa de Mortalidade",
                    value=formatar_percentual(taxa_mort)
                )
        
        with col4:
            if 'VAL_TOT' in df.columns:
                custo_medio = df_cnes_sel['VAL_TOT'].mean()
                st.metric(
                    label="💰 Custo Médio",
                    value=formatar_moeda(custo_medio)
                )
    
    st.markdown("---")
    
    # Ranking de hospitais
    st.subheader("📊 Ranking de Estabelecimentos por Volume")
    
    criterio = st.selectbox(
        "Critério de Ranking",
        options=['Volume de Internações', 'Custo Total', 'Média de Permanência', 'Taxa de Mortalidade']
    )
    
    agg_dict = {}
    if 'VAL_TOT' in df.columns:
        agg_dict['VAL_TOT'] = 'sum'
    if 'DIAS_PERM' in df.columns:
        agg_dict['DIAS_PERM'] = 'mean'
    if 'MORTE' in df.columns:
        agg_dict['MORTE'] = 'sum'

    df_ranking = df.groupby('CNES', as_index=False).agg(agg_dict)
    df_ranking.insert(1, 'Volume', df.groupby('CNES').size().values)

    # Renomear colunas
    rename_map = {'CNES': 'CNES'}
    if 'VAL_TOT' in agg_dict:
        rename_map['VAL_TOT'] = 'Custo_Total'
    if 'DIAS_PERM' in agg_dict:
        rename_map['DIAS_PERM'] = 'Media_Permanencia'
    if 'MORTE' in agg_dict:
        rename_map['MORTE'] = 'Total_Obitos'
    df_ranking = df_ranking.rename(columns=rename_map)
    df_ranking['Taxa_Mortalidade'] = (df_ranking['Total_Obitos'] / df_ranking['Volume'] * 100)
    
    if 'NOME_FANTASIA' in df.columns:
        df_nome = df[['CNES', 'NOME_FANTASIA']].drop_duplicates('CNES')
        df_ranking = df_ranking.merge(df_nome, on='CNES', how='left')
        df_ranking['Label'] = df_ranking['NOME_FANTASIA'].fillna(df_ranking['CNES'].astype(str))
    else:
        df_ranking['Label'] = df_ranking['CNES'].astype(str)
    
    # Ordenar conforme critério
    if criterio == 'Volume de Internações':
        df_ranking = df_ranking.nlargest(20, 'Volume')
        coluna_plot = 'Volume'
    elif criterio == 'Custo Total':
        df_ranking = df_ranking.nlargest(20, 'Custo_Total')
        coluna_plot = 'Custo_Total'
    elif criterio == 'Média de Permanência':
        df_ranking = df_ranking.nlargest(20, 'Media_Permanencia')
        coluna_plot = 'Media_Permanencia'
    else:
        df_ranking = df_ranking.nlargest(20, 'Taxa_Mortalidade')
        coluna_plot = 'Taxa_Mortalidade'
    
    fig_ranking = px.bar(
        df_ranking,
        y='Label',
        x=coluna_plot,
        orientation='h',
        title='',
        labels={'Label': 'Estabelecimento', coluna_plot: criterio},
        color=coluna_plot,
        color_continuous_scale='Blues'
    )
    fig_ranking.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_ranking, use_container_width=True)

# ============================================================================
# PAINEL 5: PROCEDIMENTOS
# ============================================================================

def painel_procedimentos(df):
    """Painel de análise de procedimentos"""
    
    st.title("⚕️ Painel de Procedimentos")
    st.markdown("---")
    
    # Determinar colunas de procedimento
    col_proc_nome = 'NOME_PROC_REA' if 'NOME_PROC_REA' in df.columns else None
    col_proc_real = 'PROC_REA' if 'PROC_REA' in df.columns else 'PROCEDIMENTO' if 'PROCEDIMENTO' in df.columns else None
    col_proc_soli = 'PROC_SOLI' if 'PROC_SOLI' in df.columns else None

    if not col_proc_real and not col_proc_nome:
        st.warning("Coluna de procedimento não encontrada nos dados")
        return


    col_to_use = col_proc_nome if col_proc_nome else col_proc_real
    total_proc_distintos = df[col_to_use].nunique()
    st.metric(
        label="🔢 Procedimentos Distintos",
        value=formatar_numero(total_proc_distintos)
    )

    
    col_to_use = col_proc_nome if col_proc_nome else col_proc_real
    proc_mais_comum = df[col_to_use].mode()[0] if len(df[col_to_use].mode()) > 0 else 'N/A'
    st.metric(
        label="⚕️ Procedimento Mais Realizado",
        value=str(proc_mais_comum)
    )

    
    if 'VAL_TOT' in df.columns:
        col_to_use = col_proc_nome if col_proc_nome else col_proc_real
        df_proc_valor = df.groupby(col_to_use)['VAL_TOT'].mean()
        proc_mais_caro = df_proc_valor.idxmax() if len(df_proc_valor) > 0 else 'N/A'
        st.metric(
            label="💎 Procedimento Mais Caro",
            value=str(proc_mais_caro)
        )
    
    
    if 'VAL_TOT' in df.columns:
        gasto_total = df['VAL_TOT'].sum()
        st.metric(
            label="💰 Gasto Total",
            value=formatar_moeda(gasto_total)
        )
    
    st.markdown("---")
    
    # Top procedimentos
    st.subheader("📊 Procedimentos Mais Frequentes")
    st.markdown("*Treemap mostrando os 15 procedimentos mais realizados*")

    col_to_use = col_proc_nome if col_proc_nome else col_proc_real
    top_proc = df[col_to_use].value_counts().head(15).reset_index()
    top_proc.columns = ['Procedimento', 'Quantidade']

    fig_proc = px.treemap(
        top_proc,
        path=['Procedimento'],
        values='Quantidade',
        title='',
        color='Quantidade',
        color_continuous_scale='Blues'
    )
    fig_proc.update_traces(textinfo='label+value')
    fig_proc.update_layout(height=500)
    st.plotly_chart(fig_proc, use_container_width=True)
    
    st.markdown("---")
    
    # Análise de custos
    if 'VAL_TOT' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💸 Top 15 Procedimentos por Gasto Total")
            st.markdown("*Treemap mostrando os procedimentos com maior gasto total*")

            col_to_use = col_proc_nome if col_proc_nome else col_proc_real
            df_gasto = df.groupby(col_to_use)['VAL_TOT'].sum().reset_index()
            df_gasto.columns = ['Procedimento', 'Gasto_Total']
            df_gasto = df_gasto.nlargest(15, 'Gasto_Total')
            df_gasto['Gasto_MI'] = df_gasto['Gasto_Total'] / 1_000_000

            fig_gasto = px.treemap(
                df_gasto,
                path=['Procedimento'],
                values='Gasto_Total',
                title='',
                color='Gasto_MI',
                color_continuous_scale='Greens'
            )
            fig_gasto.update_traces(textinfo='label+value')
            fig_gasto.update_layout(height=500)
            st.plotly_chart(fig_gasto, use_container_width=True)
        
        with col2:
            st.subheader("💎 Procedimentos Mais Caros (Custo Médio)")
            st.markdown("*Treemap dos procedimentos com maior custo médio (mín. 50 casos)*")

            col_to_use = col_proc_nome if col_proc_nome else col_proc_real
            df_custo_medio = df.groupby(col_to_use, as_index=False).agg({
                'VAL_TOT': ['mean', 'count']
            })
            df_custo_medio.columns = ['Procedimento', 'Custo_Medio', 'Quantidade']
            df_custo_medio = df_custo_medio[df_custo_medio['Quantidade'] >= 50]  # Filtrar outliers
            df_custo_medio = df_custo_medio.nlargest(15, 'Custo_Medio')

            fig_custo_medio = px.treemap(
                df_custo_medio,
                path=['Procedimento'],
                values='Quantidade',
                title='',
                color='Custo_Medio',
                color_continuous_scale='Reds'
            )
            fig_custo_medio.update_traces(textinfo='label+text')
            fig_custo_medio.update_layout(height=500)
            st.plotly_chart(fig_custo_medio, use_container_width=True)
    
    st.markdown("---")
    
    # Heatmap CID x Procedimento
    st.subheader("🔥 Correlação entre Diagnósticos e Procedimentos")
    st.markdown("*Heatmap mostrando a frequência de combinações entre diagnósticos e procedimentos*")

    col_cid_nome = 'NOME_CID_PRINC' if 'NOME_CID_PRINC' in df.columns else None
    col_cid = 'DIAG_PRINC' if 'DIAG_PRINC' in df.columns else 'CID_PRINC' if 'CID_PRINC' in df.columns else None

    if col_cid_nome and col_proc_nome:
        # Top 15 CIDs e procedimentos
        top_cids_heat = df[col_cid_nome].value_counts().head(15).index.tolist()
        top_proc_heat = df[col_proc_nome].value_counts().head(15).index.tolist()

        # Criar matriz de correlação
        df_heat = df[(df[col_cid_nome].isin(top_cids_heat)) & (df[col_proc_nome].isin(top_proc_heat))]
        matriz_corr = pd.crosstab(df_heat[col_cid_nome], df_heat[col_proc_nome])
    elif col_cid and col_proc_real:
        # Top 15 CIDs e procedimentos
        top_cids_heat = df[col_cid].value_counts().head(15).index.tolist()
        top_proc_heat = df[col_proc_real].value_counts().head(15).index.tolist()

        # Criar matriz de correlação
        df_heat = df[(df[col_cid].isin(top_cids_heat)) & (df[col_proc_real].isin(top_proc_heat))]
        matriz_corr = pd.crosstab(df_heat[col_cid], df_heat[col_proc_real])
    else:
        col_cid = None

    if col_cid or col_cid_nome:
        
        fig_heatmap = px.imshow(
            matriz_corr,
            title='',
            labels=dict(x='Procedimento', y='CID', color='Frequência'),
            color_continuous_scale='YlOrRd',
            aspect='auto'
        )
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("Coluna de CID não disponível para análise cruzada")

# ============================================================================
# PAINEL 6: POPULACIONAL E EQUIDADE
# ============================================================================

def painel_populacional(df):
    """Painel de análise populacional e equidade"""
    
    st.title("👥 Painel Populacional e Equidade")
    st.markdown("---")
    
    if 'RACA_COR' not in df.columns:
        st.warning("Coluna RACA_COR não disponível nos dados")
        return
    
    
    
    raca_modal = df['RACA_COR'].mode()[0] if len(df['RACA_COR'].mode()) > 0 else 'N/A'
    perc_modal = (df['RACA_COR'] == raca_modal).sum() / len(df) * 100
    st.metric(
        label="👤 Raça/Cor Modal",
        value=f"{raca_modal} ({perc_modal:.1f}%)"
    )

    st.markdown("---")
    
    # Distribuição por raça/cor
    st.subheader("📊 Internações por Raça/Cor")
    
    df_raca = df['RACA_COR'].value_counts().reset_index()
    df_raca.columns = ['Raça_Cor', 'Total']
    df_raca['Percentual'] = (df_raca['Total'] / df_raca['Total'].sum() * 100).round(1)
    
    fig_raca = px.bar(
        df_raca,
        x='Raça_Cor',
        y='Total',
        title='',
        labels={'Raça_Cor': 'Raça/Cor', 'Total': 'Número de Internações'},
        color='Raça_Cor',
        text='Percentual'
    )
    fig_raca.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_raca.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_raca, use_container_width=True)
    
    st.markdown("---")
    
    # Análise de desfechos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⏱️ Tempo Médio de Permanência por Raça/Cor")
        
        if 'DIAS_PERM' in df.columns:
            fig_perm = px.box(
                df,
                x='RACA_COR',
                y='DIAS_PERM',
                title='',
                labels={'RACA_COR': 'Raça/Cor', 'DIAS_PERM': 'Dias de Permanência'},
                color='RACA_COR'
            )
            fig_perm.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_perm, use_container_width=True)
    
    with col2:
        st.subheader("💔 Taxa de Mortalidade por Raça/Cor")
        
        if 'MORTE' in df.columns:
            df_mort_raca = df.groupby('RACA_COR').agg({
                'MORTE': ['sum', 'count']
            }).reset_index()
            df_mort_raca.columns = ['Raça_Cor', 'Óbitos', 'Total']
            df_mort_raca['Taxa_Mortalidade'] = (df_mort_raca['Óbitos'] / df_mort_raca['Total'] * 100)
            
            # Média geral
            taxa_media = (df['MORTE'].sum() / len(df) * 100)
            
            fig_mort_raca = px.bar(
                df_mort_raca,
                y='Raça_Cor',
                x='Taxa_Mortalidade',
                orientation='h',
                title='',
                labels={'Raça_Cor': 'Raça/Cor', 'Taxa_Mortalidade': 'Taxa de Mortalidade (%)'},
                color='Taxa_Mortalidade',
                color_continuous_scale='Reds'
            )
            
            # Adicionar linha de referência
            fig_mort_raca.add_vline(
                x=taxa_media,
                line_dash="dash",
                line_color="gray",
                annotation_text="Média Geral"
            )
            
            fig_mort_raca.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_mort_raca, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela consolidada
    st.subheader("📋 Indicadores por Raça/Cor - Visão Consolidada")
    
    agg_dict = {}
    if 'DIAS_PERM' in df.columns:
        agg_dict['DIAS_PERM'] = 'mean'
    if 'MORTE' in df.columns:
        agg_dict['MORTE'] = 'sum'
    if 'VAL_TOT' in df.columns:
        agg_dict['VAL_TOT'] = 'mean'

    df_consolidado = df.groupby('RACA_COR', as_index=False).agg(agg_dict)
    df_consolidado.insert(1, 'Total_Internações', df.groupby('RACA_COR').size().values)

    # Renomear colunas
    rename_map = {'RACA_COR': 'Raça_Cor'}
    if 'DIAS_PERM' in agg_dict:
        rename_map['DIAS_PERM'] = 'Média_Permanência'
    if 'MORTE' in agg_dict:
        rename_map['MORTE'] = 'Total_Óbitos'
    if 'VAL_TOT' in agg_dict:
        rename_map['VAL_TOT'] = 'Custo_Médio'
    df_consolidado = df_consolidado.rename(columns=rename_map)
    df_consolidado['%_Total'] = (df_consolidado['Total_Internações'] / df_consolidado['Total_Internações'].sum() * 100).round(1)
    
    if 'Total_Óbitos' in df_consolidado.columns:
        df_consolidado['Taxa_Mortalidade_%'] = (df_consolidado['Total_Óbitos'] / df_consolidado['Total_Internações'] * 100).round(1)
    
    # Formatar valores
    df_consolidado['Média_Permanência'] = df_consolidado['Média_Permanência'].round(1)
    if 'Custo_Médio' in df_consolidado.columns:
        df_consolidado['Custo_Médio'] = df_consolidado['Custo_Médio'].apply(lambda x: formatar_moeda(x))
    
    st.dataframe(df_consolidado, use_container_width=True)

# ============================================================================
# PAINEL 7: TEMPORAL / TENDÊNCIA
# ============================================================================

def painel_temporal(df):
    """Painel de análise temporal e tendências"""
    
    st.title("📈 Painel Temporal / Tendência")
    st.markdown("---")
    
    if 'DATA_CMPT' not in df.columns:
        st.warning("Coluna DATA_CMPT não disponível nos dados")
        return
    
    # Agregar dados mensais
    agg_dict = {}
    if 'MORTE' in df.columns:
        agg_dict['MORTE'] = 'sum'
    if 'VAL_TOT' in df.columns:
        agg_dict['VAL_TOT'] = 'sum'
    if 'DIAS_PERM' in df.columns:
        agg_dict['DIAS_PERM'] = 'mean'

    df_mensal = df.groupby(df['DATA_CMPT'].dt.to_period('M')).agg(agg_dict).reset_index()
    df_mensal.insert(1, 'Total_Internações', df.groupby(df['DATA_CMPT'].dt.to_period('M')).size().values)

    df_mensal['DATA_CMPT'] = df_mensal['DATA_CMPT'].dt.to_timestamp()

    # Renomear colunas
    rename_map = {'DATA_CMPT': 'Data'}
    if 'MORTE' in agg_dict:
        rename_map['MORTE'] = 'Total_Óbitos'
    if 'VAL_TOT' in agg_dict:
        rename_map['VAL_TOT'] = 'Custo_Total'
    if 'DIAS_PERM' in agg_dict:
        rename_map['DIAS_PERM'] = 'Média_Permanência'
    df_mensal = df_mensal.rename(columns=rename_map)
    
    if 'Total_Óbitos' in df_mensal.columns:
        df_mensal['Taxa_Mortalidade'] = (df_mensal['Total_Óbitos'] / df_mensal['Total_Internações'] * 100)
    
    # Cards de tendência
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if len(df_mensal) >= 2:
            variacao = ((df_mensal.iloc[-1]['Total_Internações'] - df_mensal.iloc[0]['Total_Internações']) / 
                       df_mensal.iloc[0]['Total_Internações'] * 100)
            tendencia = "↗️" if variacao > 0 else "↘️"
            st.metric(
                label="📊 Tendência Geral",
                value=f"{tendencia} {abs(variacao):.1f}%"
            )
    
    with col2:
        idx_max = df_mensal['Total_Internações'].idxmax()
        mes_max = df_mensal.loc[idx_max, 'Data'].strftime('%m/%Y')
        valor_max = df_mensal.loc[idx_max, 'Total_Internações']
        st.metric(
            label="📅 Mês com Maior Volume",
            value=mes_max,
            delta=formatar_numero(valor_max)
        )
    
    with col3:
        # Detectar sazonalidade simples (pico no inverno)
        df_mensal['Mês'] = pd.to_datetime(df_mensal['Data']).dt.month
        media_inverno = df_mensal[df_mensal['Mês'].isin([6, 7, 8])]['Total_Internações'].mean()
        media_verao = df_mensal[df_mensal['Mês'].isin([12, 1, 2])]['Total_Internações'].mean()
        sazonalidade = "Pico no Inverno" if media_inverno > media_verao else "Pico no Verão"
        st.metric(
            label="🌡️ Sazonalidade",
            value=sazonalidade
        )
    
    with col4:
        if len(df_mensal) >= 3:
            # Projeção simples (média móvel)
            projecao = df_mensal['Total_Internações'].tail(3).mean()
            st.metric(
                label="🔮 Projeção Próximo Mês",
                value=formatar_numero(projecao)
            )
    
    st.markdown("---")
    
    # Série temporal principal
    st.subheader("📊 Evolução Completa de Internações no Período")
    
    fig_serie = px.area(
        df_mensal,
        x='Data',
        y='Total_Internações',
        title='',
        labels={'Data': 'Período', 'Total_Internações': 'Número de Internações'}
    )
    fig_serie.update_traces(line_color='#1f77b4', fillcolor='rgba(31, 119, 180, 0.3)')
    fig_serie.update_layout(height=450, hovermode='x unified')
    st.plotly_chart(fig_serie, use_container_width=True)
    
    st.markdown("---")
    
    # Análise de sazonalidade
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Padrão Médio Mensal")
        
        df_mensal['Mês_Nome'] = pd.to_datetime(df_mensal['Data']).dt.strftime('%b')
        df_sazonal = df_mensal.groupby('Mês_Nome')['Total_Internações'].mean().reset_index()
        
        # Ordenar meses
        meses_ordem = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df_sazonal['Mês_Nome'] = pd.Categorical(df_sazonal['Mês_Nome'], categories=meses_ordem, ordered=True)
        df_sazonal = df_sazonal.sort_values('Mês_Nome')
        
        fig_sazonal = px.bar(
            df_sazonal,
            x='Mês_Nome',
            y='Total_Internações',
            title='',
            labels={'Mês_Nome': 'Mês', 'Total_Internações': 'Média de Internações'},
            color='Total_Internações',
            color_continuous_scale='Blues'
        )
        fig_sazonal.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_sazonal, use_container_width=True)
    
    with col2:
        st.subheader("📦 Distribuição de Internações por Mês")
        
        df_box = df.copy()
        df_box['Mês'] = df_box['DATA_CMPT'].dt.strftime('%b')
        df_box['Mês'] = pd.Categorical(df_box['Mês'], categories=meses_ordem, ordered=True)
        
        # Agregar por mês/ano primeiro para evitar overplotting
        df_box_agg = df_box.groupby([df_box['DATA_CMPT'].dt.to_period('M'), 'Mês']).size().reset_index(name='Total')
        df_box_agg['Mês'] = df_box_agg['Mês'].astype(str)
        
        fig_box = px.box(
            df_box_agg,
            x='Mês',
            y='Total',
            title='',
            labels={'Mês': 'Mês', 'Total': 'Internações'}
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.markdown("---")
    
    # Tendência de mortalidade
    if 'Taxa_Mortalidade' in df_mensal.columns:
        st.subheader("💔 Evolução da Taxa de Mortalidade Hospitalar")
        
        fig_mort_temp = px.line(
            df_mensal,
            x='Data',
            y='Taxa_Mortalidade',
            title='',
            labels={'Data': 'Período', 'Taxa_Mortalidade': 'Taxa de Mortalidade (%)'},
            markers=True
        )
        fig_mort_temp.update_traces(line_color='#e74c3c', line_width=3)
        fig_mort_temp.update_layout(height=400)
        st.plotly_chart(fig_mort_temp, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela de estatísticas mensais
    st.subheader("📊 Estatísticas Mensais")
    
    df_mensal_display = df_mensal.copy()
    df_mensal_display['Data'] = df_mensal_display['Data'].dt.strftime('%m/%Y')
    
    if 'Custo_Total' in df_mensal_display.columns:
        df_mensal_display['Custo_Total'] = df_mensal_display['Custo_Total'].apply(lambda x: formatar_moeda(x))
    if 'Média_Permanência' in df_mensal_display.columns:
        df_mensal_display['Média_Permanência'] = df_mensal_display['Média_Permanência'].round(1)
    if 'Taxa_Mortalidade' in df_mensal_display.columns:
        df_mensal_display['Taxa_Mortalidade'] = df_mensal_display['Taxa_Mortalidade'].round(1)
    
    st.dataframe(df_mensal_display, height=400, use_container_width=True)
    
    # Download
    csv = df_mensal.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Dados Mensais",
        data=csv,
        file_name=f"dados_mensais_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ============================================================================
# PAINEL DE METODOLOGIA
# ============================================================================

def painel_metodologia():
    """Painel sobre metodologia e documentação"""
    
    st.title("📚 Sobre o Dashboard - Metodologia")
    st.markdown("---")
    
    st.markdown("""
    ## 📊 Fonte de Dados
    
    **Sistema de Informações Hospitalares do SUS (SIH/DATASUS)**
    
    O SIH/DATASUS é o sistema responsável pelo processamento das Autorizações de Internação Hospitalar (AIH) 
    no âmbito do Sistema Único de Saúde. Contém informações sobre internações hospitalares realizadas em 
    estabelecimentos públicos e privados conveniados ao SUS em todo o Brasil.
                
    As informações de gastos aqui apresentadas dizem respeito ao valor total dos procedimentos da SIGTAP.
    
    ---
    
    ## 🔧 Tratamento de Dados
    
    Os dados foram processados utilizando Python com as seguintes etapas:
    
    1. **Carregamento**: Leitura de arquivos CSV/Parquet/Excel
    2. **Limpeza**: Remoção de registros incompletos e valores inválidos
    3. **Transformação**: 
        - Conversão de tipos de dados
        - Criação de variáveis derivadas (faixas etárias, taxas)
        - Mapeamento de códigos (raça/cor, sexo)
    4. **Agregação**: Cálculo de indicadores e métricas
    
    ---
    
    ## 📈 Definição dos Indicadores
    
    ### Indicadores de Volume
    - **Total de Internações**: Contagem de AIHs no período
    - **Internações por Município**: Agregação por município de residência ou atendimento
    
    ### Indicadores de Tempo
    - **Média de Permanência**: `Soma(Dias de Permanência) / Total de AIHs`
    - **Taxa de Uso de UTI**: `(Soma de Dias em UTI / Soma Total de Dias) × 100`
    
    ### Indicadores de Morbimortalidade
    - **Taxa de Mortalidade Hospitalar**: `(Total de Óbitos / Total de Internações) × 100`
    - **Mortalidade por CID**: Taxa específica para cada diagnóstico
    
    ### Indicadores Financeiros
    - **Custo Médio por AIH**: `Soma(Valor Total) / Total de AIHs`
    - **Custo Total**: Soma dos valores de todas as AIHs
    
    ### Indicadores de Regulação
    - **Taxa de Evasão**: `(Internações fora do município de residência / Total) × 100`
    - **Autossuficiência**: `(Internações Realizadas / Residentes Internados) × 100`
    
    ---
    
    ## 🎯 Limitações Conhecidas
    
    - Dados referem-se apenas a internações no SUS (não incluem sistema suplementar)
    - Qualidade dos dados depende do preenchimento correto das AIHs
    - Campos como raça/cor podem apresentar alto percentual de "ignorado"
    - Atrasos na disponibilização dos dados pelo DATASUS
    
    ---
    
    ## 📚 Referências
    
    1. **DATASUS**: [https://datasus.saude.gov.br/](https://datasus.saude.gov.br/)
    2. **Manual SIH/SUS**: Ministério da Saúde
    3. **Saldanha, R. F. et al. (2019)**: Microdatasus: pacote para download e pré-processamento de microdados 
       do Departamento de Informática do SUS (DATASUS). *Cadernos de Saúde Pública*, 35(9).
    
    ---
    
    ## 💻 Tecnologias Utilizadas
    
    - **Streamlit**: Framework para construção do dashboard
    - **Plotly**: Biblioteca para visualizações interativas
    - **Pandas**: Manipulação e análise de dados
    - **Python**: Linguagem de programação
    
    ---
    
    ## 📧 Contato / Feedback

    Para dúvidas, sugestões ou relatos de problemas, entre em contato:

    - 📧 **Email**: [pedrowilliamrd@gmail.com](mailto:pedrowilliamrd@gmail.com)
    - 💻 **GitHub**: [github.com/pedrow28](https://github.com/pedrow28)
    - 💼 **LinkedIn**: [linkedin.com/in/pedrowilliamrd](https://www.linkedin.com/in/pedrowilliamrd/)
    
    ---
    
    ## 📝 Licença e Uso
    
    Este dashboard foi desenvolvido para fins educacionais e de análise em saúde pública.
    Os dados são de domínio público, disponibilizados pelo DATASUS.
    
    **Última atualização**: """ + datetime.now().strftime("%d/%m/%Y"))

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal do dashboard"""
    
    # Carregar dados
    df = carregar_dados()
    
    if df is None:
        st.error("Não foi possível carregar os dados. Verifique o caminho do arquivo.")
        st.stop()
    
    # Criar filtros na sidebar
    filtros = criar_filtros_sidebar(df)
    
    # Aplicar filtros
    df_filtrado = aplicar_filtros(df, filtros)
    
    # Aviso sobre os dados
    total_registros = formatar_numero(len(df_filtrado))
    filtro_ativo = " (filtradas)" if len(df_filtrado) < len(df) else ""

    st.markdown(f"""
    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3; margin-bottom: 20px;'>
        <h3 style='color: #1976D2; margin: 0;'>📊 Dashboard de Internações Hospitalares - SUS</h3>
        <p style='margin: 10px 0 0 0; color: #424242;'>
            <strong>Período:</strong> Internações realizadas em <strong>2025</strong> (Janeiro a Julho)<br>
            <strong>Localização:</strong> Estado de <strong>Minas Gerais</strong><br>
            <strong>Registros:</strong> {total_registros} internações{filtro_ativo}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Navegação por tabs
    tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏠 Início",
        "📊 Geral",
        "🔬 Epidemiológico",
        "🗺️ Regulação",
        "🏥 Estabelecimentos",
        "⚕️ Procedimentos",
        "👥 Equidade",
        "📚 Metodologia"
    ])

    with tab0:
        painel_inicial()

    with tab1:
        painel_geral(df_filtrado)

    with tab2:
        painel_epidemiologico(df_filtrado)

    with tab3:
        painel_regulacao(df_filtrado)

    with tab4:
        painel_estabelecimento(df_filtrado)

    with tab5:
        painel_procedimentos(df_filtrado)

    with tab6:
        painel_populacional(df_filtrado)

    with tab7:
        painel_metodologia()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Dashboard SIH/DATASUS<br>
        Desenvolvido com ❤️ em Streamlit<br>
        © 2024
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# EXECUTAR
# ============================================================================

if __name__ == "__main__":
    main()