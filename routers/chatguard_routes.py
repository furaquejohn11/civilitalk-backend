from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from repositories import ConversationRepository, ChatguardRepository
from schemas.conversation_schema import ConversationCreate

router = APIRouter()


@router.get('/enable')
def enable_chatguard(inbox_id: int, name: str, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    chatguard = chatguard_repository.enable_chatguard(inbox_id, name)
    return chatguard


@router.get('/disable')
def disable_chatguard(inbox_id: int, name: str, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    chatguard = chatguard_repository.disable_chatguard(inbox_id, name)
    return chatguard


@router.get('/inbox')
def has_chatguard(inbox_id: int, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    get_chatguard = chatguard_repository.has_chatguard(inbox_id)
    return get_chatguard
