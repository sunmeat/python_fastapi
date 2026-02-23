from sqlalchemy.orm import Session
from typing import List
from models import Message
from schemas import MessageOut

def get_messages(db: Session, limit: int = 100) -> List[MessageOut]:
    messages = (
        db.query(Message)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    return [MessageOut.model_validate(m) for m in messages]

def create_message(db: Session, name: str, text: str) -> Message:
    db_message = Message(name=name, text=text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message