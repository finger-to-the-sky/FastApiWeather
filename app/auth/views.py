from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.config import auth_settings
from app.auth.schemas import Token
from app.auth.utils import create_access_token
from app.auth.user_operations import authenticate_user, get_current_user
from app.db.config import DB
from app.users.schemas import UserSchema

router = APIRouter(tags=['Auth'], prefix='/auth')


@router.post("/login/")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(DB.session_dependency)
) -> Token:
    user = await authenticate_user(session=session,
                                   username=form_data.username,
                                   password=form_data.password)

    access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    return current_user
