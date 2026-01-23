from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.task import Task
from ..schemas.task import TaskCreate

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Task]:
        return self.db.query(Task).options(joinedload(Task.category)).all()
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).options(joinedload(Task.category)).filter(Task.id == task_id).first()
    
    def get_by_name(self, name: str) -> Optional[Task]:
        return self.db.query(Task).options(joinedload(Task.category)).filter(Task.name == name).first()
    
    def create(self, task_create: TaskCreate) -> Task:
        new_task = Task(**task_create.model_dump())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task
    
    def get_multiple_by_ids(self, task_ids: List[int]) -> List[Task]:
        return self.db.query(Task).options(joinedload(Task.category)).filter(Task.id.in_(task_ids)).all()