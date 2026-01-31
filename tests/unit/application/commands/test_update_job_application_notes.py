import pytest
from types import SimpleNamespace
from uuid import uuid4

from application.commands.update_job_application_notes import (
    UpdateJobApplicationNotesCommandHandler,
)
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.exceptions import JobApplicationNotFoundException
from domain.value_objects.work_location import WorkLocation, WorkModel


@pytest.fixture
def job_application_with_notes():
    return JobApplication.create(
        company_name="Tech Corp",
        role_name="Engineer",
        posting_url="https://example.com/job",
        status=ApplicationStatus.APPLIED,
        work_location=WorkLocation(work_model=WorkModel.REMOTE, location=None),
        compensations=[],
        notes="Initial notes",
    )


@pytest.fixture
def handler(uow):
    return UpdateJobApplicationNotesCommandHandler(uow)


@pytest.mark.asyncio
async def test_execute_updates_notes_and_commits(
    handler, uow, job_application_with_notes
):
    app_id = job_application_with_notes.id
    uow.job_applications.get_by_id.return_value = job_application_with_notes

    command = SimpleNamespace(
        job_application_id=app_id,
        notes="Updated notes after interview",
    )

    await handler.execute(command)

    uow.job_applications.get_by_id.assert_called_once_with(app_id)
    assert job_application_with_notes.notes == "Updated notes after interview"
    uow.commit.assert_called_once()


@pytest.mark.asyncio
async def test_execute_raises_when_application_not_found(handler, uow):
    app_id = uuid4()
    uow.job_applications.get_by_id.return_value = None

    command = SimpleNamespace(
        job_application_id=app_id,
        notes="Some notes",
    )

    with pytest.raises(JobApplicationNotFoundException) as exc_info:
        await handler.execute(command)

    assert str(app_id) in str(exc_info.value)
    uow.commit.assert_not_called()
