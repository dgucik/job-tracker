import pytest
from uuid import uuid4

from application.commands.update_job_application_status import (
    UpdateJobApplicationStatusCommand,
    UpdateJobApplicationStatusCommandHandler,
)
from uuid import UUID

from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.exceptions import JobApplicationNotFoundException
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
    return UpdateJobApplicationStatusCommandHandler(uow)


@pytest.mark.asyncio
async def test_execute_updates_status_and_commits(
    handler, uow, existing_job_application
):
    app_id = existing_job_application.id
    uow.job_applications.get_by_id.return_value = existing_job_application

    command = UpdateJobApplicationStatusCommand(
        job_application_id=app_id,
        status="INTERVIEWED",
    )

    result = await handler.execute(command)

    uow.job_applications.get_by_id.assert_called_once_with(app_id)
    assert existing_job_application.status == ApplicationStatus.INTERVIEWED
    uow.commit.assert_called_once()

    assert isinstance(result, UUID)
    assert result == app_id


@pytest.mark.asyncio
async def test_execute_raises_when_application_not_found(handler, uow):
    app_id = uuid4()
    uow.job_applications.get_by_id.return_value = None

    command = UpdateJobApplicationStatusCommand(
        job_application_id=app_id,
        status="OFFERED",
    )

    with pytest.raises(JobApplicationNotFoundException) as exc_info:
        await handler.execute(command)

    assert str(app_id) in str(exc_info.value)
    uow.commit.assert_not_called()


@pytest.mark.asyncio
async def test_execute_updates_to_rejected(handler, uow, existing_job_application):
    uow.job_applications.get_by_id.return_value = existing_job_application

    command = UpdateJobApplicationStatusCommand(
        job_application_id=existing_job_application.id,
        status="REJECTED",
    )

    result = await handler.execute(command)

    assert existing_job_application.status == ApplicationStatus.REJECTED
    assert isinstance(result, UUID)
    assert result == existing_job_application.id
