from uuid import UUID

from application.ports import CommandHandler, UnitOfWork
from domain.exceptions import JobApplicationNotFoundException


class UpdateJobApplicationNotesCommand:
    job_application_id: UUID
    notes: str


class UpdateJobApplicationNotesCommandHandler(
    CommandHandler[UpdateJobApplicationNotesCommand]
):
    """
    Handler for updating the notes of a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: UpdateJobApplicationNotesCommand) -> None:
        """
        Execute the command.

        Args:
            command: The command to execute.
        """
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
