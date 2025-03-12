from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


async def create_tables():
    """Асинхронно создает таблицы в базе данных"""
    logger.info("Creating tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tables created successfully.")


# Запускаем создание таблиц при запуске приложения (асинхронно)
async def main():
    try:
        await create_tables()
    except Exception as e:
        logger.error(f"Error creating tables: {e}")


if __name__ == "__main__":
    asyncio.run(main())
