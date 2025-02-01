from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from jwt import InvalidTokenError

from core.models import user
from core.models import base
from core import security
from users import schemas

router = APIRouter(prefix="/user", tags=["User"])
SessionDep = Annotated[AsyncSession, Depends(base.get_session)]
http_bearer = HTTPBearer()


async def validate_user(credentials: HTTPBasicCredentials, session: SessionDep) -> schemas.UserSchema:
    query = select(user.UserModel).where(user.UserModel.telegram_id == credentials.username)
    result = await session.execute(query)
    current_user = result.scalars().first()

    if not current_user or not security.verify_password(credentials.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrent username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    output_user = schemas.UserSchema.from_orm(current_user)
    return output_user


async def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        ) -> schemas.UserSchema:
    token = credentials.credentials
    try:    
        payload = security.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Invalid token error: {e}")
    return payload


async def get_current_auth_user(session: SessionDep,
        payload: dict = Depends(get_current_token_payload)
        ) -> schemas.UserSchema:
        id: int | None = payload.get("id")
        query = select(user.UserModel).where(user.UserModel.id == id)
        result = await session.execute(query)

        if not result:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="This user in not exists")
        
        current_user = result.scalars().first()
        current_user = schemas.UserSchema.from_orm(current_user)
        return current_user


@router.post("/setup_database")
async def setup_database():
    await base.setup_database()

@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: schemas.UserSchema = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.fullname,
        "logged_in_at": iat,
    }

@router.get("/get/{user_id}")
async def get_user_by_id(user_id: int, session: SessionDep) -> schemas.UserSchema:
    query = select(user.UserModel).where(user.UserModel.id == user_id)
    result = await session.execute(query)
    user_output = result.scalars().first()
    if user_output is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return schemas.UserSchema(
        id=user_output.id,
        telegram_id=user_output.telegram_id,
        fullname=user_output.fullname,  
        created_at=user_output.created_at.isoformat(),
        updated_at=user_output.updated_at.isoformat()
    )

@router.post("/add")
async def add_user(data: schemas.UserAddSchema, session: SessionDep):
    new_user = user.UserModel(
        telegram_id = data.telegram_id,
        password = security.hash_password(data.password),
        fullname = data.fullname,
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"User with telegram_id: {data.telegram_id} is already exists.")
    return {"message": "User added"}        

@router.post("/login", response_model=schemas.Token)
def auth_user(user: schemas.UserSchema = Depends(validate_user)):
    payload = {
        "id": user.id,
        "username": user.fullname,
    }
    token = security.encode_jwt(payload=payload)
    return schemas.Token(
        access_token=token,
    )
