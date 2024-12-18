from typing import Optional

from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from enum import Enum


class BotModel(str, Enum):
    RNN = "RNN"
    RANDOM_FOREST = "RANDOM_FOREST"
    SVG = "SVG"


class Inbox(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: int = Field(foreign_key="user.id")  # Reference to the user who created the message
    received_by: int = Field(foreign_key="user.id")  # Reference to the user who receives the message
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    has_chatguard: bool = Field(default=False)
    bot_model: BotModel = Field(default=BotModel.RANDOM_FOREST)

