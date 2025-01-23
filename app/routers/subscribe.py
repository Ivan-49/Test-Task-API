from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import fetch_product_details
from typing import Dict, Any

router = APIRouter()


async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.get("/api/v1/subscribe/{artikul}", response_model=schemas.Product)
async def read_product_by_artikul(artikul: str, session: AsyncSession = Depends(get_db)):
    try:
      product_details = await fetch_product_details(artikul)
      return product_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")