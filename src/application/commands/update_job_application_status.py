from dataclasses import dataclass
from uuid import UUID

from application.ports import CommandHandler, UnitOfWork
from domain.entities.job_application import ApplicationStatus
from domain.exceptions import JobApplicationNotFoundException


@dataclass
class UpdateJobApplicationStatusCommand:
    job_application_id: UUID
    new_status: str


class UpdateJobApplicationStatusCommandHandler(
    CommandHandler[UpdateJobApplicationStatusCommand]
):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: UpdateJobApplicationStatusCommand) -> None:
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
