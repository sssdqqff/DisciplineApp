from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models.category import Category
from ..models.task import Task
from ..schemas.category import CategoryCreate
from sqlalchemy.exc import SQLAlchemyError


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: Optional[int] = None) -> List[Category]:
        stmt = select(Category).options(
            selectinload(Category.tasks.and_(Task.is_active == True))
        )
        if user_id is not None:
            stmt = stmt.where(Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all_basic(self, user_id: Optional[int] = None) -> List[Category]:
        stmt = select(Category)
        if user_id is not None:
            stmt = stmt.where(Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, category_id: int, user_id: Optional[int] = None) -> Optional[Category]:
        stmt = select(Category).options(
            selectinload(Category.tasks.and_(Task.is_active == True))
        ).where(Category.id == category_id)
        if user_id is not None:
            stmt = stmt.where(Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str, user_id: Optional[int] = None) -> Optional[Category]:
        stmt = select(Category).options(
            selectinload(Category.tasks.and_(Task.is_active == True))
        ).where(Category.name == name)
        if user_id is not None:
            stmt = stmt.where(Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, category_create: CategoryCreate, user_id: int) -> Category:
        new_category = Category(**category_create.model_dump(), user_id=user_id)
        try:
            self.db.add(new_category)
            await self.db.commit()
            await self.db.refresh(new_category)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return new_category

    async def update(self, category: Category) -> Category:
        try:
            await self.db.commit()
            await self.db.refresh(category)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return category

    async def delete(self, category_id: int) -> None:
        category = await self.get_by_id(category_id)
        if not category:
            return
        category.is_active = False
        try:
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise
