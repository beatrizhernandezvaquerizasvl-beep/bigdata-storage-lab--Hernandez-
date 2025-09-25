# src/validate.py
import pandas as pd

def basic_checks(df: pd.DataFrame) -> list[str]:
    """
    Ejecuta validaciones sobre el dataframe canónico.
    Retorna una lista de mensajes de error (vacía si todo está OK).
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
            return errors  # no seguimos si faltan columnas

    # Validación de fechas
    parsed_dates = pd.to_datetime(df["date"], errors="coerce")
    invalid_dates = parsed_dates.isna().sum()
    if invalid_dates > 0:
        errors.append(f"{invalid_dates} filas con fechas inválidas")

    # Rango de fechas permitido
    mask_out_of_range = (parsed_dates < "2010-01-01") | (parsed_dates > "2030-12-31")
    out_of_range_count = mask_out_of_range.sum()
    if out_of_range_count > 0:
        errors.append(f"{out_of_range_count} filas fuera del rango de fechas permitido (2010–2030)")

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
            errors.append(f"{duplicates} filas duplicadas detectadas por clave natural (date + partner)")

    return errors

