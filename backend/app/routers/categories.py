from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError

from ..database import get_db
from ..services.category_services import CategoryService
from ..schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from ..services.user_services import UserService
from ..config import settings

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

# OAuth2 для Bearer токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Получаем текущего пользователя из токена
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_all_categories(db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_all_categories()

@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    return category_service.get_category_by_id(category_id)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)
    return category_service.create_category(category, user_id=current_user.id)

@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(
    category_id: int, 
    category_update: CategoryUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)

    # Проверка, что текущий пользователь владелец категории
    category = category_service.get_category_by_id(category_id)
    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this category")

    return category_service.update_category(category_id, category_update)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    category_service = CategoryService(db)

    # Проверка владельца
    category = category_service.get_category_by_id(category_id)
    if category.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this category")

    category_service.delete_category(category_id)
    return None
