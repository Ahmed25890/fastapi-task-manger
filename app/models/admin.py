from pydantic import BaseModel
from typing import List

class UserTaskCount(BaseModel):
    user_name: str
    task_count: int

class UserRequestCount(BaseModel):
    user_name: str
    request_count: int

class AdminAnalysisResponse(BaseModel):
    all_tasks_count: int
    most_10_users_make_tasks: List[UserTaskCount]
    all_users_count: int
    most_10_users_make_requests: List[UserRequestCount]
    all_admins_count: int
    done_tasks_count: int
    todo_tasks_count: int
    in_progress_tasks_count: int
