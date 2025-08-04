import pandas as pd

# --------------------------
# DAFO + Canvas
# --------------------------
def analizar_dafo(file):
    df = pd.read_excel(file)

    def generar_analisis(row):
        cat = row["Categoría DAFO"]
        sit = row["Situación actual (1-5)"]
        if cat == "Fortaleza" and sit >= 4:
            return "✅ Consolidar esta fortaleza como ventaja competitiva."
        elif cat == "Fortaleza":
            return "🔧 Potenciar esta fortaleza con acciones específicas."
        elif cat == "Debilidad" and sit <= 2:
            return "🚨 Debilidad crítica. Requiere atención prioritaria."
        elif cat == "Debilidad":
            return "⚠️ Debilidad relevante. Mitigar a corto plazo."
        elif cat == "Oportunidad" and sit <= 3:
            return "🌱 Explorar esta oportunidad estratégicamente."
        elif cat == "Amenaza" and sit >= 4:
            return "🔥 Riesgo latente. Preparar plan de contingencia."
        else:
            return "📝 Observar esta categoría y evaluar con más datos."

    df["Análisis GariMind"] = df.apply(generar_analisis, axis=1)
    return df

# --------------------------
# PLAN ESTRATÉGICO
# --------------------------
def analizar_plan_estrategico(file):
    df = pd.read_excel(file)
    df["Diagnóstico"] = df["Resultado Esperado"].apply(
        lambda x: "✅ Enfocado y claro." if isinstance(x, str) and len(x) > 30 else "⚠️ Resultado poco específico."
    )
    return df

# --------------------------
# PLAN DE MARKETING
# --------------------------
def analizar_plan_marketing(file):
    df = pd.read_excel(file)
    df["Diagnóstico"] = df["Objetivo"].apply(
        lambda x: "🎯 Objetivo claro." if isinstance(x, str) and "segmento" in x.lower() else "📝 Requiere ajustar enfoque al cliente."
    )
    return df

# --------------------------
# SIMULADOR FINANCIERO
# --------------------------
def analizar_simulador_financiero(file):
    df = pd.read_excel(file)
    if "Utilidad Neta" in df.columns:
        promedio = df["Utilidad Neta"].mean()
        df["Diagnóstico"] = df["Utilidad Neta"].apply(
            lambda x: "✅ Proyección saludable." if x >= promedio else "⚠️ Margen bajo frente al promedio."
        )
    else:
        df["Diagnóstico"] = "🛑 No se encontró columna 'Utilidad Neta'."
    return df
