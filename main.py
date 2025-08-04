import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chat import chat_with_gari
from calendar_integration import crear_evento
from tasks_integration import TaskCreate, TaskOut, create_task, list_tasks

app = FastAPI()

class ChatRequest(BaseModel):
    usuario_id: str
    mensaje: str

@app.post("/chat")
async def chat_endpoint(data: ChatRequest):
    try:
        result = chat_with_gari(data.usuario_id, data.mensaje)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/")
async def root():
    return {"message": "🚀 GariMind API en producción, todo listo."}


# ——————————————————————————————————————————————————
#   TASKS ENDPOINTS
# ——————————————————————————————————————————————————

@app.post("/tasks", response_model=TaskOut, status_code=201)
async def tasks_create_endpoint(task: TaskCreate):
    """
    Crea una nueva tarea para el usuario.
    """
    try:
        return create_task(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks", response_model=list[TaskOut])
async def tasks_list_endpoint():
    """
    Lista todas las tareas.
    """
    try:
        return list_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ——————————————————————————————————————————————————
#   CALENDAR ENDPOINT
# ——————————————————————————————————————————————————

class CalendarCreate(BaseModel):
    summary: str
    start: str  # ISO datetime
    end: str    # ISO datetime

@app.post("/calendar")
async def calendar_create_endpoint(payload: CalendarCreate):
    """
    Crea un evento en Google Calendar usando la integración.
    """
    calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
    if not calendar_id:
        raise HTTPException(400, "Falta la variable GOOGLE_CALENDAR_ID")
    try:
        url = crear_evento(
            calendar_id=calendar_id,
            summary=payload.summary,
            start_datetime=payload.start,
            end_datetime=payload.end
        )
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
