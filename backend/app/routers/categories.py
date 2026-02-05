from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services.category_services import CategoryService
from ..schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from backend.app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_all_categories(db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_all_categories()

@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_category_by_id(category_id)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate,  db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    category_service = CategoryService(db)
    return category_service.create_category(category, user_id=current_user.id)

@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    category_service = CategoryService(db)
    category = category_service.get_category_by_id(category_id)

    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this category")

    return category_service.update_category(category_id, category_update)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    category_service = CategoryService(db)
    category = category_service.get_category_by_id(category_id)

    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this category")

    category_service.delete_category(category_id)
    return None
