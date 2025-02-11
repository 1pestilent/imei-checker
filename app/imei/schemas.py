from pydantic import BaseModel, RootModel
from typing import List, Optional

class BalanceSchema(BaseModel):
    balance: float

class ItemForServicesSchema(BaseModel):
    id: int
    title: str
    price: float

class ServiceItemSchema(ItemForServicesSchema):
    properties: Optional[dict] = None
    
class ServicesSchema(RootModel):
    root: List[ItemForServicesSchema]