import pandas as pd
from utils import padronizar_digitos, padronizar_data, padronizar_texto, padronizar_quantidade, padronizar_valor_unitario, padronizar_desconto

# CARREGAR DADOS BRUTOS
df = pd.read_csv('dados_brutos/dados_brutos_vendas.csv', sep=';', encoding='latin-1')

# PADRONIZAÇÃO DO ID DO PEDIDO
df['id_pedido'] = df['id_pedido'].apply(padronizar_digitos)

# PADRONIZAÇÃO DE DATA
df['data_venda'] = padronizar_data(df['data_venda'])

# PADRONIZAÇÃO DO NOME DOS PRODUTOS
df['produto'] = padronizar_texto(df['produto'])

# PADRONIZAÇÃO DE QUANTIDADE
df['quantidade'] = padronizar_quantidade(df['quantidade'])  

# PADRONIZAÇÃO DE VALOR UNITÁRIO
df['valor_unitario'] = padronizar_valor_unitario(df['valor_unitario'])

# PADRONIZAÇÃO DE DESCONTO
df['desconto'] = padronizar_desconto(df['desconto'])

# PADRONIZAÇÃO DE NOME DE REGIÃO
df['regiao'] = padronizar_texto(df['regiao'])

# PADRONIZAR NOME DO VENDEDOR
df['vendedor'] = padronizar_texto(df['vendedor'])   

# SALVAR DADOS LIMPOS
df.to_csv('dados_tratados/dados_tratados_vendas.csv', index=False)