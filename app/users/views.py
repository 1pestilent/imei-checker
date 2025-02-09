from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.users.schemas import SafelyUserSchema, UserSchema
from app.auth import utils

router = APIRouter(prefix="/users", tags=["User"], dependencies=[Depends(utils.http_bearer)])

@router.get("/me")
async def get_current_user(user: Annotated[UserSchema, Depends(utils.get_current_user)],
                           ) -> SafelyUserSchema:
    return user