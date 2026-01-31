from domain.entities.job_application import JobApplication

from application.queries.dtos import (
    CompensationItemDTO,
    JobApplicationItemDTO,
)


def job_application_to_list_item_dto(
    entity: JobApplication,
) -> JobApplicationItemDTO:
    return JobApplicationItemDTO(
        id=entity.id,
        company_name=entity.company_name,
        role_name=entity.role_name,
        posting_url=entity.posting_url,
        status=entity.status.value,
        work_model=entity.work_location.work_model.name,
        work_location=entity.work_location.location,
        compensations=[
            CompensationItemDTO(
                min_salary=c.min_salary,
                max_salary=c.max_salary,
                currency=c.currency,
                employment_type=c.employment_type.name,
            )
            for c in entity.compensations
        ],
        notes=entity.notes,
    )
