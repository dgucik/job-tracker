from types import TracebackType
from application.ports import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from infrastructure.db.repositories import SqlAlchemyJobApplicationRepository
from infrastructure.exceptions import SessionNotInitializedException


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.job_applications = SqlAlchemyJobApplicationRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            if self._session is not None:
                await self._session.aclose()

    async def commit(self) -> None:
        if self._session is None:
            raise SessionNotInitializedException
        await self._session.commit()

    async def rollback(self) -> None:
        if self._session is None:
            raise SessionNotInitializedException
        await self._session.rollback()
