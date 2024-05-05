from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token
from app.auth.utils.auth_operations import create_access_token, create_refresh_token
from app.auth.utils.users_operations import authenticate_user, get_current_user, get_current_user_by_refresh
from app.db.config import DB
from app.users.schemas import UserSchema, User

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(tags=['Auth'], prefix='/auth', dependencies=[Depends(http_bearer)])


@router.post("/login/")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(DB.session_dependency)
) -> Token:
    user = await authenticate_user(session=session,
                                   username=form_data.username,
                                   password=form_data.password)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh/", response_model=Token, response_model_exclude_none=True)
async def get_refresh_token(
        current_user: Annotated[User, Depends(get_current_user_by_refresh)]
) -> Token:
    access_token = create_access_token(current_user)
    return Token(access_token=access_token)


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    return current_user
