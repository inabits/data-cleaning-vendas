import pandas as pd

# PADRONIZAR ID DO PEDIDO
def padronizar_digitos(id_str):
    
    id_str = str(id_str).strip() # remover espaços em branco
    if not id_str.startswith('PED-'): # adicionar prefixo 'PED-' se não estiver presente
        id_str = 'PED-' + id_str
        
    if '-' in id_str:
        prefixo, numero = id_str.split('-', 1)
        numero_limpo = ''.join(filter(str.isdigit, numero)).zfill(5) # preencher com zeros à esquerda para garantir 5 dígitos
        return f"{prefixo}-{numero_limpo}"
    
    return id_str

# PADRONIZAR DATA
def padronizar_data(serie_data):
    
    serie_limpa = serie_data.replace(r'^(nd|n/a|\s*)$', pd.NA, regex=True) # substituir valores inválidos por NaN
    serie_dt = pd.to_datetime(serie_limpa, format='mixed', errors='coerce', dayfirst=True) # converter para datetime, tratando erros
    
    return serie_dt.dt.strftime('%Y-%m-%d')

# PADRONIZAR TEXTO
def padronizar_texto(serie_texto):
    
    serie_limpa = serie_texto.replace(r'^\s*$', pd.NA, regex=True) # substituir valores inválidos por NaN
    
    return (
        serie_limpa.str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.upper()
    )
    
# PADRONIZAR QUANTIDADE
def padronizar_quantidade(serie_quantidade):
    
    serie_str = serie_quantidade.astype(str).str.strip() # converter para string temporariamente para limpar textos e espaços
    serie_str = serie_str.replace(r'^(N/A|n/a|nd|ND|\s*|nan|None)$', pd.NA, regex=True) # substituir variações de nulo, texto inválido ou vazio por pd.NA
    serie_str = serie_str.str.replace(r'\s*un$', '', case=False, regex=True) # remover sufixos de unidades (ex: ' un', 'UN') se houver
    serie_num = pd.to_numeric(serie_str, errors='coerce') # converter para numérico (lida com floats como 166.0 e converte falhas em NaN)
    serie_num = serie_num.where(serie_num > 0, pd.NA) # regra de negócio: quantidades <= 0 (zeros e o erro -1) tornam-se pd.NA (vão para quarentena)

    return serie_num.astype('Int64')