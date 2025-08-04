from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os

# Inicializa el cliente de Calendar con la cuenta de servicio
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
KEY_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")  # ruta al JSON

creds = Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
service = build("calendar", "v3", credentials=creds)

def crear_evento(calendar_id: str, summary: str, start_datetime: str, end_datetime: str) -> str:
    event_body = {
        "summary": summary,
        "start": {"dateTime": start_datetime},
        "end":   {"dateTime": end_datetime},
    }
    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
    # Devuelve el enlace al evento
    return event.get("htmlLink")
