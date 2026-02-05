from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.user import UserCreate, UserResponse
from ..services.user_services import UserService
from backend.app.dependencies.auth import get_current_user  

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.get_user_by_id(user_id)


@router.get("/nickname/{nickname}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_nickname(nickname: str, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.get_user_by_nickname(nickname)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.create_user(user)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserCreate, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")
    user_service = UserService(db)
    return await user_service.update_user(user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    user_service = UserService(db)
    await user_service.delete_user(user_id)
    return None
