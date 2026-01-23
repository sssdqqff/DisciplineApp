from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.category import CategoryCreate, CategoryResponse
from ..services.category_services import CategoryService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_all_categories()

@router.get("/{task_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_category_by_id(task_id)

@router.get("/tasks/{category_id}", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_tasks_by_category(category_id: int, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_category_by_id(category_id)