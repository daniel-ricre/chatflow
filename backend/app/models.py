from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    business_type = Column(String, nullable=False)
    plan = Column(String, default="free")
    chatbots_created = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Chatbot(Base):
    __tablename__ = "chatbots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    welcome_message = Column(String, default="¡Hola! ¿En qué puedo ayudarte?")
    personality = Column(Text)
    embed_code = Column(Text)
    total_chats = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"), nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
