# 🛒 Pipeline de Limpeza, Governança e Auditoria de Dados de Vendas

Pipeline de Engenharia de Dados corporativa e de nível de portfólio, desenvolvida para processar, validar e governar uma base de 10.000 registros de vendas com alto nível de ruído, inconsistências e dados corrompidos.

---

## 🏗️ Arquitetura do Pipeline (Dual-Output)

O projeto adota uma estratégia rigorosa de **Dual-Output (Dupla Saída)** para garantir a integridade dos dados analíticos sem descartar cegamente registros problemáticos:
1. **Dataset Limpo (`dados_tratados_vendas.csv`):** Contém exclusivamente os registros válidos, padronizados e prontos para consumo por ferramentas de BI e planilhas.
2. **Quarentena (`quarentena.csv`):** Isola todos os registros que falharam em regras críticas de negócio (como campos obrigatórios nulos ou inválidos), acompanhados de logs detalhados de auditoria (`motivo_quarentena`).

---

## ⚙️ Módulos e Regras de Negócio (`utils.py`)

O pipeline é modularizado através do arquivo `utils.py`, aplicando funções vetorizadas e tratamentos específicos para cada atributo:

* **Padronização de IDs e Datas:** 
  * `padronizar_digitos`: Garante a integridade e o preenchimento de dígitos para IDs de pedidos.
  * `padronizar_data`: Uniformiza o formato temporal das vendas.
* **Padronização de Textos e Dicionários (`unicodedata` & Mapeamentos):** 
  * Normalização universal de acentuação e remoção de caracteres corrompidos de *encoding* legado (ex: unificação de variações de `LOJA FÍSICA` e `CONCLUÍDO`).
  * Conversão para maiúsculas e limpeza de espaços em branco excessivos para colunas como `produto`, `regiao`, `vendedor`, `canal_venda` e `status`.
* **Validação de Quantidades (`padronizar_quantidade`):**
  * Tratamento de nulos e termos corrompidos, convertendo a coluna para o tipo seguro `Int64` do Pandas.
  * Desvio automático de quantidades inválidas, menores ou iguais a zero para a quarentena.
* **Limpeza de Valores Unitários (`padronizar_valor_unitario`):**
  * Remoção de símbolos monetários e tratamento de separadores decimais/milhar mistos.
  * Conversão segura para `float`, direcionando preços nulos, negativos ou zerados para auditoria.
* **Padronização de Descontos (`padronizar_desconto`):**
  * Conversão uniforme de taxas percentuais para o intervalo decimal padrão ($0.0$ a $1.0$).

---

## 📂 Estrutura do Repositório

```text
data-cleaning-vendas/
│
├── dados_brutos/
│   └── dados_brutos_vendas.csv       # Base original com ruídos
│
├── dados_tratados/
│   ├── dados_tratados_vendas.csv     # Output limpo para Analytics
│   ├── dados_tratados_vendas_50.csv  # Output limpo para Analytics (50 primeiros dados)
│   ├── quarentena.csv                # Registros rejeitados para auditoria
│   └── quarentena_50.csv             # Registros rejeitados para auditoria (50 primeiros dados)
│
├── scripts/
│   ├── limpeza_dados.py              # Script principal orquestrador
│   └── utils.py                      # Funções de limpeza e regras de negócio
│
├── .gitignore
└── README.md                         # Documentação técnica do projeto
```

--- 

## 🚀 Como executar o projeto

1. **Pré-requisitos:** Certifique-se de ter o Python instalado junto com a biblioteca Pandas:
```bash
pip install pandas numpy
```
2. **Executando o Pipeline:** Navegue até a raiz do projeto e execute o script orquestrador:
```bash
python scripts/limpeza_dados.py
```
3. **Verificando os Resultados:** Os arquivos processados serão salvos automaticamente na pasta `dados_tratados/`, codificados em `utf-8-sig` para garantir a leitura correta de acentos e separadores em ferramentas externas.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Python 3.x:** Linguagem principal para desenvolvimento da lógica de engenharia de dados.
* **Pandas:** Biblioteca central para manipulação, transformação, vetorização e estruturação dos DataFrames.
* **Expressões Regulares (Regex) & Unicodedata:** Utilizados para saneamento avançado de strings, remoção de caracteres corrompidos e padronização de codificação.
* **Arquitetura Dual-Output:** Padrão de projeto focado em governança para separação de dados válidos e corrompidos.
* **Git & GitHub:** Versionamento de código e documentação técnica do repositório.

---

## 🔍 Problemas Identificados na Base Bruta

O dataset original (`dados_brutos_vendas.csv`) simulava um ambiente de produção real e desestruturado, apresentando os seguintes desafios que exigiram tratamento programático:

* **Corrupção de Caracteres (*Encoding*):** Presença de artefatos legados e erros de codificação em textos acentuados (ex: `LOJA FSICA`, `CONCLUDO`, `FSICA`), resolvidos via normalização Unicode e dicionários de mapeamento.
* **Inconsistências de Tipagem:** Colunas numéricas contendo misturas de strings, espaços em branco, símbolos monetários, hífens ou valores nulos disfarçados de texto.
* **Registros Críticos Inválidos (Anomalias):** Linhas contendo datas nulas, quantidades ou preços unitários zerados/negativos que comprometeriam diretamente qualquer análise financeira ou de BI se não fossem isolados.
* **Variações de Formato:** Diferentes padrões de preenchimento em campos categóricos (`canal_venda`, `status`, `regiao`), unificados para garantir consistência em agregações futuras.

---

## 💡 Sobre o Projeto e Aprendizados

Este projeto foi concebido como parte da minha jornada de desenvolvimento técnico, focado em consolidar boas práticas de **Engenharia de Dados e Governança**. 

* **Resiliência de Dados:** Aprendi a importância de nunca descartar dados brutos cegamente. O uso da **Quarentena** garante rastreabilidade e permite que a equipe de negócios audite e corrija falhas na origem.
* **Modularização e Limpeza de Código:** A separação entre as regras de negócio (`utils.py`) e o script orquestrador (`limpeza_dados.py`) tornou o pipeline limpo, testável e escalável para bases maiores.
* **Visão de Negócio:** Compreender que o tratamento de dados vai muito além de remover linhas nulas — envolve padronizar a experiência analítica e garantir a confiabilidade para ferramentas de visualização (como Power BI ou Google Planilhas).

---

## 👩‍💻 Autora

Bianca Inazumi
