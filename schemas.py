from pydantic import BaseModel,Field
from typing import Optional


class ItemCreate(BaseModel):
    name :str = Field(min_length=2,max_length=20,examples=["tanaka"])
    email :str = Field(examples=["email@com"])


class ItemUpdate(BaseModel):
    name : Optional[str] = Field(default=None,min_length=2,max_length=20,examples=["yamada"])
    email : Optional[str] = Field(default=None,examples=["email@com"])


class ItemResponse(BaseModel):
    name :str = Field(min_length=2,max_length=20,examples=["satou"])
    email :str = Field(min_length=2,max_length=20,examples=["dafgz@com"])