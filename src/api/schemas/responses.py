from uuid import UUID
from pydantic import BaseModel, Field


class CompensationListItemResponse(BaseModel):
    min_salary: int | None = Field(examples=[5000], alias="minSalary")
    max_salary: int | None = Field(examples=[8000], alias="maxSalary")
    currency: str | None = Field(examples=["USD"], alias="currency")
    employment_type: str = Field(examples=["B2B"], alias="employmentType")


class JobApplicationListItemResponse(BaseModel):
    id: UUID
    company_name: str = Field(
        min_length=1, max_length=255, examples=["Google"], alias="companyName"
    )
    role_name: str = Field(
        min_length=1, max_length=255, examples=["Software Engineer"], alias="roleName"
    )
    posting_url: str = Field(examples=["https://www.google.com"], alias="postingUrl")
    status: str = Field(examples=["APPLIED"], alias="status")
    work_model: str = Field(examples=["REMOTE"], alias="workModel")
    work_location: str | None = Field(
        default=None, examples=["Warsaw"], alias="workLocation"
    )
    compensations: list[CompensationListItemResponse] = Field(
        default_factory=list, alias="compensations"
    )
    notes: str | None = Field(
        default=None, examples=["Exciting opportunity"], alias="notes"
    )
