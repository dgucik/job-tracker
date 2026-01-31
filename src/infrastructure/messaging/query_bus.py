from typing import Any
from application.ports import QueryBus, QueryHandler
from infrastructure.exceptions import HandlerNotRegisteredException


class InMemoryQueryBus(QueryBus):
    """
    In-memory implementation of the query bus.

    Attributes:
        _handlers: A dictionary of query types and their handlers.
    """

    def __init__(self) -> None:
        self._handlers: dict[type[Any], QueryHandler[Any, Any]] = {}

    def register_handler(
        self, query_type: type[Any], handler: QueryHandler[Any, Any]
    ) -> None:
        """
        Register a handler for a query type.

        Args:
            query_type: The type of query to register the handler for.
            handler: The handler to register for the query type.
        """
        self._handlers[query_type] = handler

    async def execute(self, query: Any) -> Any:
        """
        Execute a query.

        Args:
            query: The query to execute.
        """
        query_type = type(query)
        handler = self._handlers.get(query_type)
        if handler is None:
            raise HandlerNotRegisteredException(
                f"No handler registered for query {query_type}"
            )
        return await handler.execute(query)
