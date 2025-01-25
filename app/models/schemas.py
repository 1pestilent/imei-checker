from pydantic import BaseModel

class UserAddSchema(BaseModel):
    telegram_id: int
    telegram_nickname: str
    first_name: str
    last_name: str

class UserSchema(UserAddSchema):
    id: int
    created_ad: str
    updated_ad: str