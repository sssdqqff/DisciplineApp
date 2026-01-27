from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.task import TaskCreate, TaskResponse
from ..services.task_services import TaskService
from ..services.auth_services import AuthService
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# OAuth2 для получения текущего пользователя
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.get_current_user(token)

@router.get("", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.get_all_tasks(user_id=current_user.id)

@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id(task_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/category/{category_id}", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks_by_category(category_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.get_tasks_by_category(category_id, user_id=current_user.id)

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    return task_service.create_task(task, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    updated_task = task_service.update_task(task_id, task, user_id=current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or not yours")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task_service.delete_task(task_id, user_id=current_user.id)
    return None
