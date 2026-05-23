from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(p): return pwd_context.hash(p)
def verify_password(p, h): return pwd_context.verify(p, h)
def create_access_token(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)
def decode_token(t): return jwt.decode(t, SECRET_KEY, algorithms=[ALGORITHM])
