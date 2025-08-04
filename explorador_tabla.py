import streamlit as st
import pandas as pd
from db_connection import ejecutar_sql

def mostrar_explorador_tabla():
    st.markdown("## 🧪 Explorador de Tabla SQL – Análisis de Campos")

    tabla = st.text_input("🧾 Nombre de la tabla (incluye esquema si aplica):", value="dbo.Prestaciones_Temporal")

    if st.button("🔍 Ver primeros 1000 registros"):
        try:
            query = f"SELECT TOP 1000 * FROM {tabla}"
            df = ejecutar_sql(query)
            if df.empty:
                st.warning("⚠ La tabla está vacía o no se encontraron registros.")
            else:
                st.success(f"✅ Mostrando 1000 registros de la tabla '{tabla}'")
                st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Error al consultar la base de datos: {e}")

    if st.button("🧠 Ver nombres de columnas y tipos de datos"):
        try:
            if "." in tabla:
                esquema, nombre_tabla = tabla.split(".")
            else:
                esquema = "dbo"
                nombre_tabla = tabla

            query = f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{nombre_tabla}' AND TABLE_SCHEMA = '{esquema}'
            """
            df_info = ejecutar_sql(query)
            st.success("✅ Estructura de la tabla obtenida:")
            st.dataframe(df_info)
        except Exception as e:
            st.error(f"❌ Error al obtener metadatos: {e}")
