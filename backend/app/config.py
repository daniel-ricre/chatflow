import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

settings = Settings()
