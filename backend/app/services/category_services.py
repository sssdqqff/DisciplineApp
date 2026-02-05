from typing import List
from ..repositories.category_repository import CategoryRepository
from ..schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from fastapi import HTTPException, status


class CategoryService:
    def __init__(self, db):
        self.category_repository = CategoryRepository(db)
        self.db = db

    async def get_all_categories(self) -> List[CategoryResponse]:
        categories = await self.category_repository.get_all()
        return [CategoryResponse.model_validate(category) for category in categories]

    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return CategoryResponse.model_validate(category)

    async def create_category(self, category_create: CategoryCreate, user_id: int) -> CategoryResponse:
        existing_category = await self.category_repository.get_by_name(category_create.name, user_id=user_id)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )

        new_category = await self.category_repository.create(category_create, user_id=user_id)
        return CategoryResponse.model_validate(new_category)

    async def update_category(self, category_id: int, category_update: CategoryUpdate, user_id: int) -> CategoryResponse:
        category = await self.category_repository.get_by_id(category_id, user_id=user_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        data = category_update.model_dump(exclude_unset=True)
        ALLOWED_FIELDS = {"name", "description"}

        for key, value in data.items():
            if key in ALLOWED_FIELDS:
                setattr(category, key, value)

        updated_category = await self.category_repository.update(category)
        return CategoryResponse.model_validate(updated_category)

    async def delete_category(self, category_id: int) -> None:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        await self.category_repository.delete(category_id)
        return None
