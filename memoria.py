# memoria.py

def obtener_recuerdos(usuario_id: str) -> str:
    """
    Retorna recuerdos simulados para pruebas iniciales.
    Luego se conectará a Supabase o PostgreSQL.
    """
    recuerdos = [
        "📌 Iniciaste el proyecto GariMind SecondBrain.",
        "✅ Insertaste el primer usuario correctamente.",
        "🧠 Se guardó un recuerdo sobre el propósito humano del sistema.",
        "🚀 GariMind ya está desplegado en Render y funcionando en producción."
    ]
    return "\n".join(recuerdos)
