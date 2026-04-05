from app.db.models import user
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.db import session
from app.services.authentication import auth
from app.services.user_service import GetUserByEmailSafe
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cache import get_cache, set_cache
async def login(data: user.UserLogin, db: AsyncSession = Depends(session.get_db)):
    user = await GetUserByEmailSafe(db, data.email)
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
    cached_key = f"user: {data.email}"
    cached_user = await get_cache(cached_key)
    if cached_user:
        user_obj = cached_user
    else:
        user_obj = await GetUserByEmailSafe(db, data.email)
        if user_obj:
            await set_cache(cached_key, user_obj)
    token =  auth.create_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
