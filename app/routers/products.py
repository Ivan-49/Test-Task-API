from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import fetch_product_details
from sqlalchemy.exc import IntegrityError
from typing import Dict, Any

router = APIRouter()

async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.post("/api/v1/products", response_model=schemas.Product, status_code=201)
async def create_product(product: schemas.ProductCreate, session: AsyncSession = Depends(get_db)):
    try:
        product_details = await fetch_product_details(product.artikul)
        return product_details
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Product with artikul {product.artikul} already exists.")
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Internal server error: {e}")