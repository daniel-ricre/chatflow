import httpx
from app.config import GROQ_API_KEY

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def chat(messages: list) -> str:
    """Envía el historial completo a Groq para mantener contexto."""
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "max_tokens": 200
                }
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"Error de API: {r.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
