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


@router.get('/model')
def get_chatguard_model(inbox_id: int, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    chatguard_model = chatguard_repository.get_chatguard_model(inbox_id)
    return chatguard_model


@router.get('/rnn')
def set_rnn_model(inbox_id: int, name: str, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    chatguard_model = chatguard_repository.set_rnn_model(inbox_id, name)
    return chatguard_model


@router.get('/random_forest')
def set_random_forest_model(inbox_id: int, name: str, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    chatguard_model = chatguard_repository.set_random_forest_model(inbox_id, name)
    return chatguard_model


@router.get('/status')
def view_status(inbox_id: int, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    status = chatguard_repository.view_status(inbox_id)
    return status


@router.get('/help')
def view_help(inbox_id: int, session: Session = Depends(get_session)):
    chatguard_repository = ChatguardRepository(session)
    view = chatguard_repository.view_help(inbox_id)
    return view
