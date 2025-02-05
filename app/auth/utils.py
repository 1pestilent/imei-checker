from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from sqlalchemy import select
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.models.user import UserModel
from app.core.models import base
from app.core import security 
from app.users.schemas import *
from app.auth.jwt import TOKEN_TYPE_FIELD
from app.core.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE

SessionDep = Annotated[AsyncSession, Depends(base.get_session)]
http_bearer = HTTPBearer()

async def get_user_from_creads(credentials: HTTPBasicCredentials, session: SessionDep) -> UserSchema:
    query = select(UserModel).where(UserModel.telegram_id == credentials.username)
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
         raise HTTPException(status.HTTP_404_NOT_FOUND,
                             detail="User is not exists!")
    
    if not security.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrent username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = UserSchema.from_orm(user)
    return user

async def get_payload_from_token(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        ) -> dict:
    token = credentials.credentials
    try:    
        payload = security.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Invalid token error: {e}")
    return payload

async def validate_token_type(payload: dict, token_type: str):
    current_token_type = payload.get(TOKEN_TYPE_FIELD)

    if current_token_type == token_type:
        return True
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail= f'Incorrect token type {current_token_type!r} expected {token_type!r}')

async def get_user_from_payload(
        session: SessionDep,
        payload: dict,
        ) -> UserSchema:
    
    if await validate_token_type(
    payload=payload,
    token_type=ACCESS_TOKEN_TYPE
        ):
    
        id: int | None = payload.get("id")
        query = select(UserModel).where(UserModel.id == id)
        result = await session.execute(query)

        if not result:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="This user is not exists")

        user = result.scalars().first()
        return UserSchema.from_orm(user)