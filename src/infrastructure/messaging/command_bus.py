from typing import Any
from application.ports import CommandBus, CommandHandler
from infrastructure.exceptions import HandlerNotRegisteredException


class InMemoryCommandBus(CommandBus):
    """
    In-memory implementation of the command bus.

    Attributes:
        _handlers: A dictionary of command types and their handlers.
    """

    def __init__(self) -> None:
        self._handlers: dict[type[Any], CommandHandler[Any]] = {}

    def register_handler(
        self, command_type: type[Any], handler: CommandHandler[Any]
    ) -> None:
        """
        Register a handler for a command type.

        Args:
            command_type: The type of command to register the handler for.
            handler: The handler to register for the command type.
        """
        self._handlers[command_type] = handler

    async def execute(self, command: Any) -> None:
        """
        Execute a command.

        Args:
            command: The command to execute.
        """
        command_type = type(command)
        handler = self._handlers.get(command_type)
        if handler is None:
            raise HandlerNotRegisteredException(
                f"No handler registered for command {command_type}"
            )
        await handler.execute(command)
