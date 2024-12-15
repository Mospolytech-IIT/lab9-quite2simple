"""
    Main
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, engine
from models import Base, User

app = FastAPI()

@app.on_event("startup")
async def startup():
    """
        Syncs db if needed
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
