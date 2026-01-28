from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator

from infrastructure.db.session import AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an asynchronous database session.

    Yields:
        AsyncGenerator[AsyncSession, None]: An asynchronous generator yielding a database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
