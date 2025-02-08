from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserLoginSchema(BaseModel):
    telegram_id: int
    password: str

class UserAddSchema(UserLoginSchema):
    fullname: str

class SafelyUserSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    telegram_id: int
    fullname: str
    created_at: datetime
    updated_at: datetime

class UserSchema(SafelyUserSchema):
    password: bytes
