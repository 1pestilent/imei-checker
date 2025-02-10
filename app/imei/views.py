from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import base
from app.imei.utils import imei

from app.imei.schemas import BalanceSchema, ServicesSchema
from app.auth.utils import get_current_user, http_bearer
from app.users.schemas import UserSchema

router = APIRouter(prefix="/imei", tags=["IMEI"], dependencies=[Depends(http_bearer)])

SessionDep = Annotated[AsyncSession, Depends(base.get_session)]

@router.get("/balance")
async def get_balance(session: SessionDep, user: Annotated[UserSchema, Depends(get_current_user)]) -> BalanceSchema:
    balance: BalanceSchema = await imei.get_balance()
    return balance

@router.get("/services")
async def get_services(session: SessionDep, user: Annotated[UserSchema, Depends(get_current_user)]) -> ServicesSchema:
    services: ServicesSchema = await imei.get_services()
    return services