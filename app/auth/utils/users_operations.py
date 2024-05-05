from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils.exceptions import raise_401_exception
from app.auth.utils.auth_operations import get_token_data, REFRESH_TOKEN_TYPE
from app.db.config import DB
from app.users.models import User
from app.users.password_settings import verify_password
from app.users.queries.crud import get_user_by_username
from app.users.queries.dependecies import user_by_uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def authenticate_user(username: str,
                            password: str,
                            session: AsyncSession = Depends(DB.session_dependency)
                            ) -> User | bool:
    user = await get_user_by_username(session=session, username=username)
    if not user or not verify_password(password, user.hashed_password):
        raise raise_401_exception(
            detail="Incorrect username or password"
        )
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(DB.session_dependency)
                           ) -> User:
    token_data = get_token_data(token=token)
    user = await user_by_uuid(session=session, user_id=token_data.id)
    if user is None:
        raise raise_401_exception(
            detail="Could not validate credentials"
        )
    return user


async def get_current_user_by_refresh(token: Annotated[str, Depends(oauth2_scheme)],
                                      session: AsyncSession = Depends(DB.session_dependency)
                                      ) -> User:
    token_data = get_token_data(token=token, token_type=REFRESH_TOKEN_TYPE)
    user = await user_by_uuid(session=session, user_id=token_data.id)
    if user is None:
        raise raise_401_exception(
            detail="Could not validate credentials"
        )
    return user
