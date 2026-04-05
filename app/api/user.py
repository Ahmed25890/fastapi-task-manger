from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.session import  get_db
from app.db import models

from app.services.authentication import  auth
from app.services import user_service

from app.models.user import UserLogin, UserResponse, DelUser, UserUpdate , CreateUser
from app.models.token import Token

from app.services.authentication.get_current_user_file import get_current_user
from app.services.rate_limiter import limiter


router = APIRouter()

# note 
@limiter.limit("10/minute")
@router.post("/login",response_model=Token)
async def login(request: Request, data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await user_service.GetUserByEmailSafe(db, data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not await auth.verifyHash(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = await auth.create_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# get user id
@limiter.limit("10/minute")
@router.get("/user/{user_id}",response_model=UserResponse)
async def get_user( request:Request,user_id:int, db: AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):

    return await user_service.GetUser(db, user_id== current_user.user_id)

# get user by email 
@limiter.limit("10/minute")
@router.get("/user",response_model=UserResponse)
async def get_user_by_email( request:Request,email:str, db:AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return await user_service.GetUserByEmailSafe(db, email)

# create user
@limiter.limit("10/minute")
@router.post("/user",response_model=UserResponse) 
async def create_user( request:Request,user: CreateUser, db: AsyncSession = Depends(get_db)):
    return await user_service.CreateUserDB(db, user)

# update user 
@limiter.limit("10/minute")
@router.put("/user",response_model=UserResponse)
async def update_user( request:Request,user:UserUpdate, db: AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return await user_service.UpdateUser(db,current_user.user_id ,user)
# del user 
@limiter.limit("10/minute")
@router.delete("/user",response_model=UserResponse)
async def del_user_main( request:Request,user: DelUser, db: AsyncSession = Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    return await user_service.DelUserDB(db, current_user.user_id)
