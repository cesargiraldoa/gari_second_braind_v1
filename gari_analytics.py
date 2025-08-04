import streamlit as st
import pandas as pd
import pymssql


def ejecutar_sql(query: str) -> pd.DataFrame:
    conn = pymssql.connect(
        server='sql8020.site4now.net',
        user='db_a91131_test_admin',
        password='dEVOPS2022',
        database='db_a91131_test'
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def main():
    st.markdown("## 🧪 Explorador de Tabla SQL – Análisis de Campos")

    nombre_tabla = "[Prestaciones_Temporal]"
    query = f"SELECT TOP 1000 * FROM {nombre_tabla}"

    try:
        df = ejecutar_sql(query)

        if df.empty:
            st.warning("⚠ No se encontraron datos.")
            return

        st.success("✅ Datos cargados correctamente.")
        st.dataframe(df.head())

        st.markdown("### 🧬 Diccionario de Variables (Top 1000 registros)")
        resumen = pd.DataFrame({
            "Columna": df.columns,
            "Tipo de Dato": [df[col].dtype for col in df.columns],
            "Valores Únicos": [df[col].nunique() for col in df.columns],
            "Nulos (%)": [round(df[col].isna().mean() * 100, 2) for col in df.columns],
            "Ejemplo": [df[col].dropna().iloc[0] if df[col].dropna().shape[0] > 0 else "—" for col in df.columns]
        })

        st.dataframe(resumen)

        st.markdown("🔍 Puedes usar este diccionario para decidir qué columnas usar en tus análisis.")

    except Exception as e:
        st.error(f"❌ Error al consultar la base de datos: {e}")
