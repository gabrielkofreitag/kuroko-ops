import os
import uuid
import time
from sqlalchemy import Column, String, Float, Text, ForeignKey, JSON, create_engine
from sqlalchemy.orm import relationship, sessionmaker, DeclarativeBase
from typing import List, Dict, Any, Optional

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kuroko.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class DbSession(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(Float)
    metadata_json = Column(JSON, default={})
    
    messages = relationship("DbMessage", back_populates="session", cascade="all, delete-orphan")

class DbMessage(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String) # user, assistant, system
    content = Column(Text)
    created_at = Column(Float)
    
    session = relationship("DbSession", back_populates="messages")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
