from dataclasses import dataclass
from enum import Enum

from domain.exceptions import SalaryRangeException


class EmploymentType(Enum):
    B2B = "B2B"
    PERMANENT = "PERMANENT"
    CONTRACT = "CONTRACT"


@dataclass(frozen=True)
class Compensation:
    """
    Represents a salary range with minimum and maximum values.

    Attributes:
        min_salary: Minimum salary value.
        max_salary: Maximum salary value.
        currency: Currency of the salary.
        employment_type: Type of employment (B2B, permanent, contract).
    """

    min_salary: int | None
    max_salary: int | None
    currency: str
    employment_type: EmploymentType

    def __post_init__(self) -> None:
        if self.min_salary and self.max_salary:
            if self.min_salary < 0 or self.max_salary < 0:
                raise SalaryRangeException("Salary values must be non-negative.")
            if self.min_salary > self.max_salary:
                raise SalaryRangeException(
                    "Minimum salary cannot be greater than maximum salary."
                )
