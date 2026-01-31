from pydantic import BaseModel

from application.mappers.job_application import job_application_to_dto
from application.ports import CommandHandler, UnitOfWork
from application.dtos import JobApplicationDTO
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.value_objects.compensation import Compensation, EmploymentType
from domain.value_objects.work_location import WorkLocation, WorkModel


class RawCompensation(BaseModel):
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


class CreateJobApplicationCommand(BaseModel):
    company_name: str
    role_name: str
    posting_url: str
    status: str
    work_model: WorkModel
    work_location: str | None
    compensations: list[RawCompensation]
    notes: str | None = None


class CreateJobApplicationCommandHandler(
    CommandHandler[CreateJobApplicationCommand, JobApplicationDTO]
):
    """
    Handler for creating a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: CreateJobApplicationCommand) -> JobApplicationDTO:
        work_location = WorkLocation(
            work_model=command.work_model,
            location=command.work_location,
        )
        compensations = [
            Compensation(
                min_salary=c.min_salary,
                max_salary=c.max_salary,
                currency=c.currency,
                employment_type=EmploymentType[c.employment_type],
            )
            for c in command.compensations
        ]
        job_application = JobApplication.create(
            company_name=command.company_name,
            role_name=command.role_name,
            posting_url=command.posting_url,
            status=ApplicationStatus(command.status),
            work_location=work_location,
            compensations=compensations,
            notes=command.notes,
        )
        async with self._uow:
            await self._uow.job_applications.add(job_application)
            await self._uow.commit()
        return job_application_to_dto(job_application)
