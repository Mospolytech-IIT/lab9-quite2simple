"""
    Database setup
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./lab9.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

async def get_db():
    """
        Dependency
    """
    async with async_session() as session:
        yield session
