from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from fastapi import HTTPException
import logging

from ..schemas import ProductDetail
from ..models import Item
from ..database import get_db
from .fetch_utils import fetch_product_details
logger = logging.getLogger(__name__)






async def scheduler_pars(artikul: str, data_base: AsyncSession = Depends(get_db)):

    result = await fetch_product_details(artikul)

    # Преобразование строки в datetime объект, если необходимо.
    if isinstance(result.get("datetime"), str):
        try:
            result["datetime"] = datetime.fromisoformat(result["datetime"])
        except ValueError as e:
            await data_base.rollback()
            raise HTTPException(status_code=400, detail=f"Invalid datetime format: {e}")

    detail = ProductDetail(**result)
    detail = detail.model_dump()
    item = Item(
        name=detail.get("name"),
        article=detail.get("article"),
        price=detail.get("price"),
        rating=detail.get("rating"),
        total_quantity=detail.get("total_quantity"),
        datetime=detail.get("datetime"),
    )

    data_base.add(item)
    await data_base.commit()
    await data_base.refresh(item)

    return {"message": f"Scheduled task added for {artikul} every 30 minutes"}
