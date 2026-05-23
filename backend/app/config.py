import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatflow.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
