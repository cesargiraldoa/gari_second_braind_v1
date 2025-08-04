from pydantic import BaseModel
from datetime import datetime
import uuid

# Modelo de entrada y salida
class TaskCreate(BaseModel):
    title: str
    due: datetime | None = None

class TaskOut(TaskCreate):
    id: str

# Almacenamos en memoria para este ejemplo
_tasks: list[TaskOut] = []

def create_task(data: TaskCreate) -> TaskOut:
    task = TaskOut(id=str(uuid.uuid4()), **data.dict())
    _tasks.append(task)
    return task

def list_tasks() -> list[TaskOut]:
    return _tasks
