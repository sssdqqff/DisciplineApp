from typing import List
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse
from ..models.user import User
from fastapi import HTTPException, status
from app.utils.security import hash_password


class UserService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)
        self.db = db

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        if await self.user_repository.get_by_email(user_create.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if await self.user_repository.get_by_nickname(user_create.nickname):
            raise HTTPException(status_code=400, detail="Nickname already taken")

        new_user = User(
            email=user_create.email,
            nickname=user_create.nickname,
            hashed_password=hash_password(user_create.password[:72])
        )
        created_user = await self.user_repository.create(new_user)
        return UserResponse.model_validate(created_user)

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.user_repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)

    async def get_user_by_nickname(self, nickname: str) -> UserResponse:
        user = await self.user_repository.get_by_nickname(nickname)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_update: UserCreate) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        ALLOWED_FIELDS = {"nickname", "email", "password"}
        data = user_update.model_dump(exclude_unset=True)

        for key, value in data.items():
            if key not in ALLOWED_FIELDS:
                continue
            if key == "password":
                value = hash_password(value[:72])
                setattr(user, "hashed_password", value)
            else:
                setattr(user, key, value)

        updated_user = await self.user_repository.update(user)
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        await self.user_repository.delete(user)
