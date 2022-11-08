# Create the Pydantic models
from typing import List, Union, Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    body: Optional[str] = None
    price: float
    category: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: str
    body: Optional[str] = None
    price: float


class ProductImageUpload(BaseModel):
    images: Optional[str] = None


class ProductDetail(ProductBase):
    product_id: int

    class Config:
        orm_mode = True



