import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

DIR_PROJECT = Path(__file__).parent.parent.parent
PATH_TO_ENV = DIR_PROJECT / '.env'

load_dotenv(PATH_TO_ENV)

DATABASE_URL = os.getenv('DATABASE_URL')


class Database:
    def __init__(self, db_url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=db_url, echo=echo
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_maker() as session:
            yield session
            await session.close()


DB = Database(db_url=DATABASE_URL, echo=False)
