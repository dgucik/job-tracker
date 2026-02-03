from domain.entities.job_application import JobApplication

from application.queries.dtos import (
    CompensationDTO,
    JobApplicationDTO,
    JobApplicationDocumentDTO,
)
from domain.entities.job_application_document import JobApplicationDocument


def job_application_entity_to_dto(
    entity: JobApplication,
) -> JobApplicationDTO:
    return JobApplicationDTO(
        id=entity.id,
        company_name=entity.company_name,
        role_name=entity.role_name,
        posting_url=entity.posting_url,
        status=entity.status.value,
        work_model=entity.work_location.work_model.value,
        work_location=entity.work_location.location,
        compensations=[
            CompensationDTO(
                min_salary=c.min_salary,
                max_salary=c.max_salary,
                currency=c.currency,
                employment_type=c.employment_type.value,
            )
            for c in entity.compensations
        ],
        notes=entity.notes,
    )


def job_application_document_entity_to_dto(
    entity: JobApplicationDocument,
) -> JobApplicationDocumentDTO:
    return JobApplicationDocumentDTO(
        filename=entity.filename,
        content=entity.content,
        mime_type=entity.mime_type,
    )
