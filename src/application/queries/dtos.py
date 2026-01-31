from uuid import UUID

from pydantic import BaseModel


class CompensationItemDTO(BaseModel):
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


class JobApplicationItemDTO(BaseModel):
    id: UUID
    company_name: str
    role_name: str
    posting_url: str
    status: str
    work_model: str
    work_location: str | None
    compensations: list[CompensationItemDTO]
    notes: str | None
