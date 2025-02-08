from fastapi import APIRouter, Depends

from app.users.schemas import SafelyUserSchema

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/me")
async def get_current_user() -> SafelyUserSchema:
    ...