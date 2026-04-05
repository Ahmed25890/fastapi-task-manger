from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationInfo
from .enums import Priority, TaskStatus
from typing import Optional
from datetime import datetime, date
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
    start_date: Optional[datetime]  = None
    due_date: Optional[datetime] = Field(None)
    priority: Optional[Priority] = Field(Priority.medium)
    task_status: Optional[TaskStatus] = Field(TaskStatus.ToDo)
   
    @field_validator("description")
    @classmethod
    def val_description(cls, v: Optional[str]):
        if v is None:
            return v
        v = v.strip()
        final = re.sub(r"\s+", "_", v)
        return final
   
    @field_validator("due_date")
    @classmethod
    def val_due_date(cls, v: Optional[datetime], info: ValidationInfo):
        start = info.data.get("start_date")
        if v and start and v < start:
            raise ValueError("due_date must be after start_date")
        return v
     
    @field_validator("start_date")
    @classmethod 
    def val_start_date(cls, v: Optional[datetime]):
        if v is None: 
            return v
        if v.date() < date.today():
            raise ValueError("date error")
        return v
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