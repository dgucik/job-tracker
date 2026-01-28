class BaseInfrastructureException(Exception):
    """Base exception for infrastructure-related errors."""

    pass


class SessionNotInitializedException(BaseInfrastructureException):
    """Exception raised when a database session is not initialized."""

    def __init__(self, message: str = "Database session is not initialized."):
        super().__init__(message)
