import pandas as pd
from typing import Dict

def normalize_columns(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Renombra columnas, formatea fechas a ISO, limpia partner y normaliza amount.
    mapping: dict con {columna_origen: columna_canónica}
    """
    # Renombrar según mapping
    df = df.rename(columns=mapping)

    # Asegurar que columnas canónicas existen si estaban en mapping
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "partner" in df.columns:
        df["partner"] = df["partner"].astype(str).str.strip()
    if "amount" in df.columns:
        # Remover símbolo €, espacios y cambiar comas por puntos
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("€", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
        )
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df


def to_silver(bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega montos por partner y mes.
    Crea columna 'month' como primer día de cada mes (timestamp).
    """
    df = bronze.copy()
    if "date" not in df.columns or "partner" not in df.columns or "amount" not in df.columns:
        raise ValueError("Bronze debe contener columnas: date, partner, amount")

    # Crear columna de mes
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    silver = df.groupby(["partner", "month"], as_index=False)["amount"].sum()

    return silver
