from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user import User
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
    
    # Получить юзера по email
    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    # Получить юзера по nickname
    def get_by_nickname(self, nickname: str) -> Optional[User]:
        stmt = select(User).where(User.nickname == nickname)
        return self.db.execute(stmt).scalar_one_or_none()

    # Создать нового юзера (принимаем ORM-объект User)
    def create(self, user: User) -> User:
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return user
    
    # Обновить юзера (принимаем ORM-объект User с уже изменёнными полями)
    def update(self, user: User) -> User:
        try:
            self.db.commit()
            self.db.refresh(user)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return user
    
    # Удалить юзера
    def delete(self, user: User) -> None:
        try:
            self.db.delete(user)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
