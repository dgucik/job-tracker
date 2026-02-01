from uuid import UUID
from pydantic import BaseModel, Field


class CompensationListItemResponse(BaseModel):
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


class JobApplicationListItemResponse(BaseModel):
    id: UUID
    company_name: str = Field(min_length=1, max_length=255, examples=["Google"])
    role_name: str = Field(min_length=1, max_length=255, examples=["Software Engineer"])
    posting_url: str = Field(examples=["https://www.google.com"])
    status: str = Field(examples=["APPLIED"])
    work_model: str = Field(examples=["REMOTE"])
    work_location: str | None = Field(default=None, examples=["Warsaw"])
    compensations: list[CompensationListItemResponse] = Field(default_factory=list)
    notes: str | None = Field(default=None, examples=["Exciting opportunity"])
