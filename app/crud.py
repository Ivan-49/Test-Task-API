from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

async def get_product(db: AsyncSession, artikul: str):
    result = await db.execute(select(models.Product).filter(models.Product.artikul == artikul))
    return result.scalar_one_or_none()

async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product