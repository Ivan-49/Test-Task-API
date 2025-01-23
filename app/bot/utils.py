import aiohttp

async def fetch_product_details(artikul: str):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&sp=30&nm={artikul}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                product_info = {
                    "name": data.get("data", {}).get("products", [{}])[0].get("name"),
                    "artikul": artikul,
                    "price": data.get("data", {}).get("products", [{}])[0].get("salePriceU") / 100,
                    "rating": data.get("data", {}).get("products", [{}])[0].get("rating"),
                    "total_quantity": data.get("data", {}).get("products", [{}])[0].get("sizes", [{}])[0].get("stocks", 0)
                }
                return product_info
            else:
                return None