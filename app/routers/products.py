from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..schemas import Article, Product
from ..utils.fetch_utils import fetch_product_details
from ..utils.data_base_communications.add_to_items import add_to_items
from ..utils.database_utils import get_db

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/api/v1/products", response_model=None)
async def get_products(article: Article, session: AsyncSession = Depends(get_db)):
    result = await fetch_product_details(article.article)

    try:

        if not isinstance(result.get("artikul"), str):
            result["artikul"] = str(result.get("artikul"))
        result["date_time"] = result["date_time"].replace(tzinfo=None)

        details = Product(**result)
        details = details.model_dump()

        return await add_to_items(details, session=session)

    except Exception as e:
        logger.exception(f"Error processing product: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
