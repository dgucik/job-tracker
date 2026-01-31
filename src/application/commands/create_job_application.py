from pydantic import BaseModel, Field

from application.mappers.job_application import job_application_to_dto
from application.ports import CommandHandler, UnitOfWork
from application.dtos import JobApplicationDTO
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.value_objects.compensation import Compensation, EmploymentType
from domain.value_objects.work_location import WorkLocation, WorkModel


class RawCompensation(BaseModel):
    min_salary: int | None = Field(default=None, examples=[5000], ge=0)
    max_salary: int | None = Field(default=None, examples=[8000], ge=0)
    currency: str | None = Field(default=None, examples=["USD"])
    employment_type: str = Field(examples=["B2B"])


class CreateJobApplicationCommand(BaseModel):
    company_name: str = Field(min_length=1, max_length=255, examples=["Google"])
    role_name: str = Field(min_length=1, max_length=255, examples=["Software Engineer"])
    posting_url: str = Field(examples=["https://www.google.com"])
    status: str = Field(examples=["APPLIED"])
    work_model: WorkModel = Field(examples=["REMOTE"])
    work_location: str | None = Field(default=None, examples=["Warsaw"])
    compensations: list[RawCompensation] = Field(default_factory=list)
    notes: str | None = Field(default=None, examples=["Exciting opportunity"])


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
