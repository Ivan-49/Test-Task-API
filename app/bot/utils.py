import aiohttp
from fastapi import HTTPException
import app.schemas as schemas
async def fetch_product_details(artikul: str):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&sp=30&nm={artikul}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                products = data.get("data", {}).get("products", [])
                if products:
                    product = products[0]
                    sizes = product.get("sizes", [])
                    stocks = sizes[0].get("stocks", 0) if sizes else 0 #Обработка случая отсутствия sizes
                    return schemas.Product(
                        name=product.get("name", ""),  # Предотвращение ошибок при отсутствии name
                        artikul=artikul,
                        price=product.get("salePriceU", 0) / 100, # Предотвращение ошибок при отсутствии salePriceU
                        rating=product.get("rating", 0.0),  # Предотвращение ошибок при отсутствии rating
                        total_quantity=stocks #Предотвращение ошибки при отсутствии stocks
                    )
                else:
                    raise HTTPException(status_code=404, detail="Product not found on Wildberries")
            else:
                raise HTTPException(status_code=response.status, detail=f"Wildberries API request failed with status code {response.status}")
