from dataclasses import dataclass
from uuid import UUID

from domain.entities.job_application import ApplicationStatus
from domain.value_objects.work_location import WorkModel


@dataclass
class CompensationListItemDTO:
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


@dataclass
class JobApplicationListItemDTO:
    id: UUID
    company_name: str
    role_name: str
    posting_url: str
    status: ApplicationStatus
    work_model: WorkModel
    work_location: str | None
    compensations: list[CompensationListItemDTO]
    notes: str | None
