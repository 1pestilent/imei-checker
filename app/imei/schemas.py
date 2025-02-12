from pydantic import BaseModel, RootModel, Field
from typing import List, Optional

class CheckSchema(BaseModel):
    service_id: int 
    device_id: str = Field(min_length=8, max_length=15)
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