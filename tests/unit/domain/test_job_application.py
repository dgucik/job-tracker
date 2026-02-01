import pytest
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.exceptions import CompensationException
from domain.value_objects.compensation import Compensation, EmploymentType
from domain.value_objects.work_location import WorkLocation, WorkModel


@pytest.fixture
def job_application():
    return JobApplication.create(
        company_name="Tech Corp",
        role_name="Software Engineer",
        posting_url="https://techcorp.com/jobs/123",
        status=ApplicationStatus.APPLIED,
        work_location=WorkLocation(work_model=WorkModel.REMOTE, location="Warsaw"),
        compensations=[],
        notes="Exciting opportunity",
    )


def test_should_create_application_with_given_data():
    app = JobApplication.create(
        company_name="Tech Corp",
        role_name="Software Engineer",
        posting_url="https://techcorp.com/jobs/123",
        status=ApplicationStatus.APPLIED,
        work_location=WorkLocation(work_model=WorkModel.REMOTE, location="Warsaw"),
        compensations=[
            Compensation(
                min_salary=5000,
                max_salary=8000,
                currency="USD",
                employment_type=EmploymentType.B2B,
            )
        ],
        notes="Exciting opportunity",
    )

    assert app.id is not None
    assert app.applied_at is not None
    assert app.company_name == "Tech Corp"
    assert app.role_name == "Software Engineer"
    assert app.posting_url == "https://techcorp.com/jobs/123"
    assert app.status == ApplicationStatus.APPLIED
    assert app.work_location.work_model == WorkModel.REMOTE
    assert app.work_location.location == "Warsaw"
    assert len(app.compensations) == 1
    assert app.compensations[0].min_salary == 5000
    assert app.compensations[0].max_salary == 8000
    assert app.compensations[0].currency == "USD"
    assert app.compensations[0].employment_type == EmploymentType.B2B
    assert app.notes == "Exciting opportunity"


def test_should_add_compensation_to_application(job_application):
    compensation = Compensation(
        min_salary=6000,
        max_salary=9000,
        currency="USD",
        employment_type=EmploymentType.PERMANENT,
    )
    job_application._add_compensation(compensation)

    assert len(job_application.compensations) == 1
    assert job_application.compensations[0].min_salary == 6000
    assert job_application.compensations[0].max_salary == 9000
    assert job_application.compensations[0].currency == "USD"
    assert job_application.compensations[0].employment_type == EmploymentType.PERMANENT


def test_should_raise_exception_for_duplicate_compensation(job_application):
    compensation = Compensation(
        min_salary=5000,
        max_salary=8000,
        currency="USD",
        employment_type=EmploymentType.B2B,
    )

    duplicate_compensation = Compensation(
        min_salary=7000,
        max_salary=10000,
        currency="USD",
        employment_type=EmploymentType.B2B,
    )

    job_application._add_compensation(compensation)
    with pytest.raises(CompensationException) as exc_info:
        job_application._add_compensation(duplicate_compensation)

    assert str(exc_info.value) == "Compensation with employment B2B already exists."


def test_should_update_application_status(job_application):
    job_application.update_status("INTERVIEWED")

    assert job_application.status == "INTERVIEWED"


def test_should_add_notes_to_application(job_application):
    job_application.add_notes("Followed up via email")

    assert job_application.notes == "Followed up via email"
