import logging
from dataclasses import dataclass
from uuid import UUID

from application.ports import CommandHandler, UnitOfWork
from domain.entities.job_application import ApplicationStatus, JobApplication
from domain.value_objects.compensation import Compensation, EmploymentType
from domain.value_objects.work_location import WorkLocation, WorkModel

logger = logging.getLogger(__name__)


@dataclass
class RawCompensation:
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


@dataclass
class CreateJobApplicationCommand:
    company_name: str
    role_name: str
    posting_url: str
    status: str
    work_model: str
    work_location: str | None
    compensations: list[RawCompensation]
    notes: str | None


class CreateJobApplicationCommandHandler(
    CommandHandler[CreateJobApplicationCommand, UUID]
):
    """
    Handler for creating a job application.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: CreateJobApplicationCommand) -> UUID:
        work_location = WorkLocation(
            work_model=WorkModel(command.work_model),
            location=command.work_location,
        )
        compensations = [
            Compensation(
                min_salary=c.min_salary,
                max_salary=c.max_salary,
                currency=c.currency,
                employment_type=EmploymentType(c.employment_type),
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
        logger.info(
            "Job application created",
            extra={
                "job_application_id": str(job_application.id),
                "company": command.company_name,
            },
        )
        return job_application.id
