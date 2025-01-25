from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from models import models
from models import schemas
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user", tags=["User"])

SessionDep = Annotated[AsyncSession, Depends(models.get_session)]

@router.post("/setup_database")
async def setup_database():
    await models.setup_database()
    

@router.post("/")
async def add_user(data: schemas.UserAddSchema, session: SessionDep):
    new_user = models.UserModel(
        tg_id = data.telegram_id,
        tg_nick = data.telegram_nickname,
        first_name = data.first_name,
        last_name = data.last_name
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()  
        raise HTTPException(status_code=400, detail=f"User with telegram id - {data.telegram_id} is already exists.")
    return {"Ok": True}

@router.get("/")
async def get_user(session: SessionDep):
    query = select(models.UserModel)
    result = await session.execute(query)
    return result.scalars().all()
