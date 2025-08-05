import streamlit as st
import pandas as pd
from db_connection import ejecutar_sql

def explorar_tabla():
    st.markdown("## 🧪 Explorador de Tabla SQL – Análisis de Campos")

    # Campo editable para que el usuario escriba el nombre de la tabla
    nombre_tabla = st.text_input(
        "🔢 Nombre de la tabla a consultar:",
        "[dbo].[Prestaciones_Temporal]"
    )

    cantidad = st.slider("📄 Número de registros a mostrar", min_value=1, max_value=1000, value=10)

    if st.button("📥 Consultar tabla"):
        query = f"SELECT TOP {cantidad} * FROM {nombre_tabla}"
        st.code(query)

        try:
            df = ejecutar_sql(query)
            if df.empty:
                st.warning("⚠ La consulta no retornó datos.")
            else:
                st.success("✅ Datos consultados exitosamente desde la base de datos.")
                st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Error al consultar la base de datos: {e}")
