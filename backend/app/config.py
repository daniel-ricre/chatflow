import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatflow.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
