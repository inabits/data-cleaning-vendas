import pandas as pd
import numpy as np

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

# PADRONIZAR VALOR UNITÁRIO
def padronizar_valor_unitario(serie_valor):
    
    s = serie_valor.astype(str).str.strip() # converter para string para manipulação de dados
    s = s.replace(r'^(-|N/D|n/d|ND|\s*|nan|None)$', pd.NA, regex=True) # substituir variações de nulo, texto inválido ou vazio por pd.NA
    s = s.str.replace(r'R\$\s?', '', case=False, regex=True) # remover prefixo monetário 'R$' se houver
    s = s.mask(s.str.contains(r'%|\(', regex=True).fillna(False), pd.NA) # remover valores com porcentagem ou parênteses (ex: '10%', '(10)') e substituir por pd.NA

    # normalizar separadores decimais e de milhar
    def limpar_formato(val):
        
        if pd.isna(val):
            return np.nan
        val_str = str(val)
        if '.' in val_str and ',' in val_str:
            val_str = val_str.replace('.', '').replace(',', '.')
        elif ',' in val_str:
            val_str = val_str.replace(',', '.')
        return val_str
    
    s_limpa = s.apply(limpar_formato)
    serie_num = pd.to_numeric(s_limpa, errors='coerce') # converter para numérico (lida com floats e converte falhas em NaN)
    serie_num = serie_num.where(serie_num > 0, pd.NA) # regra de negócio: valores <= 0 tornam-se pd.NA (vão para quarentena)
    
    return serie_num.astype(float)
    
# PADRONIZAR DESCONTO
def padronizar_desconto(serie_desconto):
    
    s = serie_desconto.astype(str).str.strip() # converter para string para manipulação de dados
    s = s.replace(r'^(-|N/A|n/a|ND|\s*|nan|None)$', '0', regex=True) # substituir variações de nulo, texto inválido ou vazio por pd.NA
    tem_porcentagem = s.str.contains('%', regex=False).fillna(False) # identificar se o valor contém o símbolo de porcentagem
    s_limpa = s.str.replace('%', '', regex=False).str.strip() # remover o símbolo de porcentagem e espaços em branco
    serie_num = pd.to_numeric(s_limpa, errors='coerce').fillna(0.0) # converter para numérico (lida com floats e converte falhas em NaN)
    
    # Função auxiliar para aplicar a escala correta
    def aplicar_escala(val, tem_pct):
        
        if val == 0.0:
            return 0.0
        if tem_pct:
            return val / 100.0
        else:
            # se vieram números altos sem '%', normalizamos para a escala 0 a 1 
            if val > 1.0:
                return val / 10000.0 if val > 100 else val / 100.0
            return val

    serie_final = [aplicar_escala(v, p) for v, p in zip(serie_num, tem_porcentagem)]
    
    return pd.Series(serie_final, index=serie_desconto.index, dtype=float)