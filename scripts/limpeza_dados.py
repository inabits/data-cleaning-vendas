import pandas as pd
from utils import padronizar_digitos, padronizar_data, padronizar_texto, padronizar_quantidade, padronizar_valor_unitario, padronizar_desconto

# CARREGAR DADOS BRUTOS
df = pd.read_csv('dados_brutos/dados_brutos_vendas.csv', sep=';', encoding='utf-8', dtype=str)

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

# PADRONIZAR TIPO DE CANAL DE VENDAS
df['canal_venda'] = padronizar_texto(df['canal_venda'])
mapa_canal_venda = {
    'ONLINE': 'ONLINE',
    'LOJA FISICA': 'LOJA FÍSICA',
    'LOJA F�SICA': 'LOJA FÍSICA',
    'LOJA FÍSICA': 'LOJA FÍSICA',
    'LOJA FSICA': 'LOJA FÍSICA',      
    'TELEVENDAS': 'TELEVENDAS',
    'REVENDEDOR': 'REVENDEDOR'
}
df['canal_venda'] = df['canal_venda'].map(mapa_canal_venda).fillna(df['canal_venda'])

# PADRONIZAR STATUS DO PEDIDO
df['status'] = padronizar_texto(df['status'])
mapa_status = {
    'CONCLUIDO': 'CONCLUÍDO',
    'CONCLU�DO': 'CONCLUÍDO',
    'CONCLUÍDO': 'CONCLUÍDO',
    'CANCELADO': 'CANCELADO',
    'PENDENTE': 'PENDENTE',
    'EM ANÁLISE': 'EM ANÁLISE',
    'EM AN�LISE': 'EM ANÁLISE',
    'EM ANALISE': 'EM ANÁLISE'
}
df['status'] = df['status'].map(mapa_status).fillna(df['status'])

### 

# definindo as regras críticas de falha (campos obrigatórios que não podem ser nulos)
falha_data = df['data_venda'].isna() | (df['data_venda'].astype(str).str.strip() == '')
falha_quantidade = df['quantidade'].isna()
falha_preco = df['valor_unitario'].isna()

# máscara de quarentena (se falhar em qualquer regra crítica)
mascara_quarentena = falha_data | falha_quantidade | falha_preco

# criando os DataFrames separados
df_quarentena = df[mascara_quarentena].copy()
df_tratado = df[~mascara_quarentena].copy()

# adicionando a coluna descritiva com o motivo da rejeição na Quarentena
def identificar_motivos(row):
    motivos = []
    if pd.isna(row['data_venda']) or str(row['data_venda']).strip() == '':
        motivos.append('Data ausente ou inválida')
    if pd.isna(row['quantidade']):
        motivos.append('Quantidade ausente ou <= 0')
    if pd.isna(row['valor_unitario']):
        motivos.append('Valor unitário ausente ou inválido')
    return ' | '.join(motivos)

df_quarentena['motivo_quarentena'] = df_quarentena.apply(identificar_motivos, axis=1)

# salvando os arquivos finais 
df_tratado.to_csv('dados_tratados/dados_tratados_vendas.csv', index=False, encoding='utf-8-sig')
df_quarentena.to_csv('dados_tratados/quarentena.csv', index=False, encoding='utf-8-sig')
df_tratado.head(50).to_csv('dados_tratados/dados_tratados_vendas_50.csv', index=False, encoding='utf-8-sig')
df_quarentena.head(50).to_csv('dados_tratados/quarentena_50.csv', index=False, encoding='utf-8-sig')

print("Pipeline executado com sucesso!")
print(f"-> Registros validos (Analytics): {len(df_tratado)}")
print(f"-> Registros em Quarentena (Auditoria): {len(df_quarentena)}")