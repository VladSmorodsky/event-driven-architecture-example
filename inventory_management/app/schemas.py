from typing import Annotated

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    quantity: Annotated[int, Field(ge=0)]
    price: Annotated[float, Field(ge=0)]


class ProductQuantityUpdate(BaseModel):
    id: int
    quantity: Annotated[int, Field(ge=0)]
