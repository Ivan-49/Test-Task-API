from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    artikul: int
    rating: Optional[float] = None

class Product(BaseModel):
    id: int
    name: str
    price: float
    artikul: int
    rating: Optional[float] = None

class SubscribeCreate(BaseModel):
    product_id: int
    email: str

class Subscribe(BaseModel):
    id: int
    product_id: int
    email: str