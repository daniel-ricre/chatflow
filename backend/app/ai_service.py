import httpx
from app.config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def chat(messages: list) -> str:
    """Envía el historial completo a Groq para mantener contexto."""
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "max_tokens": 1024,
                    "temperature": 0.7
                }
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"Error de API: {r.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
