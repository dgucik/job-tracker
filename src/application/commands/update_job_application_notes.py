from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from application.mappers.job_application import job_application_to_dto
from application.ports import CommandHandler, UnitOfWork
from application.dtos import JobApplicationDTO
from domain.exceptions import JobApplicationNotFoundException


class UpdateJobApplicationNotesCommand(BaseModel):
    job_application_id: UUID = Field(examples=[uuid4()])
    notes: str = Field(examples=["Exciting opportunity"])


class UpdateJobApplicationNotesCommandHandler(
    CommandHandler[UpdateJobApplicationNotesCommand, JobApplicationDTO]
):
    """
    Handler for updating the notes of a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, command: UpdateJobApplicationNotesCommand
    ) -> JobApplicationDTO:
        async with self._uow:
            job_application = await self._uow.job_applications.get_by_id(
                command.job_application_id
            )
            if not job_application:
                raise JobApplicationNotFoundException(
                    f"Job application with id {command.job_application_id} not found"
                )
            job_application.add_notes(command.notes)
            await self._uow.commit()
        return job_application_to_dto(job_application)
