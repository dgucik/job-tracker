import pytest

from application.commands.create_job_application import (
    CreateJobApplicationCommand,
    CreateJobApplicationCommandHandler,
    RawCompensation,
)
from application.dtos import JobApplicationDTO
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.value_objects.compensation import EmploymentType
from domain.value_objects.work_location import WorkModel


@pytest.fixture
def handler(uow):
    return CreateJobApplicationCommandHandler(uow)


@pytest.fixture
def valid_command():
    return CreateJobApplicationCommand(
        company_name="Tech Corp",
        role_name="Software Engineer",
        posting_url="https://techcorp.com/jobs/123",
        status="APPLIED",
        work_model="REMOTE",
        work_location="Warsaw",
        compensations=[
            RawCompensation(
                min_salary=5000,
                max_salary=8000,
                currency="USD",
                employment_type="B2B",
            )
        ],
        notes="Exciting opportunity",
    )


@pytest.mark.asyncio
async def test_execute_creates_job_application_and_adds_to_repository(
    handler, uow, valid_command
):
    result = await handler.execute(valid_command)

    uow.job_applications.add.assert_called_once()
    assert isinstance(result, JobApplicationDTO)
    assert result.company_name == "Tech Corp"
    assert result.role_name == "Software Engineer"
    call_arg = uow.job_applications.add.call_args[0][0]
    assert isinstance(call_arg, JobApplication)
    assert call_arg.company_name == "Tech Corp"
    assert call_arg.role_name == "Software Engineer"
    assert call_arg.posting_url == "https://techcorp.com/jobs/123"
    assert call_arg.status == ApplicationStatus.APPLIED
    assert call_arg.work_location.work_model == WorkModel.REMOTE
    assert call_arg.work_location.location == "Warsaw"
    assert len(call_arg.compensations) == 1
    assert call_arg.compensations[0].min_salary == 5000
    assert call_arg.compensations[0].max_salary == 8000
    assert call_arg.compensations[0].currency == "USD"
    assert call_arg.compensations[0].employment_type == EmploymentType.B2B
    assert call_arg.notes == "Exciting opportunity"


@pytest.mark.asyncio
async def test_execute_commits_transaction(handler, uow, valid_command):
    result = await handler.execute(valid_command)

    uow.commit.assert_called_once()
    assert isinstance(result, JobApplicationDTO)


@pytest.mark.asyncio
async def test_execute_with_empty_compensations(handler, uow):
    command = CreateJobApplicationCommand(
        company_name="Startup",
        role_name="DevOps",
        posting_url="https://startup.com/job",
        status="REJECTED",
        work_model="HYBRID",
        work_location="Kraków",
        compensations=[],
    )

    await handler.execute(command)

    call_arg = uow.job_applications.add.call_args[0][0]
    assert call_arg.company_name == "Startup"
    assert call_arg.compensations == []


@pytest.mark.asyncio
async def test_execute_with_multiple_compensations(handler, uow):
    command = CreateJobApplicationCommand(
        company_name="BigCo",
        role_name="Lead",
        posting_url="https://bigco.com/job",
        status="INTERVIEWED",
        work_model="ONSITE",
        work_location="Berlin",
        compensations=[
            RawCompensation(
                min_salary=10000,
                max_salary=15000,
                currency="EUR",
                employment_type="B2B",
            ),
            RawCompensation(
                min_salary=8000,
                max_salary=12000,
                currency="EUR",
                employment_type="PERMANENT",
            ),
        ],
    )

    await handler.execute(command)

    call_arg = uow.job_applications.add.call_args[0][0]
    assert len(call_arg.compensations) == 2
    assert call_arg.compensations[0].employment_type == EmploymentType.B2B
    assert call_arg.compensations[1].employment_type == EmploymentType.PERMANENT
