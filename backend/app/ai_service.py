import httpx
from app.config import GEMINI_API_KEY

async def chat(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
                json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":200}})
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            return f"Error de API: {r.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
