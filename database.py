"""
    Database setup
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./lab9.db"
DATABASE_URL_SYNC = "sqlite:///./lab9.db"

engine = create_async_engine(DATABASE_URL, echo=True)

sync_engine = create_engine(DATABASE_URL_SYNC)

async_session = sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)
sync_session = sessionmaker(sync_engine)

async def get_db():
    """

        Dependency
    """

    async with async_session() as session:
        yield session

def get_db_sync():
    """

        Dependency
    """
    with sync_session() as session:
        yield session
