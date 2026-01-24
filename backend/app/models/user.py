from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task
    from .category import Category

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nickname: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="user")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")