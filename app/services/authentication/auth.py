from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.session import get_db

SECRET_KEY =settings.SECRET_KEY
ALGORITHM =settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def HashPassword(password: str):
    hashed = pwd_context.hash(password)
    return hashed
    
def verifyHash(password:str, hash:str):
    verify_pass =pwd_context.verify(password, hash)
    return verify_pass

def create_token(data: dict, engine_delta: Optional[timedelta]= None):
    to_encode = data.copy()
    if engine_delta:
        expire = datetime.now(timezone.utc) + engine_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

 