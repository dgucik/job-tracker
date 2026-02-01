from dataclasses import dataclass
from uuid import UUID


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
    status: str
    work_model: str
    work_location: str | None
    compensations: list[CompensationListItemDTO]
    notes: str | None
