from collections.abc import AsyncGenerator
from infrastructure.db.session import AsyncSessionLocal
from infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


async def get_unit_of_work() -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    """
    Dependency injector for SqlAlchemyUnitOfWork.

    Yields an instance of SqlAlchemyUnitOfWork with an AsyncSessionLocal session factory.
    """
    uow = SqlAlchemyUnitOfWork(AsyncSessionLocal)
    yield uow
