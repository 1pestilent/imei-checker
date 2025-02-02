from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.models.user import UserModel
from app.core.models import base
from app.core import security 
from app.users.schemas import *

SessionDep = Annotated[AsyncSession, Depends(base.get_session)]
http_bearer = HTTPBearer()


async def validate_user(credentials: HTTPBasicCredentials, session: SessionDep) -> UserSchema:
    query = select(UserModel).where(UserModel.telegram_id == credentials.username)
    result = await session.execute(query)
    current_user = result.scalars().first()

    if not current_user:
         raise HTTPException(status.HTTP_404_NOT_FOUND,
                             detail="User is not exists!")
    
    if not security.verify_password(credentials.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrent username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    output_user = UserSchema.from_orm(current_user)
    return output_user


async def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        ) -> UserSchema:
    token = credentials.credentials
    try:    
        payload = security.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Invalid token error: {e}")
    return payload


async def get_current_auth_user(session: SessionDep,
        payload: dict = Depends(get_current_token_payload)
        ) -> UserSchema:
        id: int | None = payload.get("id")
        query = select(UserModel).where(UserModel.id == id)
        result = await session.execute(query)

        if not result:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="This user in not exists")
        
        current_user = result.scalars().first()
        current_user = UserSchema.from_orm(current_user)
        return current_user