from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
async def global_exception_handler(request:Request, exc: Exception):
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )