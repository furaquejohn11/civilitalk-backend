from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.db import get_session

from schemas.user_schema import UserCreate, UserLogin
from repositories import UserRepository

router = APIRouter()


@router.post('/signup')
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    user = user_repository.create_user(user_data)
    return user


@router.post('/login')
def login_user(user_data: UserLogin, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    user = user_repository.login_user(user_data)
    return user


@router.get('/{username}')
def get_user(username: str, session: Session = Depends(get_session)):
    user_repository = UserRepository(session)
    user_read = user_repository.get_user(username)
    return user_read

