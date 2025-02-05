from fastapi import APIRouter, Depends

from app.users.schemas import TokenSchema, UserSchema
from app.auth import create_token
from app.auth import utils

router = APIRouter(prefix="/auth", tags=["Auth"])




@router.post("/login/", response_model=TokenSchema)
async def auth_user(user: UserSchema = Depends(utils.get_user_from_creads)):

    access_token = await create_token.access_token(user=user)
    refresh_token = await create_token.refresh_token(user=user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post("/refresh/",
            response_model=TokenSchema,
            response_model_exclude_none=True
            )
async def refresh_access_token(
    user: UserSchema = Depends(utils.get_user_from_payload)
    ):
    access_token = await utils.create_refresh_token(user)
    return TokenSchema(
        access_token=access_token
    )