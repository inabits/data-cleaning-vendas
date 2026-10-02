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