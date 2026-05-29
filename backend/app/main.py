from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from app.database import get_db, engine, Base
from app.models import User, Chatbot, Conversation
from app.security import get_password_hash, verify_password, create_access_token, decode_token
from app.ai_service import chat

app = FastAPI(title="ChatFlow AI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class R(BaseModel): email: str; password: str; company_name: str; business_type: str
class L(BaseModel): email: str; password: str
class CB(BaseModel): name: str; welcome_message: str = "¡Hola!"; personality: str = "Eres amable."
class Msg(BaseModel): role: str; content: str
class CH(BaseModel): chatbot_id: int; message: str; history: Optional[List[Msg]] = []

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
    
    b = Chatbot(
        name=d.name,
        user_id=u.id,
        welcome_message=d.welcome_message,
        personality=f"{d.personality} Negocio: {u.business_type}."
    )
    db.add(b)
    db.flush()
    
    b.embed_code = f'<script src="https://chatflow-frontend-r6mx.onrender.com/widget.js" data-chatbot="{b.id}"></script>'
    u.chatbots_created += 1
    db.commit()
    db.refresh(b)
    
    return {"id": b.id, "embed": b.embed_code}

@app.post("/api/v1/chat")
async def chat_msg(d: CH, db=Depends(get_db)):
    b = db.query(Chatbot).filter(Chatbot.id == d.chatbot_id).first()
    if not b: raise HTTPException(404, "Bot no encontrado")
    u = db.query(User).filter(User.id == b.user_id).first()

    # Prompt mejorado: instrucción directa para recordar la conversación
    system_msg = (
        f"Eres {b.name}. {b.personality} "
        "Recuerda TODO el historial de la conversación. "
        "Cuando el usuario pregunte por una opción numérica (ej: 'opción 2', 'la segunda opción'), "
        "responde directamente con la información de esa opción que tú mismo listaste anteriormente. "
        "No pidas más contexto, solo recupera la información que ya diste. "
        "No vuelvas a presentarte a menos que te lo pidan explícitamente."
    )
    messages = [{"role": "system", "content": system_msg}]
    for h in (d.history or []):
        messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": d.message})

    response = await chat(messages)
    db.add(Conversation(chatbot_id=b.id, user_message=d.message, bot_response=response))
    b.total_chats += 1
    db.commit()
    return {"response": response}

@app.get("/")
async def root(): return {"status": "online"}
