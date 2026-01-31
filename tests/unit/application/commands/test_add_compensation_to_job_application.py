import pytest
from uuid import uuid4

from application.commands.add_compensation_to_job_application import (
    AddCompensationToJobApplicationCommand,
    AddCompensationToJobApplicationCommandHandler,
)
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.exceptions import JobApplicationNotFoundException
from domain.value_objects.compensation import EmploymentType
from domain.value_objects.work_location import WorkLocation, WorkModel


@pytest.fixture
def existing_job_application():
    return JobApplication.create(
        company_name="Tech Corp",
        role_name="Engineer",
        posting_url="https://example.com/job",
        status=ApplicationStatus.APPLIED,
        work_location=WorkLocation(work_model=WorkModel.REMOTE, location=None),
        compensations=[],
        notes=None,
    )


@pytest.fixture
def handler(uow):
    return AddCompensationToJobApplicationCommandHandler(uow)


@pytest.mark.asyncio
async def test_execute_adds_compensation_and_commits(
    handler, uow, existing_job_application
):
    app_id = existing_job_application.id
    uow.job_applications.get_by_id.return_value = existing_job_application

    command = AddCompensationToJobApplicationCommand(
        job_application_id=app_id,
        min_salary=6000,
        max_salary=9000,
        currency="PLN",
        employment_type="B2B",
    )

    await handler.execute(command)

    uow.job_applications.get_by_id.assert_called_once_with(app_id)
    assert len(existing_job_application.compensations) == 1
    assert existing_job_application.compensations[0].min_salary == 6000
    assert existing_job_application.compensations[0].max_salary == 9000
    assert existing_job_application.compensations[0].currency == "PLN"
    assert (
        existing_job_application.compensations[0].employment_type == EmploymentType.B2B
    )
    uow.commit.assert_called_once()


@pytest.mark.asyncio
async def test_execute_raises_when_application_not_found(handler, uow):
    app_id = uuid4()
    uow.job_applications.get_by_id.return_value = None

    command = AddCompensationToJobApplicationCommand(
        job_application_id=app_id,
        min_salary=5000,
        max_salary=7000,
        currency="USD",
        employment_type="PERMANENT",
    )

    with pytest.raises(JobApplicationNotFoundException) as exc_info:
        await handler.execute(command)

    assert str(app_id) in str(exc_info.value)
    uow.commit.assert_not_called()
