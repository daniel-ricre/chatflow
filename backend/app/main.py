from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db, engine, Base
from app.models import User, Chatbot
from app.security import get_password_hash, verify_password, create_access_token, decode_token
from app.ai_service import chat

app = FastAPI(title="ChatFlow AI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class R(BaseModel): email: str; password: str; company_name: str; business_type: str
class L(BaseModel): email: str; password: str
class CB(BaseModel): name: str; welcome_message: str = "¡Hola!"; personality: str = "Eres amable."
class CH(BaseModel): chatbot_id: int; message: str

@app.on_event("startup")
async def init(): Base.metadata.create_all(bind=engine)

@app.post("/api/v1/register")
async def register(d: R, db=Depends(get_db)):
    if db.query(User).filter(User.email == d.email).first(): raise HTTPException(400, "Email ya existe")
    u = User(email=d.email, hashed_password=get_password_hash(d.password), company_name=d.company_name, business_type=d.business_type)
    db.add(u); db.commit()
    return {"message": "OK", "plan": "free"}

@app.post("/api/v1/login")
async def login(d: L, db=Depends(get_db)):
    u = db.query(User).filter(User.email == d.email).first()
    if not u or not verify_password(d.password, u.hashed_password): raise HTTPException(401, "Credenciales inválidas")
    return {"token": create_access_token({"sub": str(u.id)}), "name": u.company_name}

@app.post("/api/v1/chatbots")
async def create_bot(d: CB, token: str = Query(...), db=Depends(get_db)):
    try: u = db.query(User).filter(User.id == int(decode_token(token)["sub"])).first()
    except: raise HTTPException(401, "Token inválido")
    b = Chatbot(name=d.name, user_id=u.id, welcome_message=d.welcome_message, personality=f"{d.personality} Negocio: {u.business_type}.", embed_code=f'<script src="https://chatflow.onrender.com/w/{u.id}"></script>')
    db.add(b); u.chatbots_created += 1; db.commit()
    return {"id": b.id, "embed": b.embed_code}

@app.post("/api/v1/chat")
async def chat_msg(d: CH, db=Depends(get_db)):
    b = db.query(Chatbot).filter(Chatbot.id == d.chatbot_id).first()
    if not b: raise HTTPException(404, "Bot no encontrado")
    u = db.query(User).filter(User.id == b.user_id).first()
    prompt = f"Eres {b.name}. {b.personality}\nCliente: {d.message}\nRespuesta:"
    return {"response": await chat(prompt)}

@app.get("/")
async def root(): return {"status": "online"}
