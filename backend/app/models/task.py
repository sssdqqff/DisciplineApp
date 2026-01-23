import re

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from ..database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .category import Category

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    category_id: Mapped[int] = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="tasks")

    def __repr__(self) -> str:
        return f"Task(id={self.id}, name={self.name}, description={self.description}, is_active={self.is_active}, category_id={self.category_id})"
    