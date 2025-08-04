from openai import OpenAI
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()
# Crear cliente de OpenAI (requiere que OPENAI_API_KEY esté configurada como variable de entorno)
client = OpenAI()

def generar_resumen_con_openai(diagnostico_hojas: list, contexto_estrategia: str, modelo="gpt-4"):
    """
    Genera un informe estratégico consultivo que combina dos enfoques:
    1. Evaluación desde la Teoría de la Estrategia Emergente (TEE)
    2. Análisis técnico por matriz (FODA, PEST, Porter, McKinsey, Canvas)
    
    Args:
        diagnostico_hojas (list): Diagnóstico por hoja (uno por línea)
        contexto_estrategia (str): Texto del marco estratégico (ej: principios TEE)
        modelo (str): Modelo a usar en OpenAI (por defecto 'gpt-4')
    
    Returns:
        str: Texto completo del informe generado por OpenAI
    """

    diagnostico_texto = "\n".join(diagnostico_hojas)

    prompt = (
        "Eres un consultor estratégico senior. A partir del siguiente diagnóstico hoja por hoja, "
        "y del contexto conceptual basado en la Teoría de la Estrategia Emergente (TEE), genera un informe completo con los siguientes componentes:\n\n"

        "1️⃣ Enfoque Emergente (TEE):\n"
        "- Evalúa los hallazgos según los principios de Alejandro Salazar Yusti.\n"
        "- Detecta falacias estratégicas (predicción, formalización, independencia).\n"
        "- Sugiere recomendaciones TEE: breakthrough, disonancia, aprendizaje.\n\n"

        "2️⃣ Análisis Técnico por Matriz:\n"
        "- Revisa si FODA está bien formulado y reflejado en decisiones.\n"
        "- Evalúa si los factores del entorno (PEST) aparecen en la estrategia.\n"
        "- Identifica si hay una respuesta real a las fuerzas competitivas (Porter).\n"
        "- Valida si la segmentación en McKinsey se refleja en prioridades.\n"
        "- Comprueba la coherencia del modelo Canvas.\n\n"

        "3️⃣ Concluye con una Síntesis Ejecutiva Final.\n\n"

        "Diagnóstico por hoja:\n"
        f"{diagnostico_texto}\n\n"
        "Contexto TEE:\n"
        f"{contexto_estrategia}"
    )

    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Eres un consultor estratégico senior con experiencia en estrategia emergente y análisis técnico por matriz."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1200
    )

    return response.choices[0].message.content
