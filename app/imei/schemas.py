from pydantic import BaseModel, RootModel
from typing import List

class BalanceSchema(BaseModel):
    balance: float

class ServiceItemSchema(BaseModel):
    id: int
    title: str
    price: float

class ServicesSchema(RootModel):
    root: List[ServiceItemSchema]