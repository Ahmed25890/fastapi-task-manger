from app.db import models
from app.services.authentication.auth import HashPassword
from fastapi import status, HTTPException, Request
import sqlalchemy as sq
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import GetUser, CreateUserDB, DelUser as DelUserService
from app.models.user import CreateUser, DelUser as DelUserModel
from app.services.tasks import GetAllUserTasks, DelTaskDB
from app.models.enums import Roles, TaskStatus

async def get_all_users(db: AsyncSession):
    result = await db.execute(sq.select(models.Users))
    return result.scalars().all()

async def get_user(db:AsyncSession, user_id: int):
    user = await GetUser(db, user_id)
    return user

async def add_new_admin(db: AsyncSession, admin:CreateUser ):
    hashed_password = HashPassword.create_hash(admin.password)
    admin_data = CreateUser(
        user_name=admin.user_name,
        email=admin.email,
        password=hashed_password,
        role=Roles.Admin
    )
    new_admin = await CreateUserDB(db=db, user=admin_data)
    return {"admin": new_admin.user_id, "created": "successfully"}

async def del_user(db: AsyncSession, user_id: int):
    user = await DelUserService(db, user_id)
    return {"user_deleted": "successfully", "user_id" : user.user_id}

async def get_all_user_tasks(db: AsyncSession, user_id: int): 
    tasks = await GetAllUserTasks(db, user_id)
    return tasks

async def del_all_user_tasks(db: AsyncSession, user_id: int ):
    tasks_to_delete = await GetAllUserTasks(db, user_id)
    if not tasks_to_delete:
        return {"message": f"No tasks found for user_id {user_id} to delete."}

    for task in tasks_to_delete:
        await DelTaskDB(db, task.task_id)

    return {"user_id": user_id, "tasks_deleted": len(tasks_to_delete), "message": "All user tasks deleted successfully"}

async def analysis(db: AsyncSession, admin_id: int ):
    # count all tasks in app
    all_tasks_count_result = await db.execute(sq.select(sq.func.count(models.Tasks.task_id)))
    all_tasks_count = all_tasks_count_result.scalar_one()

    # count most 10 user make tasks
    most_10_users_make_tasks_result = await db.execute(
        sq.select(models.Users.user_name, sq.func.count(models.Tasks.task_id).label("task_count"))
        .join(models.Tasks, models.Users.user_id == models.Tasks.user_id)
        .group_by(models.Users.user_id, models.Users.user_name)
        .order_by(sq.func.count(models.Tasks.task_id).desc())
        .limit(10)
    )
    most_10_users_make_tasks = most_10_users_make_tasks_result.all()

    # count all users
    all_users_count_result = await db.execute(sq.select(sq.func.count(models.Users.user_id)))
    all_users_count = all_users_count_result.scalar_one()

    # count most 10 users make a requests (assuming requests are tasks for now)
    most_10_users_make_requests_result = await db.execute(
        sq.select(models.Users.user_name, sq.func.count(models.Tasks.task_id).label("request_count"))
        .join(models.Tasks, models.Users.user_id == models.Tasks.user_id)
        .group_by(models.Users.user_id, models.Users.user_name)
        .order_by(sq.func.count(models.Tasks.task_id).desc())
        .limit(10)
    )
    most_10_users_make_requests = most_10_users_make_requests_result.all()

    # count all admins
    all_admins_count_result = await db.execute(
        sq.select(sq.func.count(models.Users.user_id)).where(models.Users.role == Roles.Admin)
    )
    all_admins_count = all_admins_count_result.scalar_one()

    # count all done tasks
    done_tasks_count_result = await db.execute(
        sq.select(sq.func.count(models.Tasks.task_id)).where(models.Tasks.task_status == TaskStatus.Done)
    )
    done_tasks_count = done_tasks_count_result.scalar_one()

    # count all todo tasks
    todo_tasks_count_result = await db.execute(
        sq.select(sq.func.count(models.Tasks.task_id)).where(models.Tasks.task_status == TaskStatus.ToDo)
    )
    todo_tasks_count = todo_tasks_count_result.scalar_one()

    # count all in_progress tasks
    in_progress_tasks_count_result = await db.execute(
        sq.select(sq.func.count(models.Tasks.task_id)).where(models.Tasks.task_status == TaskStatus.InProgress)
    )
    in_progress_tasks_count = in_progress_tasks_count_result.scalar_one()

    return {
        "all_tasks_count": all_tasks_count,
        "most_10_users_make_tasks": [{"user_name": user_name, "task_count": task_count} for user_name, task_count in most_10_users_make_tasks],
        "all_users_count": all_users_count,
        "most_10_users_make_requests": [{"user_name": user_name, "request_count": request_count} for user_name, request_count in most_10_users_make_requests],
        "all_admins_count": all_admins_count,
        "done_tasks_count": done_tasks_count,
        "todo_tasks_count": todo_tasks_count,
        "in_progress_tasks_count": in_progress_tasks_count,
    }