
from sqlalchemy.orm import Session

from models import user, tasks
from db import models
from authentication.auth import HashPassword
from fastapi import status, HTTPException
import sqlalchemy as sq


def GetUser(db: Session, user_id: int ):
    q = sq.select(models.Users).where(models.Users.user_id ==  user_id)
    user = db.execute(q).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

# def GetUserByEmail(db:Session, user_email: str):
#     user = db.query(model.Users).filter(model.Users.email == user_email).first()
#     return user
def GetUserByEmailSafe(db:Session, user_email: str): 
     user = db.query(models.Users).filter(models.Users.email == user_email).first()
     return user
def UpdateUser(db:Session, user_id: int,user: user.UserUpdate):
    get_user = GetUser(db, user_id)
    get_user.user_name = user.user_name
    get_user.email = user.email
    if user.password:
        get_user.password = HashPassword(user.password)
    db.commit()
    db.refresh(get_user)
    return get_user
def DelUserDB(db:Session, user:user.DelUser):
    get_user = GetUser(db, user.user_id)
    db.delete(get_user)
    db.commit()
    return get_user
