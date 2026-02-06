import uuid
import time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from .database import DbSession, DbMessage

class SessionManager:
    def create_session(self, db: Session, name: str) -> DbSession:
        session_id = str(uuid.uuid4())
        db_session = DbSession(
            id=session_id,
            name=name,
            created_at=time.time()
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    def get_session(self, db: Session, session_id: str) -> Optional[DbSession]:
        return db.query(DbSession).filter(DbSession.id == session_id).first()

    def list_sessions(self, db: Session) -> List[DbSession]:
        return db.query(DbSession).order_by(DbSession.created_at.desc()).all()

    def rename_session(self, db: Session, session_id: str, name: str) -> Optional[DbSession]:
        session = self.get_session(db, session_id)
        if session:
            session.name = name
            db.commit()
            db.refresh(session)
        return session

    def delete_session(self, db: Session, session_id: str) -> bool:
        session = self.get_session(db, session_id)
        if session:
            # Messages will be deleted by cascade if configured, or manually:
            db.query(DbMessage).filter(DbMessage.session_id == session_id).delete()
            db.delete(session)
            db.commit()
            return True
        return False

    def add_message(self, db: Session, session_id: str, role: str, content: str):
        message_id = str(uuid.uuid4())
        db_message = DbMessage(
            id=message_id,
            session_id=session_id,
            role=role,
            content=content,
            created_at=time.time()
        )
        db.add(db_message)
        db.commit()

    def get_messages(self, db: Session, session_id: str) -> List[DbMessage]:
        return db.query(DbMessage).filter(DbMessage.session_id == session_id).order_by(DbMessage.created_at).all()

# Global session manager
manager = SessionManager()
