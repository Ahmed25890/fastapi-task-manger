from fastapi import FastAPI
from app.services.rate_limiter import limiter
from app.api import tasks, user, login
from app.services.global_exception_handler_file import global_exception_handler

app = FastAPI(title="Task Manager API", version="1.0")

app.include_router(user.router, tags=["Users"])
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(login.router, tags=["Login"])

app.state.limiter = limiter
app.add_exception_handler(Exception, global_exception_handler)