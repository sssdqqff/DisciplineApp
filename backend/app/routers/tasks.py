from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.task import TaskCreate, TaskResponse
from ..services.task_services import TaskService
from backend.app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_all_tasks(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    return await task_service.get_all_tasks(user_id=current_user.id)

@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    task = await task_service.get_task_by_id(task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/category/{category_id}", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks_by_category(category_id: int, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    return await task_service.get_tasks_by_category(category_id, user_id=current_user.id)

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    return await task_service.create_task(task, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: TaskCreate, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    updated_task = await task_service.update_task(task_id, task, user_id=current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or not yours")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task_service = TaskService(db)
    await task_service.delete_task(task_id, user_id=current_user.id)
    return None
