import os
from sqlalchemy.orm import Session
from ..core.database import DbSession, DbMessage

class AgentsMDService:
    def __init__(self, file_path: str = "AGENTS.md"):
        self.file_path = file_path

    def update_with_session(self, db: Session, session_id: str):
        session = db.query(DbSession).filter(DbSession.id == session_id).first()
        if not session:
            return

        messages = db.query(DbMessage).filter(DbMessage.session_id == session_id).order_by(DbMessage.created_at).all()
        
        # Simple extraction of the first user message as the "Task"
        user_msgs = [m for m in messages if m.role == "user"]
        if not user_msgs:
            return
            
        task_summary = user_msgs[0].content[:100] + "..." if len(user_msgs[0].content) > 100 else user_msgs[0].content
        
        history_entry = f"\n- {time.strftime('%Y-%m-%d %H:%M:%S')}: {task_summary}"
        
        if os.path.exists(self.file_path):
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(history_entry)
        else:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(f"# Kuroko-Ops Task History\n{history_entry}")

import time
