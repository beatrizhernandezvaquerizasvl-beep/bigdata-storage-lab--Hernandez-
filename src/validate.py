# src/validate.py
import pandas as pd

def basic_checks(df: pd.DataFrame) -> list[str]:
    """
    Ejecuta validaciones sobre el dataframe canónico.
    Retorna lista de errores (vacía si todo está OK).
    Incluye:
      - Columnas obligatorias
      - Fechas válidas
      - Rango de fechas (2010–2030)
      - Amount >= 0
      - Duplicados por clave natural (date + partner)
    """
    errors: list[str] = []

    # Columnas obligatorias
    required_cols = ["date", "partner", "amount"]
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Falta la columna obligatoria: {col}")
            return errors

    # Validación de fechas
    parsed_dates = pd.to_datetime(df["date"], errors="coerce")
    invalid_dates = parsed_dates.isna().sum()
    if invalid_dates > 0:
        errors.append(f"{invalid_dates} filas con fechas inválidas")

    # Rango de fechas permitido
    mask_out_of_range = (parsed_dates < "2010-01-01") | (parsed_dates > "2030-12-31")
    out_of_range_count = mask_out_of_range.sum()
    if out_of_range_count > 0:
        errors.append(f"{out_of_range_count} filas fuera del rango permitido (2010–2030)")

    # Validación de amount
    if not pd.api.types.is_numeric_dtype(df["amount"]):
        errors.append("La columna amount no es numérica")
    else:
        negative_amounts = (df["amount"] < 0).sum()
        if negative_amounts > 0:
            errors.append(f"{negative_amounts} filas con importe negativo")

    # Duplicados por clave natural (date + partner)
    if {"date", "partner"}.issubset(df.columns):
        duplicates = df.duplicated(subset=["date", "partner"]).sum()
        if duplicates > 0:
            errors.append(f"{duplicates} filas duplicadas por clave natural (date+partner)")

    return errors


def veracity_score(df: pd.DataFrame) -> float:
    """
    Calcula % de registros válidos = registros sin errores / total.
    """
    total = len(df)
    if total == 0:
        return 0.0

    # Validaciones fila a fila
    parsed_dates = pd.to_datetime(df["date"], errors="coerce")
    valid_dates = parsed_dates.notna()
    in_range = (parsed_dates >= "2010-01-01") & (parsed_dates <= "2030-12-31")

    numeric_amount = pd.to_numeric(df["amount"], errors="coerce")
    valid_amount = numeric_amount.notna() & (numeric_amount >= 0)

    partner_ok = df["partner"].notna() & (df["partner"].astype(str).str.strip() != "")

    valid_rows = valid_dates & in_range & valid_amount & partner_ok
    score = valid_rows.sum() / total * 100
    return round(score, 2)

