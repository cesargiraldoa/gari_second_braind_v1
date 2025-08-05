import streamlit as st
from gari_secondbrain_analytics import main as analytics_main
from explorador_tabla import explorar_tabla

st.set_page_config(page_title="Gari Second Brain Analytics", layout="wide")

st.title("🧠 Gari Second Brain – Analytics Visual")

# Menú lateral para navegación
menu = st.sidebar.radio("Selecciona módulo", [
    "🔍 Gari Analytics",
    "🧪 Explorador SQL"
])

# Módulo de análisis general
if menu == "🔍 Gari Analytics":
    analytics_main()

# Explorador SQL usando mismo flujo que "Consulta ventas"
elif menu == "🧪 Explorador SQL":
    explorar_tabla()  # ✅ sin pasar parámetros
