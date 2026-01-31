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

    async def commit(self) -> None:
        """
        Commit the current transaction.
        """
        ...

    async def rollback(self) -> None:
        """
        Rollback the current transaction.
        """
        ...


# Type variables for command and query handlers
TCommand = TypeVar("TCommand", contravariant=True)
TQuery = TypeVar("TQuery", contravariant=True)
TResult = TypeVar("TResult", covariant=True)


# Command and query handlers
class CommandHandler(Protocol[TCommand]):
    """
    Handler for executing commands.

    Attributes:
        _handlers: A dictionary of command types and their handlers.
    """

    async def execute(self, command: TCommand) -> None:
        """
        Execute a command.

        Args:
            command: The command to execute.
        """
        ...


class CommandBus(Protocol):
    """
    Bus for executing commands.

    Attributes:
        _handlers: A dictionary of command types and their handlers.
    """

    def register_handler(
        self, command_type: Type[TCommand], handler: CommandHandler[TCommand]
    ) -> None:
        """
        Register a handler for a command type.

        Args:
            command_type: The type of command to register the handler for.
            handler: The handler to register for the command type.
        """
        ...

    async def execute(self, command: TCommand) -> None:
        """
        Execute a command.

        Args:
            command: The command to execute.
        """
        ...


class QueryHandler(Protocol[TQuery, TResult]):
    """
    Handler for executing queries.

    Attributes:
        _handlers: A dictionary of query types and their handlers.
    """

    async def execute(self, query: TQuery) -> TResult:
        """
        Execute a query.

        Args:
            query: The query to execute.
        """
        ...


class QueryBus(Protocol):
    """
    Bus for executing queries.

    Attributes:
        _handlers: A dictionary of query types and their handlers.
    """

    def register_handler(
        self, query_type: Type[TQuery], handler: QueryHandler[TQuery, TResult]
    ) -> None:
        """
        Register a handler for a query type.

        Args:
            query_type: The type of query to register the handler for.
            handler: The handler to register for the query type.
        """
        ...

    async def execute(self, query: TQuery) -> TResult:
        """
        Execute a query.

        Args:
            query: The query to execute.
        """
        ...
