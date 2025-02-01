from sqlalchemy.ext.asyncio import AsyncSession
import logging
from sqlalchemy import text

from ..database import get_db

logger = logging.getLogger(__name__)





async def get_product_info(artikul: str, db: AsyncSession = get_db()):
    sql_request = text("""
    SELECT name, price, rating, total_quantity
    FROM items
    WHERE article = :artikul
    ORDER BY datetime DESC
    LIMIT 1
    """)
    async for session in db: # Получаем сессию из генератора
        result = await session.execute(sql_request, {"artikul": artikul})
        result = result.first()
        print(f'result: {result}')
        return result if result else None
    
async def add_product_to_tasks(artikul: str, db: AsyncSession = get_db()):
    sql_request = text("""
    INSERT INTO scheduled_tasks (article)
    VALUES (:artikul)
    """)
    async for session in db: # Получаем сессию из генератора
        await session.execute(sql_request, {"artikul": artikul})
        await session.commit()