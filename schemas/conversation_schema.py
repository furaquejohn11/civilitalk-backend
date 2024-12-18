from pydantic import BaseModel, Field

from datetime import datetime, timezone

from models import BotModel


class ConversationCreate(BaseModel):
    inbox_id: int
    sender_id: int
    text: str
    has_chatguard: bool = Field(default=False)
    bot_model: BotModel = Field(default=BotModel.RNN)


class ConversationRead(BaseModel):
    inbox_id: int
