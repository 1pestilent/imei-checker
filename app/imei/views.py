from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import base
from app.imei.utils import imei

from app.imei.schemas import BalanceSchema, ServicesSchema, ServiceItemSchema, CheckSchema
from app.auth.utils import get_current_user, http_bearer
from app.users.schemas import UserSchema

router = APIRouter(prefix="/imei", tags=["IMEI"], dependencies=[Depends(http_bearer)])

SessionDep = Annotated[AsyncSession, Depends(base.get_session)]

@router.get("/balance")
async def get_balance(
    session: SessionDep,
    user: Annotated[UserSchema, Depends(get_current_user)],
    ) -> BalanceSchema:
    balance: BalanceSchema = await imei.get_balance()
    return balance

@router.get("/services")
async def get_services(
    session: SessionDep,
    user: Annotated[UserSchema, Depends(get_current_user)],
    ) -> ServicesSchema:
    services: ServicesSchema = await imei.get_services()
    return services

@router.get("/service")
async def get_service_by_id(
    session: SessionDep,
    user: Annotated[UserSchema, Depends(get_current_user)],
    service_id: int
    ) -> ServiceItemSchema:
    service: ServiceItemSchema = await imei.get_service(service_id)
    return service

@router.post("/check")
async def check_by_imei(
    session: SessionDep,
    user: Annotated[UserSchema, Depends(get_current_user)],
    data: Annotated[CheckSchema, Form()],
    ):
    info = await imei.check_imei(data.service_id, data.device_id)
    return info