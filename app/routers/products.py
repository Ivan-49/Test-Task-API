from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, database
from app.utils import fetch_product_details

router = APIRouter()

async def get_db():
    async with database.SessionLocal() as session:
        yield session

@router.post("/api/v1/products", response_model=schemas.Product)
async def create_product(artikul: str, db: AsyncSession = Depends(get_db)):
    product_details = await fetch_product_details(artikul)
    if not product_details:
        raise HTTPException(status_code=404, detail="Product not found")
    product = schemas.ProductCreate(**product_details)
    return await crud.create_product(db, product)