from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Асинхронный engine
async_engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для отладки

# Сессия для асинхронной работы
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()



async def get_db():
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session
