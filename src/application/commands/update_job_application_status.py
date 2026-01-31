from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel

from application.mappers.job_application import job_application_to_list_item_dto
from application.ports import CommandHandler, UnitOfWork
from application.queries.dtos import JobApplicationItemDTO
from domain.entities.job_application import ApplicationStatus
from domain.exceptions import JobApplicationNotFoundException


@dataclass
class UpdateJobApplicationStatusCommand(BaseModel):
    job_application_id: UUID
    new_status: str


class UpdateJobApplicationStatusCommandHandler(
    CommandHandler[UpdateJobApplicationStatusCommand, JobApplicationItemDTO]
):
    """
    Handler for updating the status of a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, command: UpdateJobApplicationStatusCommand
    ) -> JobApplicationItemDTO:
        status = ApplicationStatus(command.new_status)
        async with self._uow:
            job_application = await self._uow.job_applications.get_by_id(
                command.job_application_id
            )
            if not job_application:
                raise JobApplicationNotFoundException(
                    f"Job application with id {command.job_application_id} not found"
                )
            job_application.update_status(status)
            await self._uow.commit()
        return job_application_to_list_item_dto(job_application)
