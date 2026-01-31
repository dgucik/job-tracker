import importlib
import inspect
import pkgutil
from typing import Any, TypeVar, get_args

from application import queries as queries_pkg
from application.ports import QueryBus, UnitOfWork
from fastapi import Depends
from infrastructure.messaging.query_bus import InMemoryQueryBus

from api.dependencies.unit_of_work import get_unit_of_work


def _discover_query_handlers() -> list[tuple[type[Any], type[Any]]]:
    """Returns (query_type, handler_class) - handler_class is constructible with (uow: UnitOfWork)."""
    handlers: list[tuple[type[Any], type[Any]]] = []

    for _importer, modname, _ispkg in pkgutil.iter_modules(queries_pkg.__path__):
        if modname.startswith("_") or modname == "dtos":
            continue

        module = importlib.import_module(f"application.queries.{modname}")

        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if not _name.endswith("QueryHandler"):
                continue

            # Extract query type from QueryHandler[TQuery, TResult] generic
            query_type: type[Any] | None = None
            for base in getattr(obj, "__orig_bases__", ()):
                args = get_args(base)
                if args and len(args) >= 1:
                    arg = args[0]
                    # Skip TypeVar (e.g. TQuery from Protocol)
                    if not isinstance(arg, TypeVar):
                        query_type = arg
                        break

            if query_type is not None:
                handlers.append((query_type, obj))

    return handlers


def get_query_bus(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> QueryBus:
    """
    Get the query bus.

    Args:
        uow: The unit of work.

    Returns:
        The query bus.
    """
    bus = InMemoryQueryBus()

    for query_type, handler_class in _discover_query_handlers():
        handler = handler_class(uow)
        bus.register_handler(query_type, handler)

    return bus
