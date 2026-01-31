from types import TracebackType
from typing import Protocol, Type, TypeVar

from domain.repositories import JobApplicationRepository


class UnitOfWork(Protocol):
    job_applications: JobApplicationRepository

    async def __aenter__(self) -> "UnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


# Type variables for command and query handlers
TCommand = TypeVar("TCommand", contravariant=True)
TQuery = TypeVar("TQuery", contravariant=True)
TResult = TypeVar("TResult", covariant=True)


# Command and query handlers
class CommandHandler(Protocol[TCommand]):
    async def execute(self, command: TCommand) -> None: ...


class CommandBus(Protocol):
    def register_handler(
        self, command_type: Type[TCommand], handler: CommandHandler[TCommand]
    ) -> None: ...
    async def execute(self, command: TCommand) -> None: ...


class QueryHandler(Protocol[TQuery, TResult]):
    async def execute(self, query: TQuery) -> TResult: ...


class QueryBus(Protocol):
    def register_handler(
        self, query_type: Type[TQuery], handler: QueryHandler[TQuery, TResult]
    ) -> None: ...
    async def execute(self, query: TQuery) -> TResult: ...
