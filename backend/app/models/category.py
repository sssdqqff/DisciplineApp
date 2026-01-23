import re

from sqlalchemy import Mapped, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from backend.app.models.task import Task
from ..database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="category")

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active})"