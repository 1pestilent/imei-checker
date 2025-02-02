from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserLoginSchema(BaseModel):
    telegram_id: int
    password: str

class UserAddSchema(UserLoginSchema):
    fullname: str

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    telegram_id: int
    fullname: str
    created_at: datetime
    updated_at: datetime

class TokenSchema(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"