from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageCreate(BaseModel):
    name: str
    text: str

class MessageOut(BaseModel):
    id: int
    name: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)