from sqlalchemy import text
import logging

from ..utils.fetch_utils import fetch_product_details
from ..database import async_session
from ..schemas import Product
from ..utils.data_base_communications.add_to_items import add_to_items


logger = logging.getLogger(__name__)


async def tick():
    try:
        async with async_session() as db:
            request = text(
                """
SELECT artikul FROM subs
GROUP BY artikul;
"""
            )
            result = await db.execute(request)
            list_of_artikul = result.fetchall()
            for artikul in map(lambda x: x[0], list_of_artikul):
                result = await fetch_product_details(artikul)

                if not isinstance(result.get("artikul"), str):
                    result["artikul"] = str(result.get("artikul"))
                result["date_time"] = result["date_time"].replace(tzinfo=None)

                details = Product(**result)
                details = details.model_dump()
                await add_to_items(details, session=db)

    except Exception as e:
        logger.error(f"Error processing product: {e}")
