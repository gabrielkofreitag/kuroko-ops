import os
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

from core.auth import validate_api_key, get_api_key
from core.llm_client import LLMClient
from core.models import LLMResponse, LLMMessage

from core.database import init_db, get_db
from core.session import manager as session_manager
from core.worktree import worktree_manager
from sqlalchemy.orm import Session

app = FastAPI(title="Kuroko-Ops API", version="0.1.0")

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

...

# Sessions Router
sessions_router = APIRouter(prefix="/sessions", tags=["sessions"])

@sessions_router.post("/")
async def create_session(name: str, db: Session = Depends(get_db)):
    return session_manager.create_session(db, name)

@sessions_router.get("/")
async def list_sessions(db: Session = Depends(get_db)):
    return session_manager.list_sessions(db)

@sessions_router.get("/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    session = session_manager.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = session_manager.get_messages(db, session_id)
    return {
        "id": session.id,
        "name": session.name,
        "created_at": session.created_at,
        "messages": messages
    }

@sessions_router.patch("/{session_id}")
async def rename_session(session_id: str, name: str, db: Session = Depends(get_db)):
    return session_manager.rename_session(db, session_id, name)

@sessions_router.delete("/{session_id}")
async def delete_session(session_id: str, db: Session = Depends(get_db)):
    return session_manager.delete_session(db, session_id)

from services.agents_md import AgentsMDService

agents_md_service = AgentsMDService()

@sessions_router.post("/{session_id}/summarize")
async def summarize_session(session_id: str, db: Session = Depends(get_db)):
    try:
        agents_md_service.update_with_session(db, session_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(sessions_router)
app.include_router(llm_router)

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
