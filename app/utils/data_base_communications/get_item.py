from sqlalchemy import text
import logging

from ...database import async_session
from ...schemas import Article

logger = logging.getLogger(__name__)

async def get_item(artikul: str, count: int):
    try:
        async with async_session() as db:
            request = text(
                """
SELECT artikul, name, standart_price, sell_price, total_quantity, datetime, rating FROM items
WHERE artikul = :artikul
ORDER BY datetime DESC;
"""
            )
            result = await db.execute(request, {"artikul": artikul})

            if count == 1:
                return result.fetchone() or None

            elif count > 1:
                resul_a = result.fetchall()
                logger.error(f"len(resul_a): {len(resul_a)}")
                return resul_a[:min(count, len(resul_a))]

            return []
        
    except Exception as e:
        logger.error(f"Error processing product: {e}")
async def get_item_by_name(name: str, count: int):
    try:
        async with async_session() as db:
            request = text(
                """
SELECT DISTINCT ON (artikul)
       artikul,
       name,
       standart_price,
       sell_price,
       total_quantity,
       datetime,
       rating,
       latest_datetime
FROM (
    SELECT artikul,
           name,
           standart_price,
           sell_price,
           total_quantity,
           datetime,
           rating,
           MAX(datetime) OVER (PARTITION BY artikul) AS latest_datetime,
           unnest(string_to_array(name, ' ')) AS word
    FROM items
    WHERE EXISTS (SELECT 1 FROM unnest(string_to_array(items.name, ' ')) AS word_check WHERE word_check % :name)
) AS subquery
ORDER BY artikul, latest_datetime DESC, datetime DESC;
"""
            )
            result = await db.execute(request, {"name": name})

            if count == 1:
                return result.fetchone() or None

            elif count > 1:
                resul_a = result.fetchall()
                logger.error(f"len(resul_a): {len(resul_a)}")
                return resul_a[:min(count, len(resul_a))]

            return []

    except Exception as e:
        logger.error(f"Error processing product: {e}")
        return []