from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from .category import CategoryResponse

class TaskBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="The name of the task")
    description: Optional[str] = Field(..., min_length=5, max_length=255, description="A brief description of the task")
    is_active: bool = Field(default=True, description="Indicates if the task is active")
    category_id: int = Field(..., description="The ID of the category this task belongs to")

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int = Field(..., description="The unique identifier of the task")
    created_at: datetime = Field(None, description="The timestamp when the task was created")
    category: CategoryResponse = Field(..., description="The category this task belongs to")

    model_config = ConfigDict(from_attributes=True)

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse] = Field(..., description="A list of tasks")
    total: int = Field(..., description="Total number of tasks available")

    model_config = ConfigDict(from_attributes=True)
