from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from repositories import ConversationRepository
from schemas.conversation_schema import ConversationCreate

router = APIRouter()


@router.post('/create')
def create_conversation(
    conversation_data: ConversationCreate,
    session: Session = Depends(get_session)
):
    conversation_repository = ConversationRepository(session)
    conversation = conversation_repository.create_conversation(conversation_data)
    return conversation


@router.post('/batch-create')
def batch_create_conversations(
    conversations_data: List[ConversationCreate],
    session: Session = Depends(get_session)
):
    conversation_repository = ConversationRepository(session)
    conversations = conversation_repository.batch_create_conversations(conversations_data)
    return conversations


@router.get('/{inbox_id}')
def read_conversation(inbox_id: int, page: int, session: Session = Depends(get_session)):
    conversation_repository = ConversationRepository(session)
    conversation = conversation_repository.read_conversation(inbox_id, page)
    return conversation
