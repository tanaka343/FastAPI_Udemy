from pydantic import BaseModel,Field
from typing import Optional
from enum import Enum

class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"

class ItemCreate(BaseModel):
    name: str = Field(min_length=2,max_length=20,examples=["PC"])
    price: int = Field(gt=0,examples=[10000])
    description: Optional[str] = Field(None,examples=["美品です"])
    status: ItemStatus = Field(examples=["ON_SALE"])

# class ItemUpdate(BaseModel):



