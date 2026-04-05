from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app.db.session import  get_db
from app.db import models
from app.services import tasks

from app.services.authentication import  auth

from app.models.tasks import TaskResponse, CreateTask, UpdateTask, DelTask
from app.services.authentication.get_current_user_file import get_current_user
from app.services.rate_limiter import limiter
from sqlalchemy.ext.asyncio import AsyncSession 
router = APIRouter()

# get task 
@limiter.limit("10/minute")
@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task( request:Request, task_id: int, db: AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
   return await tasks.GetTask(db, task_id)
# get all user tasks
@limiter.limit("10/minute")
@router.get("/tasks")
async def get_all_tasks( request:Request,db:AsyncSession = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    return await tasks.GetAllUserTasks(db, current_user.user_id)
# get task by title
@limiter.limit("10/minute")
@router.get("/task", response_model=TaskResponse)
async def get_task_by_tittle( request:Request,title: str, db:AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return await tasks.GetTaskByTitle(db, title)
# create task 
@limiter.limit("10/minute")
@router.post("/task", response_model=TaskResponse)
async def create_task( request:Request,task: CreateTask, db: AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return await tasks.CreateTaskDB(db, task, user_id=current_user.user_id)
    
# update task 
@limiter.limit("10/minute")
@router.put("/task{task_id}", response_model=TaskResponse)
async def update_task( request:Request, task_id: int,task: UpdateTask, db: AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    db_task = await tasks.GetTask(db, task_id)
    if db_task.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="auth error")
    
    return await tasks.UpdateTaskDB(db,task_id=task_id, task=task)

# del task 
@limiter.limit("10/minute")
@router.delete("/task", response_model=TaskResponse)
async def delete_task( request:Request,task: DelTask, db:AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    db_task = await tasks.GetTask(db, task.task_id)
    if db_task.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="auth error")
    return await tasks.DelTaskDB(db, task_id = task.task_id)
