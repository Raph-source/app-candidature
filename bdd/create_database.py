# create_db.py
import asyncio
from app.models import Base
from database import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Base creee")

asyncio.run(init_db())