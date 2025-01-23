from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/dbname"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_sessionmaker = async_sessionmaker(engine)

Base = declarative_base()