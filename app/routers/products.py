from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app import crud, schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.post("/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, session: AsyncSession = Depends(get_db)):
    db_product = await crud.create_product(session, product)
    return db_product

@router.get("/products", response_model=List[schemas.Product])
async def read_products(session: AsyncSession = Depends(get_db)):
    db_products = await crud.read_products(session)
    return db_products


@router.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, session: AsyncSession = Depends(get_db)):
    db_product = await crud.read_product(session, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product