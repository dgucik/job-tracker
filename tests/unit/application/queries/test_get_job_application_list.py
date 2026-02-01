import pytest

from application.queries.dtos import JobApplicationDTO
from application.queries.get_job_application_list import (
    GetJobApplicationListQuery,
    GetJobApplicationListQueryHandler,
)
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.value_objects.compensation import Compensation, EmploymentType
from domain.value_objects.work_location import WorkLocation, WorkModel


@pytest.fixture
def sample_job_application():
    return JobApplication.create(
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


@pytest.fixture
def handler(uow):
    return GetJobApplicationListQueryHandler(uow)


@pytest.mark.asyncio
async def test_execute_returns_empty_list_when_no_applications(handler, uow):
    uow.job_applications.get_all.return_value = []

    query = GetJobApplicationListQuery()
    result = await handler.execute(query)

    assert result == []
    uow.job_applications.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_execute_returns_list_of_dtos(handler, uow, sample_job_application):
    uow.job_applications.get_all.return_value = [sample_job_application]

    query = GetJobApplicationListQuery()
    result = await handler.execute(query)

    assert len(result) == 1
    dto = result[0]
    assert isinstance(dto, JobApplicationDTO)
    assert dto.id == sample_job_application.id
    assert dto.company_name == "Tech Corp"
    assert dto.role_name == "Software Engineer"
    assert dto.posting_url == "https://techcorp.com/jobs/123"
    assert dto.status == ApplicationStatus.APPLIED
    assert dto.work_model == WorkModel.REMOTE
    assert dto.work_location == "Warsaw"
    assert dto.notes == "Exciting opportunity"
    assert len(dto.compensations) == 1
    assert dto.compensations[0].min_salary == 5000
    assert dto.compensations[0].max_salary == 8000
    assert dto.compensations[0].currency == "USD"
    assert dto.compensations[0].employment_type == "B2B"


@pytest.mark.asyncio
async def test_execute_returns_multiple_dtos(handler, uow, sample_job_application):
    second_app = JobApplication.create(
        company_name="Other Co",
        role_name="DevOps",
        posting_url="https://other.com/job",
        status=ApplicationStatus.REJECTED,
        work_location=WorkLocation(work_model=WorkModel.HYBRID, location="Kraków"),
        compensations=[],
        notes=None,
    )
    uow.job_applications.get_all.return_value = [
        sample_job_application,
        second_app,
    ]

    query = GetJobApplicationListQuery()
    result = await handler.execute(query)

    assert len(result) == 2
    assert result[0].company_name == "Tech Corp"
    assert result[1].company_name == "Other Co"
    assert result[1].status == ApplicationStatus.REJECTED
    assert result[1].work_model == WorkModel.HYBRID
    assert result[1].work_location == "Kraków"
