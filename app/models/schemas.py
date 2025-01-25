from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    tg_nick: str
    firts_name: str
    last_name: str