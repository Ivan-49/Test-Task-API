from pydantic import BaseModel, Field
from datetime import datetime as dt

# from typing import List, Optional, Any


class Product(BaseModel):

    article: str = Field(title="Article", description="The article of the product")


class ProductDetail(BaseModel):
    name: str = Field(title="Name", description="The name of the product")
    article: str = Field(title="Article", description="The article of the product")
    price: float = Field(title="Price", description="The price of the product")
    rating: float = Field(title="Rating", description="The rating of the product")
    total_quantity: int = Field(
        title="Total Quantity", description="The total quantity of the product"
    )
    datetime: dt = Field(title="Datetime", description="The datetime of the product")
