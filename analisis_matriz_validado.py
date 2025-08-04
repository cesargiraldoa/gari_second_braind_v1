def diagnostico_foda():
    return [
        "✅ FODA diligenciado con fortalezas claras (BI, integración mercado).",
        "⚠️ Algunas oportunidades bien formuladas, pero no todas con vínculo a decisiones visibles.",
        "🚨 Amenazas como BUK y ASCENDO reconocidas, pero falta estrategia ofensiva sólida contra ellas.",
        "🧩 Estrategias de reorientación y defensivas formuladas, pero poco diferenciadas."
    ]

def diagnostico_mefe_mefi():
    return [
        "✅ MEFE y MEFI con factores críticos cuantificados y ponderados correctamente.",
        "📊 La organización tiene puntuación media-alta en fortalezas internas (2.55) y externas (2.30).",
        "⚠️ No hay mención clara a cómo estas valoraciones alimentan decisiones específicas en estrategias."
    ]

def diagnostico_porter_pest():
    return [
        "✅ 5 Fuerzas bien estructuradas: análisis completo de competencia, entrada y proveedores.",
        "📈 Entorno PEST detallado por política, economía, social y tecnología.",
        "⚠️ Algunas amenazas del entorno político y económico no se reflejan aún en propuestas estratégicas visibles."
    ]

def diagnostico_mckinsey_bcg_ansoff_adl():
    return [
        "✅ Matriz McKinsey aplicada con pesos, evaluación por unidad y burbuja visual.",
        "📉 BCG muestra enfoque conservador (3 Cash Cows), falta Stars y Question Marks activos.",
        "🟡 ADL estructuralmente vacía: no hay posicionamiento claro por unidad o ciclo de vida.",
        "📊 Ansoff completo con iniciativas reales en penetración y desarrollo de mercado."
    ]

def diagnostico_canvas_objetivos():
    return [
        "⚠️ El modelo Canvas está visualmente presente, pero no diligenciado.",
        "📌 Factores clave 2022 bien formulados: objetivos por segmento, metas y plazo.",
        "✅ Planificación táctica clara en campañas digitales, cursos, crecimiento por canal."
    ]

def diagnostico_conclusiones():
    return [
        "✅ Hoja de conclusiones estructurada entre análisis interno y externo.",
        "🧠 Se reconocen oportunidades estratégicas bien alineadas a visión y amenazas del entorno.",
        "⚠️ Faltan conexiones directas entre esas conclusiones y las matrices previas."
    ]

def obtener_diagnostico_validado():
    return (
        diagnostico_foda() +
        diagnostico_mefe_mefi() +
        diagnostico_porter_pest() +
        diagnostico_mckinsey_bcg_ansoff_adl() +
        diagnostico_canvas_objetivos() +
        diagnostico_conclusiones()
    )
