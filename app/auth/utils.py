from fastapi import HTTPException, status, Depends
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.auth.schemas import TokenSchema
from app.core.models.user import UserModel
from app.core.models import base
from app.core import security
from app.core.config import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.users.schemas import UserSchema, SafelyUserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_bearer = HTTPBearer(auto_error=False)
session_dep = Annotated[AsyncSession, Depends(base.get_session)]

async def get_user(telegram_id: int,
                   session: session_dep,
                   ) -> UserSchema:
    
    query = select(UserModel).where(UserModel.telegram_id == telegram_id)
    result = await session.execute(query)
    received_user = result.scalars().first()

    if received_user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Failed to get user!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = UserSchema.from_orm(received_user)
    return user

def return_safe_user(user: UserSchema) -> SafelyUserSchema:
    safe_user_data = user.model_dump(exclude={"password"})
    safe_user = SafelyUserSchema(**safe_user_data)
    return safe_user

async def authenticate_user(telegram_id: int,
                            password: str,
                            session: session_dep
                            ) -> SafelyUserSchema:
    user: UserSchema = await get_user(telegram_id, session)

    if not security.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    logined_user = SafelyUserSchema(
        id = user.id,
        telegram_id=user.telegram_id,
        fullname=user.fullname,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    return logined_user

async def get_token_payload(
        token: Annotated[str, Depends(oauth2_scheme)]
        ) -> dict:
    try:
        payload = security.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}"
        )
    return payload

def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )

async def get_user_from_payload(payload: dict,
                                session: session_dep,
                                ) -> SafelyUserSchema:
    telegram_id = payload.get("id")
    user = await get_user(int(telegram_id), session)
    return return_safe_user(user)

async def get_current_user(session: session_dep,
                           payload: Annotated[dict, Depends(get_token_payload)],
                           token
                           ):
    if validate_token_type(payload, ACCESS_TOKEN_TYPE):
        user = await get_user_from_payload(payload, session)
        return user
    
async def get_current_user_for_refresh(session: session_dep,
                           payload: Annotated[dict, Depends(get_token_payload)],
                           ):
    if validate_token_type(payload, REFRESH_TOKEN_TYPE):
        user = await get_user_from_payload(payload, session)
        return user