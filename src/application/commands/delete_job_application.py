from uuid import UUID
from application.ports import CommandHandler, UnitOfWork
from domain.exceptions import JobApplicationNotFoundException


class DeleteJobApplicationCommand:
    job_application_id: UUID


class DeleteJobApplicationCommandHandler(CommandHandler[DeleteJobApplicationCommand]):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: DeleteJobApplicationCommand) -> None:
        async with self._uow:
            job_application = await self._uow.job_applications.get_by_id(
                command.job_application_id
            )
            if not job_application:
                raise JobApplicationNotFoundException(
                    f"Job application with id {command.job_application_id} not found"
                )
            await self._uow.job_applications.delete(job_application)
            await self._uow.commit()
