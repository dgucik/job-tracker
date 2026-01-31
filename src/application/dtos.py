from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.job_application import ApplicationStatus
from domain.value_objects.work_location import WorkModel


class CompensationDTO(BaseModel):
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


class JobApplicationDTO(BaseModel):
    id: UUID
    company_name: str = Field(min_length=1, max_length=255, examples=["Google"])
    role_name: str = Field(min_length=1, max_length=255, examples=["Software Engineer"])
    posting_url: str = Field(examples=["https://www.google.com"])
    status: ApplicationStatus = Field(examples=["APPLIED"])
    work_model: WorkModel = Field(examples=["REMOTE"])
    work_location: str | None = Field(default=None, examples=["Warsaw"])
    compensations: list[CompensationDTO] = Field(default_factory=list)
    notes: str | None = Field(default=None, examples=["Exciting opportunity"])
