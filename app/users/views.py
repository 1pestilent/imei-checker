from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from core.models import user
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
    

@router.post("/add")
async def add_user(data: schemas.UserAddSchema, session: SessionDep):
    new_user = user.UserModel(
        telegram_id = data.telegram_id,
        password = data.password,
        full_name = data.fullname,
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()  
        raise HTTPException(status_code=400, detail=f"User with telegram id - {data.telegram_id} is already exists.")
    return {"message": "User added"}

@router.get("/get/{user_id}")
async def get_user_by_id(user_id: int, session: SessionDep) -> schemas.UserSchema:
    query = select(user.UserModel).where(user.UserModel.id == user_id)
    result = await session.execute(query)
    user_output = result.scalars().first()
    if user_output is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return schemas.UserSchema(
        id=user_output.id,
        telegram_id=user_output.telegram_id,
        fullname=user_output.full_name,  
        created_at=user_output.created_at.isoformat(),
        updated_at=user_output.updated_at.isoformat()
    )
