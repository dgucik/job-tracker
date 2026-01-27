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


class CompensationException(BaseDomainException):
    """Exception raised for errors in the compensation details."""

    def __init__(self, message: str = "Compensation details are invalid.") -> None:
        self.message = message
        super().__init__(self.message)


class CurrencyNotProvidedException(CompensationException):
    """Exception raised when currency is not provided with salary values."""

    def __init__(
        self, message: str = "Currency must be provided if salary values are specified."
    ) -> None:
        self.message = message
        super().__init__(self.message)
