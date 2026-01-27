from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.exc import SQLAlchemyError

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    # Получить все активные задачи (по юзеру)
    def get_all(self, user_id: Optional[int] = None) -> List[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    # Получить конкретную активную задачу по ID (по юзеру)
    def get_by_id(self, task_id: int, user_id: Optional[int] = None) -> Optional[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.id == task_id, Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()
    
    # Получить активную задачу по имени (по юзеру)
    def get_by_name(self, name: str, user_id: Optional[int] = None) -> Optional[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.name == name, Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    # Создать задачу с обязательным user_id
    def create(self, task_create: TaskCreate, user_id: int) -> Task:
        new_task = Task(**task_create.model_dump(), user_id=user_id)
        try:
            self.db.add(new_task)
            self.db.commit()
            self.db.refresh(new_task)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return new_task
    
    # Получить несколько активных задач по списку ID (по юзеру)
    def get_multiple_by_ids(self, task_ids: List[int], user_id: Optional[int] = None) -> List[Task]:
        stmt = select(Task).options(selectinload(Task.category)).where(Task.id.in_(task_ids), Task.is_active == True)
        if user_id is not None:
            stmt = stmt.where(Task.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalars().all()
    
    # Обновить задачу (проверка по user_id)
    def update(self, task_id: int, task_update: TaskUpdate, user_id: Optional[int] = None) -> Optional[Task]:
        task = self.get_by_id(task_id, user_id=user_id)
        if not task:
            return None
        for key, value in task_update.model_dump().items():
            setattr(task, key, value)
        try:
            self.db.commit()
            self.db.refresh(task)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return task
    
    # Логическое удаление задачи (с учётом user_id)
    def delete(self, task_id: int, user_id: Optional[int] = None) -> None:
        task = self.get_by_id(task_id, user_id=user_id)
        if not task:
            return
        task.is_active = False
        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
