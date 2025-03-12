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
                        artikul = product.get("id")
                        name = product.get("name")
                        standart_price = product.get("priceU") / 100
                        sell_price = product.get("salePriceU") / 100
                        rating = product.get("rating", 0.0)
                        utc_datetime = datetime.now(timezone.utc)
                        sizes = product.get("sizes", [])
                        total_quantity = 0
                        for size in sizes:
                            total_quantity += sum(
                                item.get("qty", 0) for item in size.get("stocks", [])
                            )

                        return {
                            "artikul": str(artikul),
                            "name": str(name),
                            "standart_price": float(standart_price),
                            "sell_price": float(sell_price),
                            "total_quantity": int(total_quantity),
                            "date_time": utc_datetime,
                            "rating": float(rating),
                        }

    except Exception as e:
        print(e)


async def fetch_gpt(CHAD_API_KEY, request, condition: str = ""):
    request_json = {"message": f"{condition} {request}", "api_key": CHAD_API_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://ask.chadgpt.ru/api/public/gpt-4o-mini", json=request_json
        ) as response:
            logger.error("response.status: " + str(response.status))
            logger.error("начался запрос gpt")
            if response.status != 200:
                logger.error(f"Ошибка! Код http-ответа: {response.status}")
                return
            resp_json = await response.json()

            if resp_json["is_success"]:
                resp_msg = resp_json["response"]
                used_words = resp_json["used_words_count"]
                return resp_msg

            else:
                error = resp_json["error_message"]
                logger.error(f"Ошибка! {error}")
            logger.error("response.status: " + str(response.status))
            logger.error("закончился запрос gpt")
