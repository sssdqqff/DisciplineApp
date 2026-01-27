from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional
from ..models.category import Category
from ..models.task import Task
from ..schemas.category import CategoryCreate, CategoryUpdate
from sqlalchemy.exc import SQLAlchemyError

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    # Основной метод: возвращает категории с активными задачами
    def get_all(self, user_id: Optional[int] = None) -> List[Category]:
        stmt = select(Category).options(
            selectinload(Category.tasks.and_(Task.is_active == True))  # <-- только активные задачи
        )
        if user_id:
            stmt = stmt.where(Category.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalars().all()
    
    # Базовый метод: возвращает категории без задач
    def get_all_basic(self, user_id: Optional[int] = None) -> List[Category]:
        stmt = select(Category)
        if user_id:
            stmt = stmt.where(Category.user_id == user_id)
        result = self.db.execute(stmt)
        return result.scalars().all()

    # Возвращает категорию с активными задачами по ID
    def get_by_id(self, category_id: int, user_id: Optional[int] = None) -> Optional[Category]:
        stmt = select(Category).options(
            selectinload(Category.tasks.and_(Task.is_active == True))
        ).where(Category.id == category_id)
        if user_id:
            stmt = stmt.where(Category.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    # Возвращает категорию по имени (тоже с активными задачами)
    def get_by_name(self, name: str, user_id: Optional[int] = None) -> Optional[Category]:
        stmt = select(Category).options(
            selectinload(Category.tasks.and_(Task.is_active == True))
        ).where(Category.name == name)
        if user_id:
            stmt = stmt.where(Category.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()
    
    # Создание категории
    def create(self, category_create: CategoryCreate, user_id: int) -> Category:
        new_category = Category(**category_create.model_dump(), user_id=user_id)
        try:
            self.db.add(new_category)
            self.db.commit()
            self.db.refresh(new_category)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return new_category
    
    # Обновление категории
    def update(self, category_id: int, category_update: CategoryUpdate) -> Category:
        category = self.get_by_id(category_id)
        if not category:
            return None
        for key, value in category_update.model_dump().items():
            setattr(category, key, value)
        try:
            self.db.commit()
            self.db.refresh(category)   
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return category
    
    # Логическое удаление категории
    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        if not category:
            return
        category.is_active = False
        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise