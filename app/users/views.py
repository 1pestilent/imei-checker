from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.users import auth
from app.core.models.user import UserModel
from app.core.models import base
from app.core import security 
from app.users.schemas import *

router = APIRouter(prefix="/user", tags=["User"])
SessionDep = Annotated[AsyncSession, Depends(base.get_session)]

@router.get("/users/me/")
async def get_current_user(
    payload: dict = Depends(auth.get_current_token_payload),
    current_user: UserSchema = Depends(auth.get_current_auth_user),
) -> UserSchema:
    return current_user

@router.get("/get/{searched_user}")
async def get_user_by_id(searched_user: int ,
                         session: SessionDep,
                        payload: dict = Depends(auth.get_current_token_payload),
                        current_user: UserSchema = Depends(auth.get_current_auth_user)
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

@router.post("/registration")
async def registration_user(data: UserAddSchema, session: SessionDep):
    new_user = UserModel(
        telegram_id = data.telegram_id,
        password = security.hash_password(data.password),
        fullname = data.fullname,
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=f"User with telegram_id: {data.telegram_id} is already exists.")
    return {"message": "User added"}        

@router.post("/login", response_model=TokenSchema)
def auth_user(user: UserSchema = Depends(auth.validate_user)):
    payload = {
        "id": user.id,
        "username": user.fullname,
    }
    token = security.encode_jwt(payload=payload)
    return TokenSchema(
        access_token=token,
    )
