from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.database import get_db, engine, Base
from app.models import User, Chatbot, Conversation
from app.security import get_password_hash, verify_password, create_access_token, decode_token
from app.ai_service import chat

app = FastAPI(title="ChatFlow AI")

# Configuración CORS más agresiva
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Middleware manual para asegurar headers CORS en todas las respuestas
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

class R(BaseModel): email: str; password: str; company_name: str; business_type: str
class L(BaseModel): email: str; password: str
class CB(BaseModel): name: str; welcome_message: str = "¡Hola!"; personality: str = "Eres amable."
class CH(BaseModel):
    chatbot_id: int
    message: str
    session_id: Optional[str] = None
    history: Optional[List[dict]] = []

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

    sid = d.session_id
    if not sid:
        sid = str(uuid.uuid4())

    db_messages = db.query(Conversation).filter(
        Conversation.chatbot_id == b.id,
        Conversation.session_id == sid
    ).order_by(Conversation.created_at.asc()).limit(20).all()

    messages = [{"role": "system", "content": f"Eres {b.name}. {b.personality} Recuerda toda la conversación anterior. Cuando el usuario se refiera a una opción numérica, responde directamente con la información que tú mismo diste en esa lista. No preguntes de nuevo."}]
    
    for conv in db_messages:
        messages.append({"role": "user", "content": conv.user_message})
        messages.append({"role": "assistant", "content": conv.bot_response})
    
    messages.append({"role": "user", "content": d.message})

    response = await chat(messages)

    db.add(Conversation(
        chatbot_id=b.id,
        session_id=sid,
        user_message=d.message,
        bot_response=response
    ))
    b.total_chats += 1
    db.commit()

    return {"response": response, "session_id": sid}

@app.get("/")
async def root(): return {"status": "online"}
