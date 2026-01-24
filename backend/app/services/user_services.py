from sqlalchemy.orm import Session
from typing import List, Optional
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse
from fastapi import HTTPException, status

class CategoryService:
    def __init__(self, db: Session):
        self.category_repository = UserRepository(db)
        self.db = db

    def get_all_users(self) -> List[UserResponse]:
        users = self.category_repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)
    
    def get_user_by_nickname(self, nickname: str) -> UserResponse:
        user = self.user_repository.get_by_nickname(nickname)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)

    def create_user(self, user_create: UserCreate) -> UserResponse:
        existing_user = self.category_repository.get_by_name(user_create.name)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists")

        new_user = self.category_repository.create(user_create)
        return UserResponse.model_validate(new_user)