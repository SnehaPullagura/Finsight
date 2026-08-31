from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings
from backend.app.core.logging import logger

engine_kwargs = {
    "echo": False,
    "future": True,
    "pool_pre_ping": True,
}

if "sqlite" not in settings.DATABASE_URL:
    engine_kwargs["pool_size"] = 20
    engine_kwargs["max_overflow"] = 10

# Async Engine for FastAPI Request Lifecycle
async_engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync Engine for Migrations, Background Workers and Tools
sync_db_url = settings.DATABASE_SYNC_URL if "postgresql" in settings.DATABASE_SYNC_URL else settings.DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "")
sync_engine_kwargs = {"echo": False, "pool_pre_ping": True}
if "sqlite" not in sync_db_url:
    sync_engine_kwargs["pool_size"] = 10

sync_engine = create_engine(
    sync_db_url,
    **sync_engine_kwargs
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rolled back due to error: {str(e)}", exc_info=True)
            raise
        finally:
            await session.close()
