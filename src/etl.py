import pandas as pd
import pandera as pa
from modules import FinancialBase, FinancialBaseOutput

from sqlalchemy import create_engine


def extract_data(directory: str = "data/dados_financeiros.csv") -> pd.DataFrame:
    """Extrair dados de um arquivo CSV."""
    df = pd.read_csv(directory)

    try:
        df = FinancialBase.validate(df, lazy=True)
        return df
    except pa.errors.SchemaError as e:
        print(f"Erro de validação: {e}")


@pa.check_output(FinancialBaseOutput, lazy=True)
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformar os dados."""
    transformed_df = df.copy()

    transformed_df['valor_do_imposto'] = transformed_df['receita_operacional'] * \
        transformed_df['percentual_de_imposto']

    transformed_df['custo_total'] = transformed_df['valor_do_imposto'] + \
        transformed_df['custos_operacionais']

    transformed_df['receita_liquida'] = transformed_df['receita_operacional'] - \
        transformed_df['custo_total']

    transformed_df['margem_operacional'] = transformed_df['receita_liquida'] / \
        transformed_df['receita_operacional']

    transformed_df['changed_at'] = pd.to_datetime('now')

    return transformed_df


def load_data(df: pd.DataFrame) -> None:
    """Carregar os dados."""
    # Criando o banco de dados SQLite
    engine = create_engine('sqlite:///data/financial_data.db')
    df.to_sql('metricas_financeiras', engine, if_exists="replace", index=False)


df = extract_data()
df = transform_data(df)
load_data(df)
