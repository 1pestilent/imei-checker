from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.models.user import UserModel
from app.core.models import base
from app.core import security 
from app.users.schemas import *
from app.auth import create_token
from app.auth import utils

router = APIRouter(prefix="/user", tags=["User"])
SessionDep = Annotated[AsyncSession, Depends(base.get_session)]

@router.post("/registration/", response_model=TokenSchema)
async def registration_user(data: UserAddSchema, session: SessionDep):
    new_user = UserModel(
        telegram_id = data.telegram_id,
        password = security.hash_password(data.password),
        fullname = data.fullname,
    )
    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)  
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=f"User with telegram_id: {data.telegram_id} is already exists.")
   
    user = UserSchema.from_orm(new_user)

    access_token = await create_token.access_token(user=user)
    refresh_token = await create_token.refresh_token(user=user)
    
    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.get("/me/")
async def get_current_user(
    session: SessionDep,
    payload: dict = Depends(utils.get_payload_from_token),
    current_user: UserSchema = Depends(utils.get_user_from_payload),
) -> UserSchema:
    return current_user

@router.get("/get/{searched_user}")
async def get_user_by_id(searched_user: int ,
                        session: SessionDep,
                        payload: dict = Depends(utils.get_payload_from_token),
                        current_user: UserSchema = Depends(utils.get_user_from_payload),
                        ) -> UserSchema:
    
    query = select(UserModel).where(UserModel.id == searched_user)
    result = await session.execute(query)
    user_output = result.scalars().first()
    if user_output is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserSchema(
        id=user_output.id,
        telegram_id=user_output.telegram_id,
        fullname=user_output.fullname,  
        created_at=user_output.created_at,
        updated_at=user_output.updated_at
    )