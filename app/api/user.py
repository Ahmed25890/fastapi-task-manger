from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.db.session import  get_db
from app.db import models

from app.services.authentication import  auth
from app.services import user_service

from app.models.user import UserLogin, UserResponse, DelUser, UserUpdate , CreateUser
from app.models.token import Token

from app.services.authentication.get_current_user_file import get_current_user


router = APIRouter()

# note 
@router.post("/login",response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.GetUserByEmailSafe(db, data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not auth.verifyHash(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.create_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# get user id
@router.get("/user/{user_id}",response_model=UserResponse)
def get_user(user_id:int, db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):

    return user_service.GetUser(db, user_id== current_user.user_id)

# get user by email 
@router.get("/user",response_model=UserResponse)
def get_user_by_email(email:str, db:Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return user_service.GetUserByEmailSafe(db, email)

# create user
@router.post("/user",response_model=UserResponse) 
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    return user_service.CreateUserDB(db, user)

# update user 
@router.put("/user",response_model=UserResponse)
def update_user(user:UserUpdate, db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return user_service.UpdateUser(db,current_user.user_id ,user)
# del user 
@router.delete("/user",response_model=UserResponse)
def del_user_main(user: DelUser, db: Session = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return user_service.DelUserDB(db, current_user.user_id)
