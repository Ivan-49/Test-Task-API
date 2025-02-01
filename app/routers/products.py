from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DataError, ProgrammingError, OperationalError
import datetime

from ..schemas import Product, ProductDetail
from ..utils.fetch_utils import fetch_product_details
from ..models import Item
from ..database import get_db

router = APIRouter()


@router.post("/api/v1/products/", response_model=None)
async def create_product(product: Product, db: AsyncSession = Depends(get_db)):
    try:
        result = await fetch_product_details(product.article)

        # Преобразование строки в datetime объект, если необходимо.
        if isinstance(result.get("datetime"), str):
            try:
                result["datetime"] = datetime.fromisoformat(result["datetime"])
            except ValueError as e:
                await db.rollback()
                raise HTTPException(
                    status_code=400, detail=f"Invalid datetime format: {e}"
                )

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

        db.add(item)
        await db.commit()
        # await db.refresh(item)

        return {
            "message": "Product created successfully"
        }  # или возвращайте id, например
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=409, detail=f"Database integrity error: {e}"
        )  # Конфликт
    except DataError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Data error: {e}")  # Плохие данные
    except ProgrammingError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Programming error: {e}"
        )  # Ошибка запроса
    except OperationalError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database connection error: {e}"
        )  # Проблема с БД
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
