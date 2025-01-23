from fastapi import APIRouter, Depends, HTTPException
from app import crud, schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.post("/api/v1/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, session: AsyncSession = Depends(get_db)):
    db_product = await crud.create_product(session, product)
    return db_product