from typing import Any
from application.ports import CommandBus, CommandHandler
from infrastructure.exceptions import HandlerNotRegisteredException


class InMemoryCommandBus(CommandBus):
    def __init__(self) -> None:
        self._handlers: dict[type[Any], CommandHandler[Any]] = {}

    def register_handler(
        self, command_type: type[Any], handler: CommandHandler[Any]
    ) -> None:
        self._handlers[command_type] = handler

    async def execute(self, command: Any) -> None:
        command_type = type(command)
        handler = self._handlers.get(command_type)
        if handler is None:
            raise HandlerNotRegisteredException(
                f"No handler registered for command {command_type}"
            )
        await handler.execute(command)
