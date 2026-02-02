import logging
from typing import Any

from application.ports import QueryBus, QueryHandler
from infrastructure.exceptions import HandlerNotRegisteredException

logger = logging.getLogger(__name__)


class InMemoryQueryBus(QueryBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Any], QueryHandler[Any, Any]] = {}

    def register_handler(
        self, query_type: type[Any], handler: QueryHandler[Any, Any]
    ) -> None:
        self._handlers[query_type] = handler

    async def execute(self, query: Any) -> Any:
        query_type = type(query)
        handler = self._handlers.get(query_type)
        if handler is None:
            logger.warning(
                "No handler registered for query", extra={"query_type": str(query_type)}
            )
            raise HandlerNotRegisteredException(
                f"No handler registered for query {query_type}"
            )
        return await handler.execute(query)
