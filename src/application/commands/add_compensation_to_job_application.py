from uuid import UUID

from application.dtos import JobApplicationDTO
from application.mappers.job_application import job_application_to_dto
from application.ports import CommandHandler, UnitOfWork
from domain.exceptions import JobApplicationNotFoundException
from domain.value_objects.compensation import Compensation, EmploymentType
from pydantic import BaseModel


class AddCompensationToJobApplicationCommand(BaseModel):
    job_application_id: UUID
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


class AddCompensationToJobApplicationCommandHandler(
    CommandHandler[AddCompensationToJobApplicationCommand, JobApplicationDTO]
):
    """
    Handler for adding a compensation to a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, command: AddCompensationToJobApplicationCommand
    ) -> JobApplicationDTO:
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
        return job_application_to_dto(job_application)
