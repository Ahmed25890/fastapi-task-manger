from sqlalchemy.orm import Session
from app.models import tasks, user  
from app.db import models, session  
from app.services.authentication import auth , get_current_user_file
from fastapi import status, HTTPException, Request
import sqlalchemy as sq
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.rate_limiter import limiter
async def GetTask(db:AsyncSession, task_id:int):
    result = await db.execute(sq.select(models.Tasks).where(models.Tasks.task_id == task_id))
    get_task = result.scalar_one_or_none()
    if get_task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return get_task
async def GetTaskByTitle(db: AsyncSession, TaskTitle:str):
    result = await db.execute(sq.select(models.Tasks).where(models.Tasks.title == TaskTitle))
    get_task = result.scalar_one_or_none()
    if get_task is None:
        raise HTTPException(status_code=404, detail="task not found ")
    return get_task
async def GetAllUserTasks(db: AsyncSession, user_id: int):
    result = await db.execute(sq.select(models.Tasks).where(models.Tasks.user_id == user_id))
    return result.scalars().all()
# def CreateTaskDB(db:Session, task: CreateTask, user_id: int):
#     task_create = model.Tasks(
#     title       = task.title,
#     description = task.description,
#     completed   = task.completed,
#     due_date    = task.due_date,
#     priority    = task.priority,
#     user_id     = user_id,
#     Task_status = task.task_status
# )
#     db.add(task_create)
#     db.commit()
#     db.refresh(task_create)
#     return task_create
### this write with chat gpt 
async def CreateTaskDB(db: AsyncSession, task: tasks.CreateTask, user_id: int):
    task_create = models.Tasks(
        title       = task.title,
        description = task.description,
        completed   = task.completed,
        due_date    = task.due_date,
        priority    = task.priority,
        user_id     = user_id,       
        task_status = task.task_status
    )
    db.add(task_create)
    await db.commit()
    await db.refresh(task_create)
    return task_create
##### 
async def UpdateTaskDB(db:AsyncSession, task_id:int, task: tasks.UpdateTask):
    edit_task = await GetTask(db, task_id)
    edit_task.title = task.title
    edit_task.description = task.description
    edit_task.completed = task.completed
    edit_task.due_date = task.due_date
    edit_task.priority = task.priority
    edit_task.task_status = task.task_status
    await db.commit()
    await db.refresh(edit_task) 
    return edit_task

async def DelTaskDB(db:AsyncSession, task_id: int):
    del_task = await GetTask(db, task_id)
    db.delete(del_task)
    await db.commit()
    task_data = {
        "id": task_id
    }
    return task_data