# src/validate.py
"""
Módulo de validación de datos canónicos.
Se espera que los DataFrames tengan las columnas estandarizadas:
- date   : fecha de la transacción
- partner: cliente/partner asociado
- amount : importe numérico
"""

import pandas as pd
import logging

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def basic_checks(df: pd.DataFrame) -> list[str]:
    """
    Ejecuta validaciones mínimas sobre el DataFrame canónico.
    Retorna una lista de mensajes de error (vacía si todo está OK).
    """
    errors: list[str] = []

    # --- 1. Columnas obligatorias ---
    required_cols = ["date", "partner", "amount"]
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"❌ Falta la columna obligatoria: {col}")

    # Si faltan columnas críticas, no seguir
    if errors:
        logging.error("Errores de columnas: %s", errors)
        return errors

    # --- 2. Fecha válida ---
    invalid_dates = pd.to_datetime(df["date"], errors="coerce").isna().sum()
    if invalid_dates > 0:
        errors.append(f"❌ {invalid_dates} filas con fechas inválidas")

    # --- 3. Partner no nulo ---
    null_partners = df["partner"].isna().sum()
    if null_partners > 0:
        errors.append(f"❌ {null_partners} filas con partner vacío")

    # --- 4. Amount válido ---
    # numérico
    if not pd.api.types.is_numeric_dtype(df["amount"]):
        errors.append("❌ La columna 'amount' no es numérica")

    # sin negativos
    invalid_amounts = df[df["amount"] < 0].shape[0]
    if invalid_amounts > 0:
        errors.append(f"❌ {invalid_amounts} filas con importe negativo")

    # log
    if errors:
        logging.warning("Validaciones con errores: %s", errors)
    else:
        logging.info("Validaciones superadas correctamente ✅")

    return errors


def validation_summary(errors: list[str]) -> str:
    """
    Devuelve un string legible con el resultado de las validaciones.
    """
    if not errors:
        return "✅ Todas las validaciones fueron superadas."
    return "⚠️ Se encontraron los siguientes problemas:\n- " + "\n- ".join(errors)
