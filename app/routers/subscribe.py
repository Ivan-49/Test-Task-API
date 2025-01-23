from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app import crud, schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.post("/subscribe", response_model=schemas.Subscribe)
async def create_subscribe(subscribe: schemas.SubscribeCreate, session: AsyncSession = Depends(get_db)):
    db_subscribe = await crud.create_subscribe(session, subscribe)
    return db_subscribe


@router.get("/subscribe", response_model=List[schemas.Subscribe])
async def read_subscribes(session: AsyncSession = Depends(get_db)):
    db_subscribe = await crud.read_subscribes(session)
    return db_subscribe


@router.get("/subscribe/{subscribe_id}", response_model=schemas.Subscribe)
async def read_subscribe(subscribe_id: int, session: AsyncSession = Depends(get_db)):
    db_subscribe = await crud.read_subscribe(session, subscribe_id)
    if db_subscribe is None:
        raise HTTPException(status_code=404, detail="Subscribe not found")
    return db_subscribe