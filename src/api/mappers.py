from api.schemas.requests import CreateJobApplicationRequest
from api.schemas.responses import (
    CompensationListItemResponse,
    JobApplicationListItemResponse,
)
from application.commands.create_job_application import (
    CreateJobApplicationCommand,
    RawCompensation,
)
from application.queries.dtos import JobApplicationListItemDTO


def job_application_dto_to_response(
    dto: JobApplicationListItemDTO,
) -> JobApplicationListItemResponse:
    return JobApplicationListItemResponse(
        id=dto.id,
        company_name=dto.company_name,
        role_name=dto.role_name,
        posting_url=dto.posting_url,
        status=dto.status,
        work_model=dto.work_model,
        work_location=dto.work_location,
        compensations=[
            CompensationListItemResponse(
                min_salary=c.min_salary,
                max_salary=c.max_salary,
                currency=c.currency,
                employment_type=c.employment_type,
            )
            for c in dto.compensations
        ],
        notes=dto.notes,
    )


def job_application_request_to_command(
    request: CreateJobApplicationRequest,
) -> CreateJobApplicationCommand:
    return CreateJobApplicationCommand(
        company_name=request.company_name,
        role_name=request.role_name,
        posting_url=request.posting_url,
        status=request.status,
        work_model=request.work_model,
        work_location=request.work_location,
        compensations=[
            RawCompensation(
                min_salary=c.min_salary,
                max_salary=c.max_salary,
                currency=c.currency,
                employment_type=c.employment_type,
            )
            for c in request.compensations
        ],
        notes=request.notes,
    )
