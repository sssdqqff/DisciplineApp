from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from .task import TaskResponse
from .category import CategoryResponse

# Базовая схема пользователя
class UserBase(BaseModel):
    nickname: str = Field(..., min_length=2, max_length=50, description="The user's nickname")
    email: EmailStr = Field(..., description="The user's email address")
    is_active: Optional[bool] = True

# Схема для создания пользователя
class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=2, max_length=50, description="The user's nickname")
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=6, max_length=72, description="The user's password")

# Схема для ответа (без пароля)
class UserResponse(UserBase):
    id: int = Field(..., description="The unique identifier of the user")
    created_at: datetime = Field(..., description="User creation timestamp")

    model_config = ConfigDict(from_attributes=True)

# Схема для ответа с задачами и категориями
class UserWithRelationsResponse(UserResponse):
    tasks: Optional[List[TaskResponse]] = []
    categories: Optional[List[CategoryResponse]] = []

    model_config = ConfigDict(from_attributes=True)
