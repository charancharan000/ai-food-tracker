from app.db.session import async_engine
from app.models.base import Base
import app.models

async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
