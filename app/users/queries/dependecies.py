from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import DB
from app.users.exceptions import check_user
from app.users.models import User
from app.users.queries import crud


async def user_by_uuid(user_id: Annotated[str, Path],
                       session: AsyncSession = Depends(DB.session_dependency)) -> User:
    user = await crud.get_user_by_uuid(session=session, user_id=user_id)
    return await check_user(user=user, data_for_message=user_id)


