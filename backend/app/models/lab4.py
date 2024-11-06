from pydantic import BaseModel
from typing import Union

class Purchase(BaseModel):
    buyer_name: str
    purchase_date: str
    review: str | None = None
    delivery_service: str

class Specifications(BaseModel):
    color: str
    other_specs: dict[str, Union[str, int, float]]

class Product(BaseModel):
    name: str
    manufacturer: str
    price: float
    category: str
    specifications: Specifications
    purchases: list[Purchase] = []