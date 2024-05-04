from fastapi import HTTPException
from starlette import status

from app.users.models import User


async def check_user(user: User, data_for_message) -> User:
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User {data_for_message} not found'
    )


def validate_password(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password and Confirm Password does not equal')
