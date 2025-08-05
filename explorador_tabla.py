import streamlit as st
import pandas as pd
from db_connection import ejecutar_sql

def mostrar_explorador():
    st.markdown("## 🧪 Explorador de Tabla SQL – Análisis de Campos")

    tabla = st.text_input("🔢 Nombre de la tabla de ventas:", "Prestaciones_Temporal")
    limite = st.slider("📄 Número de registros a mostrar", min_value=1, max_value=1000, value=5)

    if st.button("📥 Consultar ventas"):
        nombre_tabla = tabla.strip()
        if not nombre_tabla.startswith("[") and not nombre_tabla.endswith("]"):
            nombre_tabla = f"[{nombre_tabla}]"

        query = f"SELECT TOP {limite} * FROM {nombre_tabla}"

        try:
            df = ejecutar_sql(query)
            if df.empty:
                st.warning("⚠ La consulta no retornó datos.")
            else:
                st.success("✅ Datos consultados exitosamente desde la BD.")
                st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Error al consultar la base de datos: {e}")

def explorar_tabla(nombre_tabla="[Prestaciones_Temporal]", cantidad=1000):
    st.markdown("## 🧪 Explorador de Tabla SQL – Análisis de Campos")

    st.write(f"Tabla seleccionada: `{nombre_tabla}` – Registros: {cantidad}")

    nombre = nombre_tabla.strip()
    if not nombre.startswith("[") and not nombre.endswith("]"):
        nombre = f"[{nombre}]"

    query = f"SELECT TOP {cantidad} * FROM {nombre}"

    try:
        df = ejecutar_sql(query)
        if df.empty:
            st.warning("⚠ La consulta no retornó datos.")
        else:
            st.success("✅ Datos consultados exitosamente desde la BD.")
            st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Error al consultar la base de datos: {e}")
