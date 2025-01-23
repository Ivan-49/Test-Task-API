from pydantic import BaseModel

class ProductCreate(BaseModel):
    artikul: str

class Product(BaseModel):
    name: str
    price: float
    artikul: str
    rating: float
    total_quantity: int