from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..models.user import User
from ..schemas.user import UserUpdate
from sqlalchemy.exc import SQLAlchemyError


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_nickname(self, nickname: str) -> Optional[User]:
        stmt = select(User).where(User.nickname == nickname)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return user

    async def update(self, user: User) -> User:
        try:
            await self.db.commit()
            await self.db.refresh(user)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if not user:
            return
        try:
            await self.db.delete(user)
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise
