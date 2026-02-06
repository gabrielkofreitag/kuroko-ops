import time
from sqlalchemy import Column, String, Float, Text, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .database import engine, Base

class DbMemory(Base):
    __tablename__ = "memory"
    id = Column(String, primary_key=True, index=True)
    category = Column(String, index=True) # pattern, fact, guideline
    content = Column(Text)
    created_at = Column(Float)
    last_accessed = Column(Float)

def init_memory_db():
    Base.metadata.create_all(bind=engine)

class MemoryService:
    def __init__(self, db_session):
        self.db = db_session

    def add_memory(self, category: str, content: str):
        import uuid
        memory = DbMemory(
            id=str(uuid.uuid4()),
            category=category,
            content=content,
            created_at=time.time(),
            last_accessed=time.time()
        )
        self.db.add(memory)
        self.db.commit()

    def search_memory(self, query: str, limit: int = 5) -> str:
        # Simple keyword search for now
        # In Phase E/F we would add real vector search
        memories = self.db.query(DbMemory).filter(DbMemory.content.contains(query)).limit(limit).all()
        if not memories:
            return "No relevant memories found."
            
        return "\n---\n".join([f"[{m.category}] {m.content}" for m in memories])
