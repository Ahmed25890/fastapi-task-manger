from models import user
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from db import session
from .authentication import auth
from user_service import GetUserByEmailSafe


def login(data: user.UserLogin, db: Session = Depends(session.get_db)):
    user = GetUserByEmailSafe(db, data.email)
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


