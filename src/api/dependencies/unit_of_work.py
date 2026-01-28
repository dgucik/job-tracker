from collections.abc import Generator
from infrastructure.db.session import AsyncSessionLocal
from infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork


def get_unit_of_work() -> Generator[SqlAlchemyUnitOfWork, None]:
    """
    Dependency injector for SqlAlchemyUnitOfWork.

    Yields an instance of SqlAlchemyUnitOfWork with an AsyncSessionLocal session factory.
    """
    uow = SqlAlchemyUnitOfWork(AsyncSessionLocal)
    yield uow
