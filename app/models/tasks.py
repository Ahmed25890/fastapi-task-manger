from pydantic import BaseModel, Field, ConfigDict, field_validator
from .enums import Priority, TaskStatus
from typing import Optional
from datetime import date
import re
# tasks

class TaskBase(BaseModel):
    model_config = ConfigDict(
    from_attributes=True,
    populate_by_name=True
)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = Field(False)
    start_date: Optional[date]  = Field(None)
    due_date: Optional[date] = Field(None)
    priority: Optional[Priority] = Field(Priority.medium)
    task_status: Optional[TaskStatus] = Field(TaskStatus.ToDo)
   
    @field_validator("description")
    @classmethod
    def val_description(cls, x:Optional[str]):
        if x is None: 
            raise ValueError("")
        x = x.strip()
        final = re.sub(" ", "_", x)
        return final
   
    @field_validator("due_date")
    @classmethod
    def val_due_date(cls, due, values):
        start = values.get("start_date")
        if start is None:
            return start
        if start and due and due < start:
            raise ValueError("due_date must be after start_date")

        return due  
     
    @field_validator("start_date")
    @classmethod 
    def val_start_date(cls, t: Optional[date]):
        if t is None: 
            return t
        if t < date.today():
            raise ValueError("date error")
        return t
class CreateTask(TaskBase):
    pass
class UpdateTask(TaskBase):
    task_id: int
class TaskResponse(CreateTask):
    model_config = ConfigDict(from_attributes=True)
    task_id: int
    user_id: int
class DelTask(BaseModel):
    task_id: int 