# config.py
from dotenv import load_dotenv
import os

# Carga variables de entorno desde .env
load_dotenv()

# Ejemplo de acceso:
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL    = os.getenv("SUPABASE_URL")
SUPABASE_KEY    = os.getenv("SUPABASE_SERVICE_KEY")
