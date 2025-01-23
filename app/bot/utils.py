import aiohttp
from fastapi import HTTPException
from typing import Optional, Dict, Any

async def fetch_product_details(artikul: str) -> Optional[Dict[str, Any]]:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&sp=30&nm={artikul}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    products = data.get("data", {}).get("products", [])
                    if products:
                        product = products[0]
                        # Строгие проверки наличия полей
                        name = product.get("name")
                        if not name:
                            raise HTTPException(status_code=500, detail="Missing 'name' field in Wildberries response")
                        price_u = product.get("salePriceU")
                        if price_u is None:
                            raise HTTPException(status_code=500, detail="Missing 'salePriceU' field in Wildberries response")
                        price = price_u / 100
                        rating = product.get("rating", 0.0)  # Значение по умолчанию 0.0

                        sizes = product.get("sizes", [])
                        total_quantity = 0
                        for size in sizes:
                            total_quantity += sum(item.get("qty", 0) for item in size.get("stocks", []))
                                             
                        return {
                            "name": name,
                            "artikul": artikul,
                            "price": price,
                            "rating": rating,
                            "total_quantity": total_quantity,
                        }
                    else:
                        raise HTTPException(status_code=404, detail="Product not found on Wildberries")
                else:
                    raise HTTPException(status_code=response.status,
                                        detail=f"Wildberries API request failed with status code {response.status}")
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Wildberries API: {e}")
    except (KeyError, IndexError, TypeError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Wildberries API response: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")