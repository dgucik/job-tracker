class BaseInfrastructureException(Exception):
    """Base exception for infrastructure-related errors."""

    pass


class SessionNotInitializedException(BaseInfrastructureException):
    """Exception raised when a database session is not initialized."""

    def __init__(self, message: str = "Database session is not initialized."):
        super().__init__(message)


class HandlerNotRegisteredException(BaseInfrastructureException):
    """Exception raised when a handler is not registered in the system."""

    def __init__(self, handler_type: str = "Handler not registered."):
        super().__init__(handler_type)


class EntityNotFoundError(BaseInfrastructureException):
    """Exception raised when an entity is not found in the persistence layer."""

    pass
