import pandas as pd
from utils import padronizar_digitos, padronizar_data

# CARREGAR DADOS BRUTOS
df = pd.read_csv('dados_brutos/dados_brutos_vendas.csv', sep=';', encoding='latin-1')

# PADRONIZAÇÃO DO ID DO PEDIDO
df['id_pedido'] = df['id_pedido'].apply(padronizar_digitos)

# PADRONIZAÇÃO DE DATA
df['data_venda'] = padronizar_data(df['data_venda'])

# SALVAR DADOS LIMPOS
df.to_csv('dados_tratados/dados_tratados_vendas.csv', index=False)