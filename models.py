from sqlalchemy import Column, Integer, String, DateTime, func

from database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    text = Column(String(1000), nullable=False)
    created_at = Column(DateTime, server_default=func.now())