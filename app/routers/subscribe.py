from fastapi import APIRouter, Depends, HTTPException
from app import crud, schemas
from app.database import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def get_db():
    async with async_sessionmaker() as session:
        yield session

@router.get("/api/v1/subscribe/{artikul}", response_model=schemas.Product)
async def read_product_by_artikul(artikul: int, session: AsyncSession = Depends(get_db)):
    db_product = await crud.read_product_by_artikul(session, artikul)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product