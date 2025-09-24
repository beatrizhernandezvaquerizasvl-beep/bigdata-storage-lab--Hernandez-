# streamlit_app.py
import io
import pandas as pd
import streamlit as st

from src.transform import normalize_columns, to_silver
from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks

st.set_page_config(page_title="Almacén Analítico", page_icon="📊", layout="wide")

st.title("📊 De CSVs heterogéneos a un almacén analítico confiable")
st.markdown(
    "Sube uno o varios archivos CSV, define el mapeo de columnas y genera un dataset "
    "unificado (bronze) y agregado (silver)."
)

# --- Sidebar para configuración ---
st.sidebar.header("⚙️ Configuración de columnas origen")
date_col = st.sidebar.text_input("Columna de fecha en origen", "fecha")
partner_col = st.sidebar.text_input("Columna de socio/cliente en origen", "cliente")
amount_col = st.sidebar.text_input("Columna de monto en origen", "importe")

uploaded_files = st.file_uploader(
    "Sube uno o varios archivos CSV",
    type=["csv"],
    accept_multiple_files=True,
)

bronze_frames = []

if uploaded_files:
    st.subheader("📥 Archivos cargados y normalizados")
    for file in uploaded_files:
        st.write(f"**Archivo:** {file.name}")
        try:
            df = pd.read_csv(file)
        except UnicodeDecodeError:
            # Fallback a latin-1 si falla utf-8
            file.seek(0)
            df = pd.read_csv(file, encoding="latin-1")

        # Normalizar columnas
        mapping = {
            date_col: "date",
            partner_col: "partner",
            amount_col: "amount",
        }
        df = normalize_columns(df, mapping)

        # Añadir linaje
        df = tag_lineage(df, file.name)
        bronze_frames.append(df)

    # Unir en bronze
    bronze = concat_bronze(bronze_frames)
    st.dataframe(bronze, use_container_width=True)

    # Validaciones
    st.subheader("✅ Validación de datos")
    errors = basic_checks(bronze)
    if errors:
        st.error("Se encontraron problemas en los datos:")
        for e in errors:
            st.markdown(f"- {e}")
    else:
        st.success("Datos validados correctamente. Puedes generar la capa Silver.")
        # Derivar silver
        silver = to_silver(bronze)

        st.subheader("🏆 KPIs básicos")
        st.metric("Total registros Bronze", len(bronze))
        st.metric("Total registros Silver", len(silver))
        st.metric("Suma total Amount (€)", f"{silver['amount'].sum():,.2f}")

        st.subheader("📈 Agregados Silver (Partner × Mes)")
        st.dataframe(silver, use_container_width=True)

        # Gráfico simple de evolución de montos por mes
        st.subheader("📊 Evolución mensual de Amount")
        monthly = silver.groupby("month", as_index=False)["amount"].sum()
        st.bar_chart(monthly, x="month", y="amount")

        # Botones de descarga
        st.subheader("⬇️ Descargas")
        bronze_csv = bronze.to_csv(index=False).encode("utf-8")
        silver_csv = silver.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar Bronze CSV", bronze_csv, "bronze.csv", "text/csv")
        st.download_button("Descargar Silver CSV", silver_csv, "silver.csv", "text/csv")
else:
    st.info("👆 Sube al menos un archivo CSV para comenzar.")
