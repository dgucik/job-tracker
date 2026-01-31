import importlib
import inspect
import pkgutil
from typing import Any, TypeVar, get_args

from application import commands as commands_pkg
from application.ports import CommandBus, UnitOfWork
from fastapi import Depends
from infrastructure.messaging.command_bus import InMemoryCommandBus

from api.dependencies.unit_of_work import get_unit_of_work


def _discover_command_handlers() -> list[tuple[type[Any], type[Any]]]:
    """Returns (command_type, handler_class) - handler_class is constructible with (uow: UnitOfWork)."""
    handlers: list[tuple[type[Any], type[Any]]] = []

    for _importer, modname, _ispkg in pkgutil.iter_modules(commands_pkg.__path__):
        if modname.startswith("_"):
            continue

        module = importlib.import_module(f"application.commands.{modname}")

        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if not _name.endswith("CommandHandler"):
                continue

            # Extract command type from CommandHandler[TCommand] generic
            command_type: type[Any] | None = None
            for base in getattr(obj, "__orig_bases__", ()):
                args = get_args(base)
                if args and len(args) >= 1:
                    arg = args[0]
                    # Skip TypeVar (e.g. TCommand from Protocol)
                    if not isinstance(arg, TypeVar):
                        command_type = arg
                        break

            if command_type is not None:
                handlers.append((command_type, obj))

    return handlers


def get_command_bus(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> CommandBus:
    """
    Get the command bus.

    Args:
        uow: The unit of work.

    Returns:
        The command bus.
    """
    bus = InMemoryCommandBus()

    for command_type, handler_class in _discover_command_handlers():
        handler = handler_class(uow)
        bus.register_handler(command_type, handler)

    return bus
