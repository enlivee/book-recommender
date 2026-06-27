from google.generativeai import genai
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


async def get_embedding(text: str) -> list[float]:
    """Получает эмбеддинг текста через Gemini API."""
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )
    return result.embeddings[0].values