import logging
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from domain.exceptions import (
    CompensationException,
    CurrencyNotProvidedException,
    JobApplicationDocumentNotFoundException,
    JobApplicationNotFoundException,
    SalaryRangeException,
    WorkLocationException,
)
from infrastructure.exceptions import (
    EntityNotFoundError,
    HandlerNotRegisteredException,
)

logger = logging.getLogger(__name__)


def _create_handler(status_code: int, log_warning: bool = False) -> Callable:
    """
    Creates a handler returning JSON with detail.

    Args:
        status_code: The HTTP status code to return.
        log_warning: Whether to log a warning when the exception is not handled.

    Returns:
        A handler function that returns a JSONResponse with the status code and detail.
    """

    async def handler(_request: Request, exc: BaseException) -> JSONResponse:
        if log_warning:
            logger.warning("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)},
        )

    return handler


# fmt: off
EXCEPTION_REGISTRY: list[dict[str, Any]] = [
    # Domain - Not Found
    {"exception": JobApplicationNotFoundException, "status_code": status.HTTP_404_NOT_FOUND},
    # Domain - Validation (400)
    {"exception": WorkLocationException, "status_code": status.HTTP_400_BAD_REQUEST},
    {"exception": CurrencyNotProvidedException, "status_code": status.HTTP_400_BAD_REQUEST},
    {"exception": SalaryRangeException, "status_code": status.HTTP_400_BAD_REQUEST},
    {"exception": CompensationException, "status_code": status.HTTP_400_BAD_REQUEST},
    {"exception": JobApplicationDocumentNotFoundException, "status_code": status.HTTP_404_NOT_FOUND},
    # Infrastructure
    {"exception": EntityNotFoundError, "status_code": status.HTTP_404_NOT_FOUND},
    {"exception": HandlerNotRegisteredException, "status_code": status.HTTP_501_NOT_IMPLEMENTED, "log_warning": True},
]
# fmt: on


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers all handlers from EXCEPTION_REGISTRY.

    Args:
        app: The FastAPI app to register the exception handlers to.
    """
    for entry in EXCEPTION_REGISTRY:
        exc_type = entry["exception"]
        status_code = entry["status_code"]
        log_warning = entry.get("log_warning", False)
        handler = _create_handler(status_code=status_code, log_warning=log_warning)
        app.add_exception_handler(exc_type, handler)
