from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(
    # autocommit=False,
    # autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
    # future=True
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as db:
        yield db