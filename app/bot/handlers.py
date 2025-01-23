from app.utils import fetch_product_details
async def get_product_info(artikul: str):
    try:
        product_details = await fetch_product_details(artikul)
        if product_details is None:
            return None
        return product_details
    except Exception as e:
        print(f"Error in get_product_info: {e}")
        return None

