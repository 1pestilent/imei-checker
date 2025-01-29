from pydantic import BaseModel

class UserAddSchema(BaseModel):
    telegram_id: int
    telegram_nickname: str
    first_name: str
    last_name: str

class UserSchema(UserAddSchema):
    id: int
    created_at: str
    updated_at: str