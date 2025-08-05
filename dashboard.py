# dashboard.py

import streamlit as st
from gari_secondbrain_analytics import main as analytics_main
from explorador_tabla import explorar_tabla
from eda_prestaciones import mostrar_eda  # 👈 NUEVO IMPORT

st.set_page_config(page_title="Gari Second Brain Analytics", layout="wide")

st.title("🧠 Gari Second Brain – Analytics Visual")

# Menú lateral para navegación
menu = st.sidebar.radio("Selecciona módulo", [
    "🔍 Gari Analytics",
    "🧪 Explorador SQL",
    "📊 Análisis EDA"  # 👈 NUEVA OPCIÓN
])

# Lógica por módulo
if menu == "🔍 Gari Analytics":
    analytics_main()

elif menu == "🧪 Explorador SQL":
    explorar_tabla()

elif menu == "📊 Análisis EDA":
    mostrar_eda()  # 👈 LLAMADO AL MÓDULO
