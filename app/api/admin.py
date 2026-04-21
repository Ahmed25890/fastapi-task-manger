from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.session import  get_db
from app.db import models

from app.services import admin as admin_service
from app.models.user import UserResponse, CreateUser
from app.models.admin import AdminAnalysisResponse
from app.models.tasks import TaskResponse
from app.models.enums import Roles

from app.services.authentication.get_current_user_file import get_current_user
from app.services.rate_limiter import limiter
from typing import List

router = APIRouter(prefix="/admin", dependencies=[Depends(get_current_user)])

async def check_admin_role(user: models.Users = Depends(get_current_user)):
    if user.role != Roles.Admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access admin resources"
        )
    return user

@router.get("/users", response_model=List[UserResponse])
@limiter.limit("10/minute")
async def get_all_users(request: Request, db: AsyncSession = Depends(get_db), admin=Depends(check_admin_role)):
    return await admin_service.get_all_users(db)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(check_admin_role)):
    return await admin_service.get_user(db, user_id)

@router.post("/new-admin", status_code=status.HTTP_201_CREATED)
async def create_admin(admin_data: CreateUser, db: AsyncSession = Depends(get_db), admin=Depends(check_admin_role)):
    return await admin_service.add_new_admin(db, admin_data)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(check_admin_role)):
    return await admin_service.del_user(db, user_id)

@router.get("/users/{user_id}/tasks", response_model=List[TaskResponse])
async def get_user_tasks(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(check_admin_role)):
    return await admin_service.get_all_user_tasks(db, user_id)

@router.delete("/users/{user_id}/tasks")
async def delete_all_user_tasks(user_id: int, db: AsyncSession = Depends(get_db), admin=Depends(check_admin_role)):
    return await admin_service.del_all_user_tasks(db, user_id)

@router.get("/analysis", response_model=AdminAnalysisResponse)
async def get_system_analysis(db: AsyncSession = Depends(get_db), admin: models.Users = Depends(check_admin_role)):
    return await admin_service.analysis(db, admin.user_id)
