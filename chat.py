# chat.py
import os
import re
import json
from openai import OpenAI
from calendar_integration import crear_evento

# Inicializa el cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parsear_cronograma(texto: str) -> list[dict]:
    """
    Extrae del texto un array de dicts con keys:
      - título
      - start (ISO)
      - end   (ISO)
    Se asume que la LLM usa un formato JSON en bloque dentro del texto.
    """
    match = re.search(r"```json(.*?)```", texto, flags=re.DOTALL)
    if not match:
        raise ValueError("No encontré bloque JSON en la respuesta")
    bloque = match.group(1).strip()
    return json.loads(bloque)

def chat_with_gari(usuario_id: str, mensaje: str) -> dict:
    """
    Llama a la LLM, extrae cronograma, crea eventos y retorna todo.
    """
    # 1) Generar respuesta con cronograma en JSON
    prompt = (
        "Eres GariMind, un asistente ejecutivo que produce un plan de acción con fechas.\n"
        "Cuando te pregunte, devuélveme UNA RESPUESTA en este formato:\n"
        "Primero un bloque de texto con explicación, luego:\n"
        "```json\n"
        "[ {\"título\":\"...\", \"start\":\"YYYY-MM-DDTHH:MM:SS-ZZZZ\", \"end\":\"...\"}, ... ]\n"
        "```\n"
        "Nada más."
    )
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": mensaje}
        ]
    ).choices[0].message.content

    # 2) Parsear cronograma de la respuesta
    cronograma = parsear_cronograma(respuesta)

    # 3) Crear eventos y acumular enlaces
    calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
    enlaces = []
    for item in cronograma:
        url = crear_evento(
            calendar_id=calendar_id,
            summary=item["título"],
            start_datetime=item["start"],
            end_datetime=item["end"]
        )
        enlaces.append(url)

    # 4) Devolver todo junto
    return {
        "respuesta": respuesta,
        "cronograma": cronograma,
        "enlaces": enlaces
    }

