from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    artikul: int
    rating: Optional[float] = None

class Product(ProductCreate):
    id: int

class SubscribeCreate(BaseModel):
    product_id: int
    email: str

class Subscribe(SubscribeCreate):
    id: int