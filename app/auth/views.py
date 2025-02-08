from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.models import base
from app.auth import utils
from app.auth import create_token
from app.auth.schemas import TokenSchema
from app.users.schemas import UserLoginSchema, SafelyUserSchema, UserSchema

router = APIRouter(tags=["Auth"])


@router.post("/test/")
async def test(data: Annotated[UserLoginSchema, Form()],
               session: AsyncSession = Depends(base.get_session)
               ):
    return await utils.get_user(data.telegram_id, session)

@router.post("/token")
async def login_for_tokens(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           session: AsyncSession = Depends(base.get_session)
                                 ) -> TokenSchema:
    user = await utils.authenticate_user(int(form_data.username),form_data.password, session)
    
    access_token = await create_token.access_token(user)
    refresh_token = await create_token.refresh_token(user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
