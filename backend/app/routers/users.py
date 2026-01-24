from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.user import UserCreate, UserResponse
from ..services.user_services import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_user_by_id(user_id)

@router.get("/nickname/{nickname}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_nickname(nickname: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_user_by_nickname(nickname)

