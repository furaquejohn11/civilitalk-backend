from typing import Optional, List

from sqlmodel import Session, select, col
from schemas.conversation_schema import ConversationCreate
from models import Conversation
from .ml_repository import MLRepository


class ConversationRepository:
    def __init__(self, session: Session, ml_repository: Optional[MLRepository] = None):
        self.session = session
        self._ml_repository = ml_repository or MLRepository()

    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        # Conditionally apply chat guard filtering
        if conversation_data.has_chatguard:
            conversation_data.text = self._ml_repository.censor_profane_words(
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

    def batch_create_conversations(self, conversations_data: List[ConversationCreate]) -> List[Conversation]:
        conversations = []

        for conversation_data in conversations_data:
            conversation = self.create_conversation(conversation_data)
            conversations.append(conversation)

        return conversations

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

    def latest_conversation(self, inbox_id: int) -> tuple:
        conversation = (self.session.exec(
            select(Conversation.sender_id, Conversation.text, Conversation.created_at)
            .where(Conversation.inbox_id == inbox_id)
            .order_by(col(Conversation.created_at).desc())
            .limit(1)
        )).first()

        return conversation

