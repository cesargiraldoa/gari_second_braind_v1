import streamlit as st
import pandas as pd
from db_connection import ejecutar_sql

def mostrar_eda():
    st.markdown("## 📊 Análisis Descriptivo – Prestaciones Temporales")

    # Consulta base limitada para análisis (ajustable)
    query = "SELECT TOP 10000 * FROM [dbo].[Prestaciones_Temporal]"

    try:
        df = ejecutar_sql(query)
        st.success(f"✅ Datos cargados correctamente. {df.shape[0]} filas × {df.shape[1]} columnas.")
    except Exception as e:
        st.error(f"❌ Error al consultar la tabla: {e}")
        return

    st.markdown("### 📌 Tipos de datos")
    st.dataframe(df.dtypes.rename("Tipo").to_frame())

    st.markdown("### 🚨 Valores nulos por columna")
    st.dataframe(df.isnull().sum().rename("Nulos").to_frame())

    st.markdown("### 📈 Estadísticas descriptivas (numéricas)")
    st.dataframe(df.describe().transpose())

    st.markdown("### 🏷️ Top categorías más frecuentes")
    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols:
        st.markdown(f"**🔹 {col} (Top 10)**")
        st.dataframe(df[col].value_counts().head(10).rename("Frecuencia").to_frame())

    st.markdown("### 🔍 Vista previa de los datos")
    st.dataframe(df.head(10))
