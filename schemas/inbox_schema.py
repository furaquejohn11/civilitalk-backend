from pydantic import BaseModel, Field
from datetime import datetime, timezone


class InboxCreate(BaseModel):
    created_by: int = Field()
    received_by: int
    has_chatguard: bool = Field(default=False)


class InboxRead(BaseModel):
    convo_id: int
    created_by: int
    received_by: int
    has_chatguard: bool


