from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, database
from app.utils import fetch_product_details
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

router = APIRouter()
scheduler = AsyncIOScheduler()

async def get_db():
    async with database.SessionLocal() as session:
        yield session

@router.get("/api/v1/subscribe/{artikul}", response_model=schemas.Product)
async def subscribe_product(artikul: str, db: AsyncSession = Depends(get_db)):
    product_details = await fetch_product_details(artikul)
    if not product_details:
        raise HTTPException(status_code=404, detail="Product not found")
    product = schemas.ProductCreate(**product_details)
    await crud.create_product(db, product)
    scheduler.add_job(fetch_and_update_product, IntervalTrigger(minutes=30), args=[artikul, db])
    scheduler.start()
    return product

async def fetch_and_update_product(artikul: str, db: AsyncSession):
    product_details = await fetch_product_details(artikul)
    if product_details:
        product = schemas.ProductCreate(**product_details)
        await crud.create_product(db, product)