from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.db import get_session
from fastapi import APIRouter

from schemas.inbox_schema import InboxRead, InboxCreate
from repositories import InboxRepository

router = APIRouter()


@router.post('/create')
def create_inbox(inbox_data: InboxCreate, session: Session = Depends(get_session)):
    inbox_repository = InboxRepository(session)
    inbox = inbox_repository.create_inbox(inbox_data)
    return inbox


@router.get('/validate')
def has_inbox(sender_id: int, receiver_id: int, session: Session = Depends(get_session)):
    inbox_repository = InboxRepository(session)
    has_existing_inbox = inbox_repository.get_inbox_id(sender_id, receiver_id)
    return has_existing_inbox


@router.get('/inbox/{user_id}')
def get_user_inbox(user_id: int, session: Session = Depends(get_session)):
    inbox_repository = InboxRepository(session)
    user_inbox = inbox_repository.get_user_inbox(user_id)
    return user_inbox


@router.get('/user')
def get_inbox_preview(user_id: int, session: Session = Depends(get_session)):
    inbox_repository = InboxRepository(session)
    inbox_preview = inbox_repository.inbox_preview(user_id)
    return inbox_preview

