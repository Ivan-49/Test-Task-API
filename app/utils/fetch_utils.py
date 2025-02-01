from datetime import datetime, timezone
import aiohttp
from fastapi import HTTPException
from typing import Optional, Dict, Any
import logging


logger = logging.getLogger(__name__)





async def fetch_product_details(artikul: str) -> Optional[Dict[str, Any]]:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&sp=30&nm={artikul}"
    try:
        logger.info(f"Fetching product details for artikul: {artikul}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    products = data.get("data", {}).get("products", [])
                    if products:
                        product = products[0]
                        if not product:
                            logger.error(f"Product is None for artikul: {artikul}")
                            raise HTTPException(
                                status_code=404,
                                detail="Product not found in Wildberries response",
                            )

                        # Строгие проверки наличия полей
                        name = product.get("name")
                        if not name:
                            logger.error(f"Missing 'name' field for artikul: {artikul}")
                            raise HTTPException(
                                status_code=500,
                                detail="Missing 'name' field in Wildberries response",
                            )
                        price_u = product.get("salePriceU")
                        if price_u is None:
                            logger.error(
                                f"Missing 'salePriceU' field for artikul: {artikul}"
                            )
                            raise HTTPException(
                                status_code=500,
                                detail="Missing 'salePriceU' field in Wildberries response",
                            )
                        price = price_u / 100
                        rating = product.get("rating", 0.0)  # Значение по умолчанию 0.0

                        sizes = product.get("sizes", [])
                        total_quantity = 0
                        for size in sizes:
                            total_quantity += sum(
                                item.get("qty", 0) for item in size.get("stocks", [])
                            )

                        utc_datetime = datetime.now(timezone.utc)  # Текущее UTC время
                        logger.info(
                            f"Successfully fetched product details for artikul: {artikul}"
                        )
                        return {
                            "name": name,
                            "article": artikul,
                            "price": price,
                            "rating": rating,
                            "total_quantity": total_quantity,
                            "datetime": utc_datetime,
                        }
                    else:
                        logger.warning(
                            f"Product not found on Wildberries for artikul: {artikul}"
                        )
                        raise HTTPException(
                            status_code=404, detail="Product not found on Wildberries"
                        )
                else:
                    logger.error(
                        f"Wildberries API request failed with status code {response.status} for artikul: {artikul}"
                    )
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Wildberries API request failed with status code {response.status}",
                    )
    except aiohttp.ClientError as e:
        logger.error(f"Error connecting to Wildberries API for artikul {artikul}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error connecting to Wildberries API: {e}"
        )
    except (KeyError, IndexError, TypeError) as e:
        logger.error(
            f"Error parsing Wildberries API response for artikul {artikul}: {e}"
        )
        raise HTTPException(
            status_code=500, detail=f"Error parsing Wildberries API response: {e}"
        )
    except HTTPException as e:
        # Пробрасываем HTTPException как есть
        raise e
    except Exception as e:
        logger.exception(
            f"Unexpected error fetching product details for artikul {artikul}: {e}"
        )
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

