from sqlalchemy.orm import Session
from models.user import CreateUser
from db import  models
from authentication import auth
from fastapi import status, HTTPException
import sqlalchemy as sq
from user_service import GetUserByEmailSafe

def CreateUserDB(db:Session, user: CreateUser):
    check = GetUserByEmailSafe(db, user.email)
    if check:
        raise HTTPException(status_code=400, detail="this email was used")
    new_user =models.Users(
        user_name = user.user_name,
        email = user.email,
        password = auth.HashPassword(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
