# Dicionário de Dados - Projeto Venda de Eletrônicos 🔌

Este documento descreve a estrutura técnica e as regras de negócio de cada campo presente na base de dados de transações fictícias de vendas de eletrônicos.

## Tabela: `dados_brutos_venda.csv`

| Coluna | Tipo de Dado | Obrigatório? (Sim/Não) | Regra de Negócio / Padrão Esperado |
| :--- | :--- | :--- | :--- |
| **id_pedido** | Inteiro (INT) | Sim | Identificador único e sequencial de cada pedido realizado. Deve seguir o padrão `PED-99999`. |
| **data_venda** | Data (YYYY-MM-DD) | Sim | Data em que a venda foi efetuada. O formato oficial padrão aceito é o internacional `AAAA-MM-DD`. Valores nulos, em branco ou ruídos textuais (`nd`, `N/A`) presentes na origem são filtrados e isolados em camada de quarentena/auditoria, garantindo integridade na base analítica tratada. |
| **produto** | Texto (String) | Sim | Nome comercial do produto eletrônico da venda. |
| **quantidade** | Inteiro (INT) | Sim | Volume de itens adquirido na transação. |
| **valor_unitario** | Numérico (Float) | Sim | Preço de uma única unidade do produto. Deve conter apenas números e ponto decimal (Ex: `35.00`), sem o símbolo de moeda. |
| **desconto** | Numérico (Float) | Não | Percentual ou valor absoluto de desconto aplicado. |
| **regiao** | Texto (String) | Sim | Região geográfica do Brasil onde a venda ocorreu. Valores permitidos: `Norte`, `Nordeste`, `Centro-Oeste`, `Sudeste` e `Sul`.|
| **vendedor** | Texto (String) | Sim | Nome do colaborador responsável pela venda. |
| **canal_venda** | Texto (String) | Sim | Canal utilizado para a transação. Valores permitidos: `Online`, `Loja física`, `Televendas` e `Revendedor`.|
| **status**| Texto (String) | Sim | Situação cadastral do pedido. Valores permitidos: `Concluído`, `Pendente`, `Em análise` ou `Cancelado`. |