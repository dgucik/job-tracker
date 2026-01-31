from dataclasses import dataclass
from uuid import UUID

from application.ports import Command, CommandHandler, UnitOfWork
from domain.exceptions import JobApplicationNotFoundException
from domain.value_objects.compensation import Compensation, EmploymentType


@dataclass
class AddCompensationToJobApplicationCommand(Command):
    job_application_id: UUID
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


class AddCompensationToJobApplicationCommandHandler(
    CommandHandler[AddCompensationToJobApplicationCommand]
):
    """
    Handler for adding a compensation to a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: AddCompensationToJobApplicationCommand) -> None:
        compensation = Compensation(
            min_salary=command.min_salary,
            max_salary=command.max_salary,
            currency=command.currency,
            employment_type=EmploymentType[command.employment_type],
        )
        async with self._uow:
            job_application = await self._uow.job_applications.get_by_id(
                command.job_application_id
            )
            if not job_application:
                raise JobApplicationNotFoundException(
                    f"Job application with id {command.job_application_id} not found"
                )
            job_application.add_compensation(compensation)
            await self._uow.commit()
