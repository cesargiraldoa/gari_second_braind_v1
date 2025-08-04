import streamlit as st
import pandas as pd
import pymssql

from bic3 import save_uploaded_file, analyze_file
from estrategia import (
    analizar_dafo,
    analizar_plan_marketing,
    analizar_simulador_financiero
)
from motor_estrategico import (
    analizar_plan_completo,
    generar_diagnostico_preliminar
)
from openai_resumen import generar_resumen_con_openai
from analisis_matriz_validado import obtener_diagnostico_validado
import gari_analytics
from ventas_connector import fetch_sample_data

st.set_page_config(page_title="GariMind CésarStyle™", layout="wide")
st.title("🧠 GariMind CésarStyle™")

# ----------------------------------------
# 📂 MÓDULO BIC3
# ----------------------------------------
st.sidebar.markdown("## 📂 Módulo BIC3")
with st.sidebar.expander("Subir documentos para análisis BIC3"):
    context_choice = st.radio("Tipo de documento", ["General", "Por Empresa"])
    empresa_id = None
    if context_choice == "Por Empresa":
        empresa_id = st.text_input("ID de la empresa")

    uploaded_files = st.file_uploader("Subir archivos", accept_multiple_files=True)

    if st.button("📊 Ejecutar análisis BIC3") and uploaded_files:
        for file in uploaded_files:
            context_type = "general" if context_choice == "General" else "empresa"
            file_path = save_uploaded_file(file, context_type=context_type, empresa_id=empresa_id)
            output_path = analyze_file(file_path)
            st.success(f"Archivo procesado: {file.name}")
            with open(output_path, "r", encoding="utf-8") as result:
                st.text_area("Resultado del análisis", result.read(), height=200)

# ----------------------------------------
# 📈 ANÁLISIS ESTRATÉGICO - DAFO
# ----------------------------------------
st.markdown("## 📈 Análisis Estratégico: DAFO + Canvas")
with st.expander("Subir archivo DAFO para análisis"):
    uploaded_dafo = st.file_uploader("Cargar archivo Excel tipo DAFO", type=["xlsx"], key="dafo")
    if uploaded_dafo is not None:
        try:
            df_resultado = analizar_dafo(uploaded_dafo)
            st.success("✅ Análisis realizado con éxito.")
            df_resultado.insert(0, "No.", df_resultado.index + 1)
            st.dataframe(df_resultado)

            resumen = df_resultado.groupby("Análisis GariMind")["No."].apply(
                lambda x: f"{len(x)} ({', '.join(map(str, x))})"
            ).reset_index()
            resumen.columns = ["Tipo de diagnóstico", "Cantidad e Ítems"]
            st.markdown("### 🧠 Resumen Ejecutivo GariMind")
            st.table(resumen)
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo DAFO: {e}")

# ----------------------------------------
# 🧠 PLAN ESTRATÉGICO (modo GariMind SecondBrain)
# ----------------------------------------
st.markdown("## 🧠 Análisis: Plan Estratégico (Full Engine)")
with st.expander("Subir archivo completo del Plan Estratégico (.xlsx)"):
    uploaded_plan_full = st.file_uploader("Subir archivo completo del Plan Estratégico", type=["xlsx"], key="planfull")
    if uploaded_plan_full is not None:
        try:
            contenido = analizar_plan_completo(uploaded_plan_full)
            diagnostico = generar_diagnostico_preliminar(contenido)
            st.success("✅ Diagnóstico preliminar generado.")
            st.markdown("### 🗉 Diagnóstico por hoja")
            for r in diagnostico:
                st.markdown(f"- {r}")

            st.markdown("### 📊 Análisis técnico validado por evidencia")
            diagnostico_validado = obtener_diagnostico_validado()
            for linea in diagnostico_validado:
                st.markdown(f"- {linea}")

            st.markdown("### 🤖 Informe estratégico automatizado con OpenAI")
            contexto_file = st.file_uploader("📎 Subir archivo de contexto (principios TEE - .txt)", type=["txt"], key="contexto_openai")
            if st.button("🧠 Generar informe estratégico"):
                if contexto_file is not None:
                    try:
                        contexto_texto = contexto_file.read().decode("utf-8")
                        resumen = generar_resumen_con_openai(diagnostico_validado, contexto_texto)
                        st.success("✅ Informe generado con éxito:")
                        st.markdown("#### 📝 Informe Consultivo")
                        st.text_area("Resumen generado por GariMind + OpenAI", resumen, height=400)
                    except Exception as e:
                        st.error(f"❌ Error al generar el informe: {e}")
                else:
                    st.warning("📄 Por favor sube un archivo de contexto (.txt) antes de continuar.")
        except Exception as e:
            st.error(f"❌ Error al procesar el plan estratégico completo: {e}")

# ----------------------------------------
# 📢 PLAN DE MARKETING
# ----------------------------------------
st.markdown("## 📢 Análisis: Plan de Marketing")
with st.expander("Subir archivo de Plan de Marketing"):
    uploaded_marketing = st.file_uploader("Cargar archivo Plan de Marketing (.xlsx)", type=["xlsx"], key="marketing")
    if uploaded_marketing is not None:
        try:
            df_marketing = analizar_plan_marketing(uploaded_marketing)
            st.success("✅ Plan de marketing analizado.")
            st.dataframe(df_marketing)
        except Exception as e:
            st.error(f"❌ Error al procesar el Plan de Marketing: {e}")

# ----------------------------------------
# 💰 SIMULADOR FINANCIERO
# ----------------------------------------
st.markdown("## 💰 Análisis: Simulador Financiero")
with st.expander("Subir archivo Simulador Financiero"):
    uploaded_finanzas = st.file_uploader("Cargar archivo de simulador financiero (.xlsx)", type=["xlsx"], key="finanzas")
    if uploaded_finanzas is not None:
        try:
            df_finanzas = analizar_simulador_financiero(uploaded_finanzas)
            st.success("✅ Simulador financiero analizado.")
            st.dataframe(df_finanzas)
        except Exception as e:
            st.error(f"❌ Error al procesar el Simulador Financiero: {e}")

# ----------------------------------------
# 📊 ANÁLISIS DE VENTAS HISTÓRICAS
# ----------------------------------------
st.markdown("## 📊 Análisis de Ventas Históricas – Dentisalud")
with st.expander("📈 Ver datos reales de ventas desde SQL Server"):
    tabla = st.text_input("🔎 Nombre de la tabla de ventas:", value="[Prestaciones_Temporal]")
    cantidad = st.slider("Número de registros a mostrar", min_value=5, max_value=100, value=10)

    if st.button("📅 Consultar ventas"):
        try:
            df_ventas = fetch_sample_data(tabla, top_n=cantidad)
            st.success("✅ Datos consultados exitosamente desde la BD.")
            st.dataframe(df_ventas)
        except Exception as e:
            st.error(f"❌ Error al consultar la base de datos: {e}")

# ----------------------------------------
# 📊 GARI ANALYTICS
# ----------------------------------------
st.markdown("---")
st.header("📊 Gari Analytics – Edad vs Prestación")
with st.expander("📈 Ver análisis exploratorio de edad vs tipo de prestación"):
    if st.button("🚀 Ejecutar Gari Analytics"):
        try:
            gari_analytics.main()
        except Exception as e:
            st.error(f"❌ Error al ejecutar Gari Analytics: {e}")
