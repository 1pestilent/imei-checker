from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


from app.core.models.user import UserModel
from app.core.models import base
from app.core import security
from app.users.schemas import UserLoginSchema, UserSchema, SafelyUserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect login or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_user(telegram_id: int,
                   session: AsyncSession
                   ) -> UserLoginSchema: 
    query = select(UserModel).where(UserModel.telegram_id == telegram_id)
    result = await session.execute(query)
    received_user = result.scalars().first()

    if received_user is None:
        raise credentials_exception
    
    user = UserSchema.from_orm(received_user)
    return user


async def authenticate_user(telegram_id: int, password: str, session: AsyncSession) -> SafelyUserSchema:
    user: UserSchema = await get_user(telegram_id, session)
    if not security.verify_password(password, user.password):
        raise credentials_exception
    logined_user = SafelyUserSchema(
        id = user.id,
        telegram_id=user.telegram_id,
        fullname=user.fullname,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    return logined_user