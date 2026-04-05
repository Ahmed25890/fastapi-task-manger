
from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import  get_db

from app.services.authentication import  auth
from app.services import user_service

from app.models.user import UserLogin
from app.models.token import Token

from app.services.rate_limiter import limiter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()



@limiter.limit("10/minute")
@router.post("/login", response_model=Token)
async def login( request:Request,data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await user_service.GetUserByEmailSafe(db, data.email)
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
    token =  auth.create_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
