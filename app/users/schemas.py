from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    telegram_id: int
    password: str

class UserAddSchema(UserLoginSchema):
    fullname: str

class UserSchema(BaseModel):
    id: int
    telegram_id: int
    fullname: str
    created_at: str
    updated_at: str