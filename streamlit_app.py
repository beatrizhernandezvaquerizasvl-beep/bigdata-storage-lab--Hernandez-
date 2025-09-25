from src.transform import normalize_columns, to_silver, to_gold
from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks, veracity_score

# ... después de crear silver
if all_errors == []:  # si no hubo errores críticos
    st.subheader("📊 Tabla Silver (partner × mes)")
    st.dataframe(silver)

    # KPIs simples
    st.metric("Total amount (€)", f"{silver['total_amount'].sum():,.2f}")
    st.metric("Partners únicos", silver["partner"].nunique())

    # Chart
    st.bar_chart(silver, x="month", y="total_amount")

    # ➡️ Nueva capa GOLD
    gold = to_gold(silver)
    st.subheader("🏆 Tabla Gold (partner × año)")
    st.dataframe(gold)

    # Descargas
    st.download_button(
        "⬇️ Descargar bronze.csv",
        bronze.to_csv(index=False).encode("utf-8"),
        file_name="bronze.csv",
        mime="text/csv",
    )
    st.download_button(
        "⬇️ Descargar silver.csv",
        silver.to_csv(index=False).encode("utf-8"),
        file_name="silver.csv",
        mime="text/csv",
    )
    st.download_button(
        "⬇️ Descargar gold.csv",
        gold.to_csv(index=False).encode("utf-8"),
        file_name="gold.csv",
        mime="text/csv",
    )
