from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from typing import Annotated

from app.auth import utils
from app.auth import create_token
from app.auth.schemas import TokenSchema
from app.users.schemas import SafelyUserSchema

router = APIRouter(tags=["Auth"])

http_bearer = HTTPBearer(auto_error=False)


@router.post("/token")
async def login_for_tokens(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           session: utils.session_dep,
                                 ) -> TokenSchema:
    user = await utils.authenticate_user(int(form_data.username),form_data.password, session)
    
    access_token = await create_token.access_token(user)
    refresh_token = await create_token.refresh_token(user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh",
            response_model=TokenSchema,
            response_model_exclude_none=True,
            dependencies=[Depends(http_bearer)]
            )
async def refresh_access_token(user: SafelyUserSchema = Depends(utils.get_current_user_for_refresh)):
    access_token = await create_token.access_token(user)

    return TokenSchema(
        access_token=access_token
    )