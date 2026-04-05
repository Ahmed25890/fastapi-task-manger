from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from .session import Base
from datetime import datetime, timezone
from app.models.enums import TaskStatus , Priority

# add to users role 
class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    tasks = relationship("Tasks", back_populates="user")


class Tasks(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    completed = Column(Boolean, nullable=False, default=False)
    start_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    due_date = Column(DateTime, nullable=True)
    priority = Column(Enum(Priority), default=Priority.medium)
    task_status = Column(Enum(TaskStatus), default=TaskStatus.ToDo)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    user = relationship("Users", back_populates="tasks")

