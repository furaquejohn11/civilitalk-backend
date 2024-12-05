from pydantic import BaseModel, Field

from datetime import datetime, timezone


class ConversationCreate(BaseModel):
    inbox_id: int
    sender_id: int
    text: str
    has_chatguard: bool = Field(default=False)


class ConversationRead(BaseModel):
    inbox_id: int
