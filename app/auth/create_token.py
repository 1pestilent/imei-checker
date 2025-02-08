from datetime import timedelta

from app.core.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, REFRESH_TOKEN_EXPIRE_DAYS
from app.users.schemas import UserSchema
from app.core.security import create_jwt

async def access_token(user: UserSchema,
                            expire_timedelta: int | None = None
                            ) -> str:
    payload = {
        "id": user.id,
        "username": user.fullname,
        }
    return await create_jwt(
         token_type=ACCESS_TOKEN_TYPE,
         payload=payload,
         expire_timedelta= expire_timedelta
    )

async def refresh_token(user: UserSchema,
    expire_timedelta: int | None = None
    ) -> str:
    payload = {
        "id": user.id,
        "username": user.fullname,
        }
    return await create_jwt(
         token_type=REFRESH_TOKEN_TYPE,
         payload=payload,
         expire_timedelta= timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )    