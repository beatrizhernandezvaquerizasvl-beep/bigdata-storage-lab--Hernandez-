# src/ingest.py
import pandas as pd
from datetime import datetime, timezone
from typing import List

def tag_lineage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    """
    Añade metadatos de linaje: nombre de archivo fuente y timestamp UTC de ingesta.
    """
    tagged = df.copy()
    tagged["source_file"] = source_name
    tagged["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return tagged

def concat_bronze(frames: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatena varios DataFrames al esquema estándar de bronze:
    [date, partner, amount, source_file, ingested_at]
    """
    if not frames:
        return pd.DataFrame(columns=["date", "partner", "amount", "source_file", "ingested_at"])
    combined = pd.concat(frames, ignore_index=True)
    # Reordenar columnas si existen
    cols = [c for c in ["date", "partner", "amount", "source_file", "ingested_at"] if c in combined.columns]
    combined = combined[cols]
    return combined
