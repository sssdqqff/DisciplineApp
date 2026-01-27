from sqlalchemy.orm import Session
from typing import List
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse
from ..models.user import User
from fastapi import HTTPException, status
from app.utils.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.db = db

    def create_user(self, user_create: UserCreate) -> UserResponse:
        # Проверка на уникальность
        if self.user_repository.get_by_email(user_create.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.user_repository.get_by_nickname(user_create.nickname):
            raise HTTPException(status_code=400, detail="Nickname already taken")

        # Создание нового пользователя
        new_user = User(
            email=user_create.email,
            nickname=user_create.nickname,
            hashed_password=hash_password(user_create.password[:72])
        )
        created_user = self.user_repository.create(new_user)
        return UserResponse.model_validate(created_user)

    def get_all_users(self) -> List[UserResponse]:
        users = self.user_repository.get_all()
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

    def update_user(self, user_id: int, user_update: UserCreate) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Обновляем поля ORM-объекта
        user.nickname = user_update.nickname
        user.email = user_update.email
        user.hashed_password = hash_password(user_update.password[:72])

        updated_user = self.user_repository.update(user)
        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: int) -> None:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Передаём объект пользователя в репозиторий
        self.user_repository.delete(user)
