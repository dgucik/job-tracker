class BaseDomainException(Exception):
    """Base exception for domain-related errors."""

    pass


class SalaryRangeException(BaseDomainException):
    """Exception raised for errors in the salary range."""

    def __init__(self, message: str = "Salary range is invalid.") -> None:
        self.message = message
        super().__init__(self.message)


class WorkLocationException(BaseDomainException):
    """Exception raised for errors in the work location."""

    def __init__(self, message: str = "Work location is invalid.") -> None:
        self.message = message
        super().__init__(self.message)
