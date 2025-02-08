from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"