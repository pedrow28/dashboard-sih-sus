"""
Script para converter dados.xlsx para formato Parquet
O formato Parquet é até 10x mais rápido para carregar que Excel

Uso:
    python converter_para_parquet.py
"""

import pandas as pd
import sys
from pathlib import Path

def converter_excel_para_parquet(arquivo_entrada, arquivo_saida=None):
    """
    Converte arquivo Excel para Parquet

    Args:
        arquivo_entrada: Caminho do arquivo .xlsx
        arquivo_saida: Caminho do arquivo .parquet (opcional, usa mesmo nome se não especificado)
    """

    # Definir arquivo de saída
    if arquivo_saida is None:
        arquivo_saida = Path(arquivo_entrada).stem + '.parquet'

    print(f"[*] Convertendo {arquivo_entrada} para Parquet...")
    print(f"[*] Arquivo de saída: {arquivo_saida}")
    print()

    try:
        # Carregar Excel
        print("[*] Carregando arquivo Excel... (pode demorar alguns minutos)")
        df = pd.read_excel(arquivo_entrada)

        total_linhas = len(df)
        total_colunas = len(df.columns)
        tamanho_mb = Path(arquivo_entrada).stat().st_size / (1024 * 1024)

        print(f"[OK] Excel carregado com sucesso!")
        print(f"     {total_linhas:,} linhas x {total_colunas} colunas")
        print(f"     Tamanho original: {tamanho_mb:.1f} MB")
        print()

        # Otimizar tipos de dados para reduzir tamanho
        print("[*] Otimizando tipos de dados...")

        # Converter colunas categóricas
        colunas_categoricas = []
        colunas_data = []

        # Identificar colunas de data
        for col in df.columns:
            if 'data' in col.lower() or 'dt_' in col.lower():
                colunas_data.append(col)

        for col in df.columns:
            # Pular colunas de data
            if col in colunas_data:
                continue

            # Se a coluna tem menos de 50% de valores únicos, pode ser categórica
            if df[col].dtype == 'object':
                razao_unica = df[col].nunique() / len(df)
                if razao_unica < 0.5:
                    try:
                        df[col] = df[col].astype('category')
                        colunas_categoricas.append(col)
                    except:
                        # Se falhar, manter como object
                        pass

        print(f"     {len(colunas_categoricas)} colunas convertidas para categoricas")

        # Converter colunas de data para datetime
        print("[*] Convertendo colunas de data...")
        for col in colunas_data:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass

        # Salvar como Parquet
        print("[*] Salvando arquivo Parquet...")
        df.to_parquet(
            arquivo_saida,
            engine='pyarrow',
            compression='snappy',
            index=False
        )

        tamanho_parquet_mb = Path(arquivo_saida).stat().st_size / (1024 * 1024)
        reducao = (1 - tamanho_parquet_mb / tamanho_mb) * 100

        print()
        print("[OK] Conversao concluida com sucesso!")
        print(f"     Tamanho Parquet: {tamanho_parquet_mb:.1f} MB")
        print(f"     Reducao de tamanho: {reducao:.1f}%")
        print(f"     Velocidade de carregamento esperada: 5-10x mais rapida")
        print()
        print(f"[!] Para usar no dashboard, altere CAMINHO_ARQUIVO para: '{arquivo_saida}'")

    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{arquivo_entrada}' nao encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO] Erro durante conversao: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Arquivo padrão
    ARQUIVO_ENTRADA = "dados.xlsx"

    # Permitir argumento via linha de comando
    if len(sys.argv) > 1:
        ARQUIVO_ENTRADA = sys.argv[1]

    # Verificar se o arquivo existe
    if not Path(ARQUIVO_ENTRADA).exists():
        print(f"[ERRO] Arquivo '{ARQUIVO_ENTRADA}' nao encontrado no diretorio atual")
        print()
        print("[!] Uso:")
        print(f"    python converter_para_parquet.py [arquivo.xlsx]")
        print()
        print("[!] Exemplo:")
        print(f"    python converter_para_parquet.py dados.xlsx")
        sys.exit(1)

    # Converter
    converter_excel_para_parquet(ARQUIVO_ENTRADA)
