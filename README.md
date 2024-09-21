# ETL com Contrato de Dados

## Descrição do Projeto

Este projeto é um simples ETL que extrai, transforma e carrega dados financeiros a partir de um arquivo CSV. Utiliza as bibliotecas pandas para manipulação de dados, pandera para validação de esquemas e SQLAlchemy para interagir com um banco de dados SQLite.

## Estrutura do Código

O código é dividido em três funções principais:

1. `extract_data(directory: str)`: Extrai dados de um arquivo CSV e valida o DataFrame utilizando o esquema definido em FinancialBase.
2. `transform_data(df: pd.DataFrame)`: Realiza transformações nos dados, calculando métricas financeiras como valor do imposto, custo total, receita líquida e margem operacional.
3. `load_data(df: pd.DataFrame)`: Carrega os dados transformados em um banco de dados SQLite.
