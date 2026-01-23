from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryCreate, CategoryResponse
from fastapi import HTTPException, status

class CategoryService:
    def __init__(self, db: Session):
        self.category_repository = CategoryRepository(db)
        self.db = db

    def get_all_categories(self) -> List[CategoryResponse]:
        categories = self.category_repository.get_all()
        return [CategoryResponse.model_validate(category) for category in categories]

    def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return CategoryResponse.model_validate(category)

    def create_category(self, category_create: CategoryCreate) -> CategoryResponse:
        existing_category = self.category_repository.get_by_name(category_create.name)
        if existing_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category with this name already exists")
        
        new_category = self.category_repository.create(category_create)
        return CategoryResponse.model_validate(new_category)