from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.password_settings import get_password_hash
from app.users.schemas import UserCreate, UserUpdate


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_uuid(session: AsyncSession, user_id: str) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(session: AsyncSession, user_email: str) -> User | None:
    stmt = select(User).where(User.email == user_email)
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(stmt)
    return user


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password),
                is_admin=user.is_admin, is_superuser=user.is_superuser)
    session.add(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession,
                      user: User,
                      user_update: UserUpdate,
                      partial: bool = False
                      ) -> User:
    data = user_update.model_dump(exclude_unset=partial)
    if 'confirm_password' in data.keys():
        data['hashed_password'] = get_password_hash(data.pop('password'))
        data.pop('confirm_password')

    for name, value in data.items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()
    return None
