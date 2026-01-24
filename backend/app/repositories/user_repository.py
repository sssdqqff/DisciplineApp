from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user import User
from ..schemas.user import UserCreate
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Получить всех юзеров
    def get_all(self) -> List[User]:
        stmt = select(User)
        result = self.db.execute(stmt)
        return result.scalars().all()

    # Получить юзера по ID
    def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    # Получить юзера по nickname
    def get_by_nickname(self, nickname: str) -> Optional[User]:
        stmt = select(User).where(User.nickname == nickname)
        return self.db.execute(stmt).scalar_one_or_none()

    # Создать нового юзера
    def create(self, user_create: UserCreate) -> User:
        new_user = User(**user_create.model_dump())
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return new_user
