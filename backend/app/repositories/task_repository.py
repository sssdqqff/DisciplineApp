from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models.task import Task
from ..schemas.task import TaskCreate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: Optional[int] = None) -> List[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, task_id: int, user_id: Optional[int] = None) -> Optional[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.id == task_id, Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str, user_id: Optional[int] = None) -> Optional[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.name == name, Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, task_create: TaskCreate, user_id: int) -> Task:
        new_task = Task(**task_create.model_dump(), user_id=user_id)
        try:
            self.db.add(new_task)
            await self.db.commit()
            await self.db.refresh(new_task)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return new_task

    async def get_multiple_by_ids(self, task_ids: List[int], user_id: Optional[int] = None) -> List[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.id.in_(task_ids), Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    
    async def update(self, task: Task) -> Task:
        try:
            await self.db.commit()
            await self.db.refresh(task)
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        return task

    async def delete(self, task_id: int, user_id: Optional[int] = None) -> None:
        task = await self.get_by_id(task_id, user_id=user_id)
        if not task:
            return
        task.is_active = False
        try:
            await self.db.commit()
        except SQLAlchemyError:
            await self.db.rollback()
            raise
