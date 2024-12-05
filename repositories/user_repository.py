from fastapi import HTTPException, status
from sqlmodel import Session, select
from models import User
from schemas.user_schema import UserLogin, UserCreate, UserRead
from utils.password_utils import hash_password, verify_password


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.session.exec(select(User).where(User.username == user_data.username)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )

        hashed_password = hash_password(user_data.password)

        user = User(
            username=user_data.username,
            hashed_password=hashed_password,
            firstname=user_data.firstname,
            lastname=user_data.lastname
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def login_user(self, user_data: UserLogin) -> User:
        user = self.session.exec(select(User).where(User.username == user_data.username)).first()

        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password"
            )
        return user

    def get_user(self, username: str,) -> UserRead:
        user = self.session.exec(select(User).where(User.username == username)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        user_read = UserRead(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            id=user.id
        )

        return user_read

# class HeroRepository:
#     def __init__(self, session: Session):
#         self.session = session
#
#     def get_hero(self, hero_id: int) -> Hero | None:
#         return self.session.get(Hero, hero_id)
#
#     def get_all_heroes(self, offset: int = 0, limit: int = 100) -> list[Hero]:
#         return self.session.exec(select(Hero).offset(offset).limit(limit)).all()
#
#     def create_hero(self, hero: Hero) -> Hero:
#         self.session.add(hero)
#         self.session.commit()
#         self.session.refresh(hero)
#         return hero
#
#     def delete_hero(self, hero_id: int):
#         hero = self.session.get(Hero, hero_id)
#         if hero:
#             self.session.delete(hero)
#             self.session.commit()
#             return
