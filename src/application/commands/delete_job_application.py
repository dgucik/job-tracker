from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from application.ports import CommandHandler, UnitOfWork


class DeleteJobApplicationCommand(BaseModel):
    job_application_id: UUID = Field(examples=[uuid4()])


class DeleteJobApplicationCommandHandler(
    CommandHandler[DeleteJobApplicationCommand, None]
):
    """
    Handler for deleting a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: DeleteJobApplicationCommand) -> None:
        async with self._uow:
            await self._uow.job_applications.delete(command.job_application_id)
            await self._uow.commit()
        return None
