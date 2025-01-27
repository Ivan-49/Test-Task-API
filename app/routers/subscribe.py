"""
сделать так что бы подпииска работала следуюшим образом:

    1. Пользователь создает подписку на продукт через API (GET /api/v1/subscribe/{product_id})
    2. Пользователь получает информацию о продукте через API (GET /api/v1/products/{product_id})
    3. Артикуль на который пользователь подписался, добавляется в таблицу scheduled_tasks
    4. Асинхронный планировщик, каждые пол часа делает следующее:
        1. Вытаскивает из БД все артикули из таблицы scheduled_tasks
        2. Получает инфорцию о каждом из продуктов через функцию fetch_product_details
        3. Добавляет информацию о продукте в таблицу items
        
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import Product
from ..models import ScheduledTask
from ..database import get_db

router = APIRouter()


@router.get("/api/v1/subscribe/product", response_model=None)
async def create_product(product: str, db: AsyncSession = Depends(get_db)):
    product = Product(article=product)
    item_article = ScheduledTask(article=product.article)

    db.add(item_article)
    await db.commit()
    return {"message": "Product created successfully"}
