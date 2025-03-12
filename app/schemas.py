from pydantic import BaseModel, Field
from datetime import datetime


class Article(BaseModel):

    article: str = Field(title="Article", description="Article")


class Product(BaseModel):
    artikul: str = Field(title="Artikul", description="Artikul")
    name: str = Field(title="Name", description="Name")
    standart_price: float = Field(title="Standart Price", description="Standart Price")
    sell_price: float = Field(title="Sell Price", description="Sell Price")
    total_quantity: int = Field(title="Total Quantity", description="Total Quantity")
    date_time: datetime = Field(title="Datetime", description="Datetime")
    rating: float = Field(title="Rating", description="Rating")
