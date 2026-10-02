import pandas as pd
from utils import padronizar_digitos

# CARREGAR DADOS BRUTOS
df = pd.read_csv('dados_brutos/dados_brutos_vendas.csv', sep=';', encoding='latin-1')

# PADRONIZAÇÃO DO ID DO PEDIDO
df['id_pedido'] = df['id_pedido'].apply(padronizar_digitos)