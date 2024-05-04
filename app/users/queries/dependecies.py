from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import DB
from app.users.models import User
from app.users.queries import crud


async def check_user(user: User, data_for_message) -> User:
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User {data_for_message} not found'
    )


async def user_by_uuid(user_id: Annotated[str, Path],
                       session: AsyncSession = Depends(DB.session_dependency)) -> User:
    user = await crud.get_user_by_uuid(session=session, user_id=user_id)
    return await check_user(user=user, data_for_message=user_id)


def validate_password(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password and Confirm Password does not equal')
