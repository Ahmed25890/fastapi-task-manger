
from app.models import user
from app.db import models
from app.services.authentication.auth import HashPassword
from fastapi import status, HTTPException, Request
import sqlalchemy as sq
from sqlalchemy.ext.asyncio import AsyncSession

async def CreateUserDB(db:AsyncSession, user: user.CreateUser):
    check = await GetUserByEmailSafe(db, user.email)
    if check:
        raise HTTPException(status_code=400, detail="this email was used")
    new_user =models.Users(
        user_name = user.user_name,
        email = user.email,
        password = await HashPassword(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def GetUser(db: AsyncSession, user_id: int):
    q = sq.select(models.Users).where(models.Users.user_id ==  user_id)
    user = db.execute(q).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

# def GetUserByEmail(db:Session, user_email: str):
#     user = db.query(model.Users).filter(model.Users.email == user_email).first()
#     return user
async def GetUserByEmailSafe(db:AsyncSession, user_email: str): 
     user = db.query(models.Users).filter(models.Users.email == user_email).first()
     return user
async def UpdateUser(db:AsyncSession, user_id: int,user: user.UserUpdate):
    get_user = await GetUser(db, user_id)
    if get_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    update_data = user.model_dump(exclude_unset=True)
    # get_user.user_name = user.user_name
    # get_user.email = user.email
    for key, value in update_data.items():
        setattr(get_user, key, value)
    if user.password:
        get_user.password = await HashPassword(user.password)
    await db.commit()
    await db.refresh(get_user)
    return get_user
async def DelUserDB(db:AsyncSession, user:user.DelUser):
    get_user = await GetUser(db, user.user_id)
    if get_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(get_user)
    await db.commit()
    return {"message": "user deleted successfully" , "user_id": user.user_id}
