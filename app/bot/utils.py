import aiohttp
from fastapi import HTTPException
from app import schemas
from typing import Optional


async def fetch_product_details(artikul: str) -> Optional[schemas.Product]:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&sp=30&nm={artikul}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    products = data.get("data", {}).get("products", [])
                    if products:
                        product = products[0]
                        sizes = product.get("sizes", [])
                        stocks = sizes[0].get("stocks", 0) if sizes else 0
                        return schemas.Product(
                            name=product.get("name", ""),
                            artikul=artikul,
                            price=product.get("salePriceU", 0) / 100,
                            rating=product.get("rating", 0.0),
                            total_quantity=stocks,
                        )
                    else:
                        raise HTTPException(status_code=404, detail="Product not found on Wildberries")
                else:
                  raise HTTPException(status_code=response.status, detail=f"Wildberries API request failed with status code {response.status}")

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Error while connecting to Wildberries API: {e}")
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Internal server error: {e}")