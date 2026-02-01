from typing import Literal
from pydantic import BaseModel, Field

EMPLOYMENT_TYPE_VALUES = Literal["B2B", "PERMANENT", "CONTRACT"]


class CreateCompensationRequest(BaseModel):
    min_salary: int | None = Field(examples=[5000], alias="minSalary")
    max_salary: int | None = Field(examples=[8000], alias="maxSalary")
    currency: str | None = Field(examples=["USD"], alias="currency")
    employment_type: EMPLOYMENT_TYPE_VALUES = Field(
        examples=["B2B"], alias="employmentType"
    )


STATUS_VALUES = Literal["APPLIED", "INTERVIEWED", "OFFERED", "ACCEPTED", "REJECTED"]
WORK_MODEL_VALUES = Literal["REMOTE", "HYBRID", "ONSITE"]


class CreateJobApplicationRequest(BaseModel):
    company_name: str = Field(
        min_length=1, max_length=255, examples=["Google"], alias="companyName"
    )
    role_name: str = Field(
        min_length=1, max_length=255, examples=["Software Engineer"], alias="roleName"
    )
    posting_url: str = Field(examples=["https://www.google.com"], alias="postingUrl")
    status: STATUS_VALUES = Field(examples=["APPLIED"], alias="status")
    work_model: WORK_MODEL_VALUES = Field(examples=["REMOTE"], alias="workModel")
    work_location: str | None = Field(
        default=None, examples=["Warsaw"], alias="workLocation"
    )
    compensations: list[CreateCompensationRequest] = Field(
        default_factory=list, alias="compensations"
    )
    notes: str | None = Field(
        default=None, examples=["Exciting opportunity"], alias="notes"
    )


class UpdateJobApplicationStatusRequest(BaseModel):
    status: STATUS_VALUES = Field(examples=["APPLIED"], alias="status")


class UpdateJobApplicationNotesRequest(BaseModel):
    notes: str = Field(examples=["Exciting opportunity"], alias="notes")
