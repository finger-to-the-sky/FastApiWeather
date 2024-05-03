from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_uuid(session: AsyncSession, user_id: str) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, user_email: str) -> User | None:
    return await session.get(User, user_email)


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    return await session.get(User, username)


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    user = User(username=user.username, email=user.email, hashed_password=user.password)
    session.add(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession,
                      user: User,
                      user_update: UserUpdate,
                      partial: bool = False
                      ) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()
    return None
