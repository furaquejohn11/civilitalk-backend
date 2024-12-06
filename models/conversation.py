from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import datetime, timezone, timedelta


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inbox_id: int = Field(foreign_key="inbox.id")
    sender_id: int = Field(foreign_key="user.id")  # Reference to the sender user
    text: str  # The conversation message
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)
                                 .astimezone(timezone(timedelta(hours=8))))
