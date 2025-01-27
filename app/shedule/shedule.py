from datetime import datetime
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy import text

from ..utils import fetch_product_details
from ..database import async_session
from ..models import Item
from ..schemas import ProductDetail


async def tick():
    try:
        async with async_session() as db:
            request = text(
                """
            SELECT article FROM scheduled_tasks
            GROUP BY article;
        """
            )
            result = await db.execute(request)
            products_with_text = result.fetchall()
            for product in products_with_text:
                try:
                    result = await fetch_product_details(product[0])
                    if not result:
                        print(f"Failed to fetch details for product: {product}")
                        continue
                    # Преобразование строки в datetime объект, если необходимо.
                    if isinstance(result.get("datetime"), str):
                        try:
                            result["datetime"] = datetime.fromisoformat(
                                result["datetime"]
                            )
                        except ValueError as e:
                            print(f"Invalid datetime format: {e}")
                            continue

                    detail = ProductDetail(**result)
                    detail = detail.model_dump()
                    # Добавление новой записи
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
                except Exception as e:
                    print(f"Error during update of product {product}: {e}")
    except Exception as e:
        print(f"Error in tick: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tick, "interval", seconds=10)
    scheduler.start()
    try:
        await asyncio.get_running_loop().create_future()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
