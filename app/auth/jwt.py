from app.core.security import encode_jwt
from app.core.config import TOKEN_TYPE_FIELD
from datetime import timedelta



async def create_jwt(
          token_type: str,
          payload: dict,
          expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return encode_jwt(
         payload=jwt_payload,
         expire_timedelta=expire_timedelta
    )