# explorador_tabla.py

import streamlit as st
import pandas as pd
from db_connection import consultar_ventas

def explorar_tabla(nombre_tabla="[Prestaciones_Temporal]", cantidad=1000):
    """
    Consulta una tabla SQL Server y muestra estructura y preview de campos.
    """
    st.subheader("🧪 Explorador de Tabla SQL – Análisis de Campos")

    try:
        df = consultar_ventas(nombre_tabla, cantidad)

        if df.empty:
            st.warning("La tabla está vacía o no se pudo consultar.")
            return

        st.success(f"✅ Datos consultados exitosamente desde la BD ({len(df)} registros).")

        # Vista previa de los datos
        st.dataframe(df.head(10))

        # Mostrar info general de columnas
        st.markdown("### 📋 Información de Columnas")
        info = pd.DataFrame({
            'Columna': df.columns,
            'Tipo': [str(df[col].dtype) for col in df.columns],
            'Nulos (%)': [round(df[col].isna().mean() * 100, 2) for col in df.columns],
            'Únicos': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(info)

        # Identificación automática de variables
        numericas = df.select_dtypes(include='number').columns.tolist()
        categoricas = df.select_dtypes(include='object').columns.tolist()
        fechas = df.select_dtypes(include='datetime').columns.tolist()

        st.markdown("### 🔍 Columnas identificadas por tipo")
        st.markdown(f"- **Numéricas:** {', '.join(numericas) if numericas else 'Ninguna'}")
        st.markdown(f"- **Categóricas:** {', '.join(categoricas) if categoricas else 'Ninguna'}")
        st.markdown(f"- **Fechas:** {', '.join(fechas) if fechas else 'Ninguna'}")

        return df

    except Exception as e:
        st.error(f"❌ Error al consultar la base de datos: {e}")
        return pd.DataFrame()
