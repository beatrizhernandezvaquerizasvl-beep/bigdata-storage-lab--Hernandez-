# src/transform.py
import pandas as pd

def normalize_columns(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """
    Renombra columnas según mapping (origen→canónico).
    Normaliza:
      - date → datetime ISO
      - amount → float (quita € y comas)
      - partner → string sin espacios extremos
    """
    df = df.rename(columns=mapping)

    # Fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Amount
    if "amount" in df.columns:
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Partner
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip()

    return df


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega amount por partner y mes.
    month = primer día del mes (timestamp).
    """
    bronze["month"] = bronze["date"].dt.to_period("M").dt.to_timestamp()
    silver = (
        bronze.groupby(["partner", "month"], as_index=False)
        .agg(total_amount=("amount", "sum"))
    )
    return silver


def to_gold(silver: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega amount por partner y año.
    Campos:
      - year
      - partner
      - total_amount
      - n_transactions
    """
    silver["year"] = silver["month"].dt.year
    gold = (
        silver.groupby(["partner", "year"], as_index=False)
        .agg(
            total_amount=("total_amount", "sum"),
            n_transactions=("total_amount", "count"),
        )
    )
    return gold

