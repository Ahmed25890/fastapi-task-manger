from fastapi import FastAPI
from app.db import session
from app.services import login , register, user_service
from app.services import tasks as task_service
from app.services.authentication import auth , get_current_user_file
from app.services.rate_limiter import Limiter
from app.api import tasks , user
app = FastAPI(title="Task Manager API", version="1.0")

app.include_router(user.router,
                   prefix="user/",
                   tags=["Users"])
app.include_router(tasks.router,
                   prefix="tasks/",
                   tags=["tasks/"])