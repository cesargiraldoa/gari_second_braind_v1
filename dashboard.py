import streamlit as st
from gari_secondbrain_analytics import main as analytics_main
from explorador_tabla import explorar_tabla

st.set_page_config(page_title="Gari Second Brain Analytics", layout="wide")

st.title("🧠 Gari Second Brain – Analytics Visual")

# Menú lateral
menu = st.sidebar.radio("Selecciona módulo", [
    "🔍 Gari Analytics",
    "🧪 Explorador SQL"
])

if menu == "🔍 Gari Analytics":
    analytics_main()

elif menu == "🧪 Explorador SQL":
    explorar_tabla()  # ✅ NO pasar nombre_tabla
