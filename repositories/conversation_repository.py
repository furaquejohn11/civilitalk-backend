from sqlmodel import Session, select, col
from schemas.conversation_schema import ConversationCreate
from models import Conversation
from .ml_repository import MLRepository
from fastapi import FastAPI, WebSocket


class ConversationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        if conversation_data.has_chatguard:
            ml_repository = MLRepository()
            conversation_data.text = ml_repository.censor_profane_words(
                conversation_data.text
            )

        conversation = Conversation(
            inbox_id=conversation_data.inbox_id,
            sender_id=conversation_data.sender_id,
            text=conversation_data.text
        )

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)

        return conversation

    def read_conversation(self, inbox_id: int, page: int, page_size: int = 10) -> list[Conversation]:
        offset = (page - 1) * page_size

        conversation = (self.session.exec(
            select(Conversation)
            .where(Conversation.inbox_id == inbox_id)
            .offset(offset)
            .limit(page_size)
            .order_by(col(Conversation.created_at).desc())
            ).all())

        return list(reversed(conversation))

