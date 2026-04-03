from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.db.session import  get_db
from app.db import models
from app.services import tasks

from app.services.authentication import  auth

from app.models.tasks import TaskResponse, CreateTask, UpdateTask, DelTask
from app.services.authentication.auth import get_current_user

router = APIRouter()

# get task 
@router.get("/task/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
   return  tasks.GetTask(db, task_id)
# get all user tasks
@router.get("/tasks")
def get_all_tasks(db:Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    return tasks.GetAllUserTasks(db, current_user.user_id)
# get task by title  
@router.get("/task", response_model=TaskResponse)
def get_task_by_tittle(title: str, db:Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return  tasks.GetTaskByTitle(db, title)
# create task 
@router.post("/task", response_model=TaskResponse)
def create_task(task: CreateTask, db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return  tasks.CreateTaskDB(db, task, user_id=current_user.user_id)
    
# update task 
@router.put("/task{task_id}", response_model=TaskResponse)
def update_task(task_id: int,task: UpdateTask, db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    db_task = tasks.GetTask(db, task_id)
    if db_task.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="auth error")
    
    return tasks.UpdateTaskDB(db,task_id=task_id, task=task)

# del task 
@router.delete("/task", response_model=TaskResponse)
def delete_task(task: DelTask, db:Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    db_task = tasks.GetTask(db, task.task_id)
    if db_task.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="auth error")
    return  tasks.DelTaskDB(db, task_id = task.task_id)
