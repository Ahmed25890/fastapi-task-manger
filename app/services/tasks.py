from sqlalchemy.orm import Session
from app.models import tasks, user  
from app.db import models, session  
from app.services.authentication import auth , get_current_user_file
from fastapi import status, HTTPException
import sqlalchemy as sq


def GetTask(db:Session, task_id:int):
    get_task = db.query(models.Tasks).filter(models.Tasks.task_id == task_id).first()
    if get_task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return get_task
def GetTaskByTitle(db: Session, TaskTitle:str):
    get_task = db.query(models.Tasks).filter(models.Tasks.title == TaskTitle).first()
    if get_task is None:
        raise HTTPException(status_code=404, detail="task not found ")
    return get_task
def GetAllUserTasks(db:Session, user_id: int):
    return db.query(models.Tasks).filter(models.Tasks.user_id == user_id).all()
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
def CreateTaskDB(db: Session, task: tasks.CreateTask, user_id: int):
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
    db.commit()
    db.refresh(task_create)
    return task_create
##### 
def UpdateTaskDB(db:Session, task_id:int, task: tasks.UpdateTask):
    edit_task = GetTask(db, task_id)
    edit_task.title = task.title
    edit_task.description = task.description
    edit_task.completed = task.completed
    edit_task.due_date = task.due_date
    edit_task.priority = task.priority
    edit_task.Task_status = task.task_status
    db.commit()
    db.refresh(edit_task) 
    return edit_task

def DelTaskDB(db:Session, task_id: int):
    del_task = GetTask(db, task_id)
    db.delete(del_task)
    db.commit()
    task_data = {
        "id": task_id
    }
    return task_data