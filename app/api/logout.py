from fastapi import APIRouter, Request, Depends, status, HTTPException
from app.db import models
from app.services.authentication.get_current_user_file import get_current_user
from app.services.rate_limiter import limiter
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/logout", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def logout(
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    current_user: models.Users = Depends(get_current_user)
):
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1] if auth_header and " " in auth_header else None

    
    return {
        "status": "success",
        "detail": f"User {current_user.email} logged out successfully.",
        "message": "Token is now invalid on the client side. Please clear your storage."
    }