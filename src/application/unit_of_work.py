from types import TracebackType
from typing import Protocol

from domain.repositories import JobApplicationRepository


class UnitOfWork(Protocol):
    job_applications: JobApplicationRepository

    def __aenter__(self) -> "UnitOfWork": ...

    def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
