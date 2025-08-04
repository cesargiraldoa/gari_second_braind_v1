# usuarios.py
from typing import Dict

# Ejemplo de almacenamiento en memoria (reemplaza con DB real).
_users: Dict[str, Dict] = {}

def crear_usuario(usuario_id: str, datos: Dict):
    _users[usuario_id] = datos

def obtener_usuario(usuario_id: str) -> Dict:
    return _users.get(usuario_id, {})

def listar_usuarios() -> Dict[str, Dict]:
    return _users

