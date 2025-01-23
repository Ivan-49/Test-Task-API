from fastapi import APIRouter, Depends, HTTPException
from app import crud, schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import fetch_product_details

router = APIRouter()


async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.get("/api/v1/subscribe/{artikul}", response_model=schemas.Product)
async def read_product_by_artikul(artikul: str, session: AsyncSession = Depends(get_db)):
    product_details = await fetch_product_details(artikul)
    if product_details is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_details