from api.schemas.responses import (
    CompensationListItemResponse,
    JobApplicationListItemResponse,
)
from application.queries.dtos import (
    JobApplicationListItemDTO,
)


def job_application_dto_to_response(
    dto: JobApplicationListItemDTO,
) -> JobApplicationListItemResponse:
    return JobApplicationListItemResponse(
        id=dto.id,
        company_name=dto.company_name,
        role_name=dto.role_name,
        posting_url=dto.posting_url,
        status=dto.status.value,
        work_model=dto.work_model.value,
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
