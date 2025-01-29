from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from core.models import base
from users import schemas
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user", tags=["User"])

SessionDep = Annotated[AsyncSession, Depends(base.get_session)]

@router.post("/setup_database")
async def setup_database():
    await base.setup_database()
    

@router.post("/")
async def add_user(data: schemas.UserAddSchema, session: SessionDep):
    new_user = base.UserModel(
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

@router.get("/get")
async def get_user_by_id(id: int, session: SessionDep):
    query = select(base.UserModel).where(base.UserModel.id == id)
    result = await session.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
