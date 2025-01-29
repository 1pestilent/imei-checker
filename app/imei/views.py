from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from core.models import base

router = APIRouter(prefix="/imei", tags=["IMEI"])

SessionDep = Annotated[AsyncSession, Depends(base.get_session)]

@router.get("/balance")
async def get_balance(session: SessionDep):
    return {"Hello": "World"}
