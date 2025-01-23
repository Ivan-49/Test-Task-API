from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    artikul: str
    price: float
    rating: float
    total_quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True