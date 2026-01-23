from sqlalchemy.orm import Session
from typing import List, Optional

from ..repositories.task_repository import TaskRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.task import TaskCreate, TaskListResponse, TaskResponse
from fastapi import HTTPException, status

class TaskService:
    def __init__(self, db: Session):
        self.task_repository = TaskRepository(db)
        self.category_repository = CategoryRepository(db)
        self.db = db

    def get_all_tasks(self) -> List[TaskResponse]:
        tasks = self.task_repository.get_all()
        return [TaskResponse.model_validate(task) for task in tasks]

    def get_task_by_id(self, task_id: int) -> TaskResponse:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return TaskResponse.model_validate(task)
    
    def get_tasks_by_category(self, category_id: int) -> List[TaskResponse]:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        
        tasks = self.task_repository.get_by_category(category_id)
        tasks_response = [TaskResponse.model_validate(task) for task in tasks]
        return TaskListResponse(tasks=tasks_response, total=len(tasks_response)).tasks

    def create_task(self, task_create: TaskCreate) -> TaskResponse:
        category = self.category_repository.get_by_id(task_create.category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")

        existing_task = self.task_repository.get_by_name(task_create.name)
        if existing_task:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task with this name already exists")
        
        new_task = self.task_repository.create(task_create)
        return TaskResponse.model_validate(new_task)