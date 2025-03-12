from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ...database import get_db, async_session
from ...models import Subscribe, Item
from ...schemas import Article

logger = logging.getLogger(__name__)


async def add_to_items(item: dict, session: AsyncSession = Depends(get_db)):
    try:

        async with async_session() as session:

            item = Item(
                artikul=item["artikul"],
                name=item["name"],
                standart_price=item["standart_price"],
                sell_price=item["sell_price"],
                total_quantity=item["total_quantity"],
                datetime=item["date_time"],
                rating=item["rating"],
            )
            session.add(item)
            await session.commit()
        return "success"

    except Exception as e:
        logger.error(f"Error processing product: {e}")


async def add_to_subs(articul: str, session: AsyncSession = Depends(get_db)):
    try:
        async with async_session() as session:
            article = Subscribe(artikul=articul)
            session.add(article)
            await session.commit()
        return "sub success"

    except Exception as e:
        logger.error(f"Error processing product add to subs: {e}")
