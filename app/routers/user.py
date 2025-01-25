from fastapi import APIRouter, Depends

from typing import Annotated
from models import models
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user", tags=["User"])

SessionDep = Annotated[AsyncSession, Depends(models.get_session)]

@router.post("/setup_database")
async def setup_database():
    await models.setup_database()
    

@router.post("/add")
async def add_user(telegram_id, nick, first_name, last_name, session: SessionDep):
    pass