from typing import Optional
import pandera as pa
from pandera.typing import Series


class FinancialBase(pa.DataFrameModel):
    """Classe base para os dados financeiros."""
    setor_da_empresa: Series[str]
    receita_operacional: Series[float] = pa.Field(ge=0)
    data: Series[pa.Timestamp]
    percentual_de_imposto: Series[float] = pa.Field(
        in_range={"min_value": 0, "max_value": 1})
    custos_operacionais: Series[float] = pa.Field(ge=0)

    class Config:
        coerce = True
        strict = True

    @pa.check("setor_da_empresa",
              name="Checagem de código dos setores",
              error="Código de setor inválido")
    def check_setor_da_empresa(cls, codigo: Series[str]) -> Series[bool]:
        return codigo.str[:4].isin(["REP_", "MNT_", "VND_"])


class FinancialBaseOutput(FinancialBase):
    valor_do_imposto: Series[float] = pa.Field(ge=0)
    custo_total: Series[float] = pa.Field(ge=0)
    receita_liquida: Series[float] = pa.Field(ge=0)
    margem_operacional: Series[float] = pa.Field(ge=0)
    changed_at: Optional[pa.Timestamp]

    @pa.dataframe_check
    def check_margem_operacional(cls, df: pa.DataFrame) -> pa.Series[bool]:
        return df['margem_operacional'] == (df['receita_liquida'] / df['receita_operacional'])
