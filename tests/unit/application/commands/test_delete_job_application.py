import pytest
from uuid import uuid4

from application.commands.delete_job_application import (
    DeleteJobApplicationCommand,
    DeleteJobApplicationCommandHandler,
)
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
    return DeleteJobApplicationCommandHandler(uow)


@pytest.mark.asyncio
async def test_execute_deletes_application_and_commits(
    handler, uow, existing_job_application
):
    app_id = existing_job_application.id
    uow.job_applications.get_by_id.return_value = existing_job_application

    command = DeleteJobApplicationCommand(job_application_id=app_id)

    result = await handler.execute(command)

    uow.job_applications.get_by_id.assert_called_once_with(app_id)
    uow.job_applications.delete.assert_called_once_with(existing_job_application)
    uow.commit.assert_called_once()

    assert result == app_id


@pytest.mark.asyncio
async def test_execute_raises_when_application_not_found(handler, uow):
    app_id = uuid4()
    uow.job_applications.get_by_id.return_value = None

    command = DeleteJobApplicationCommand(job_application_id=app_id)

    with pytest.raises(JobApplicationNotFoundException) as exc_info:
        await handler.execute(command)

    assert str(app_id) in str(exc_info.value)
    uow.job_applications.delete.assert_not_called()
    uow.commit.assert_not_called()
