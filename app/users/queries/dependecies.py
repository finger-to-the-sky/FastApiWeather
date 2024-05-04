from typing import Annotated

from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import DB
from app.users.models import User
from app.users.queries import crud


async def user_by_uuid(user_id: Annotated[str, Path],
                       session: AsyncSession = Depends(DB.session_dependency)) -> User:
    user = await crud.get_user_by_uuid(session=session, user_id=user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User {user_id} not found'
    )
