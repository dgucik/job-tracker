import pytest
from domain.exceptions import CurrencyNotProvidedException, SalaryRangeException
from domain.value_objects.compensation import Compensation, EmploymentType


def test_should_create_compensation_with_none_salaries():
    compensation = Compensation(
        min_salary=None,
        max_salary=None,
        currency=None,
        employment_type=EmploymentType.CONTRACT,
    )
    assert compensation.min_salary is None
    assert compensation.max_salary is None
    assert compensation.currency is None
    assert compensation.employment_type == EmploymentType.CONTRACT


def test_should_create_compensation_with_only_min_salary():
    compensation = Compensation(
        min_salary=60000,
        max_salary=None,
        currency="EUR",
        employment_type=EmploymentType.B2B,
    )
    assert compensation.min_salary == 60000
    assert compensation.max_salary is None
    assert compensation.currency == "EUR"
    assert compensation.employment_type == EmploymentType.B2B


def test_should_create_compensation_with_only_max_salary():
    compensation = Compensation(
        min_salary=None,
        max_salary=80000,
        currency="GBP",
        employment_type=EmploymentType.CONTRACT,
    )
    assert compensation.min_salary is None
    assert compensation.max_salary == 80000
    assert compensation.currency == "GBP"
    assert compensation.employment_type == EmploymentType.CONTRACT


def test_should_create_compensation_with_equal_salaries():
    compensation = Compensation(
        min_salary=70000,
        max_salary=70000,
        currency="USD",
        employment_type=EmploymentType.PERMANENT,
    )
    assert compensation.min_salary == 70000
    assert compensation.max_salary == 70000
    assert compensation.currency == "USD"
    assert compensation.employment_type == EmploymentType.PERMANENT


def test_should_raise_exception_for_negative_salaries():
    with pytest.raises(SalaryRangeException) as exc_info:
        Compensation(
            min_salary=-5000,
            max_salary=10000,
            currency="USD",
            employment_type=EmploymentType.B2B,
        )
    assert str(exc_info.value) == "Salary values must be non-negative."


def test_should_create_compensation_successfully():
    compensation = Compensation(
        min_salary=50000,
        max_salary=100000,
        currency="USD",
        employment_type=EmploymentType.PERMANENT,
    )
    assert compensation.min_salary == 50000
    assert compensation.max_salary == 100000
    assert compensation.currency == "USD"
    assert compensation.employment_type == EmploymentType.PERMANENT


def test_should_raise_exception_when_min_salary_greater_than_max_salary():
    with pytest.raises(SalaryRangeException) as exc_info:
        Compensation(
            min_salary=100000,
            max_salary=50000,
            currency="USD",
            employment_type=EmploymentType.B2B,
        )
    assert (
        str(exc_info.value) == "Minimum salary cannot be greater than maximum salary."
    )


def test_should_raise_exception_when_currency_is_none():
    with pytest.raises(CurrencyNotProvidedException) as exc_info:
        Compensation(
            min_salary=50000,
            max_salary=100000,
            currency=None,
            employment_type=EmploymentType.B2B,
        )
    assert (
        str(exc_info.value)
        == "Currency must be provided if salary values are specified."
    )
