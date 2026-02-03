import logging
from application.ports import QueryHandler, UnitOfWork
from dataclasses import dataclass
from uuid import UUID

from application.queries.dtos import JobApplicationDocumentDTO
from application.queries.mappers import job_application_document_entity_to_dto
from domain.exceptions import (
    JobApplicationDocumentNotFoundException,
    JobApplicationNotFoundException,
)

logger = logging.getLogger(__name__)


@dataclass
class GetJobApplicationDocumentQuery:
    job_application_id: UUID


class GetJobApplicationDocumentQueryHandler(
    QueryHandler[GetJobApplicationDocumentQuery, JobApplicationDocumentDTO]
):
    """
    Handler for getting a job application document.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, query: GetJobApplicationDocumentQuery
    ) -> JobApplicationDocumentDTO:
        async with self._uow:
            job_application = await self._uow.job_applications.get_by_id(
                query.job_application_id
            )
            if not job_application:
                raise JobApplicationNotFoundException(
                    f"Job application with id {query.job_application_id} not found"
                )
            if not job_application.document:
                raise JobApplicationDocumentNotFoundException(
                    f"Job application with id {query.job_application_id} does not have a document"
                )
        logger.info(
            "Job application document retrieved",
            extra={"job_application_id": str(query.job_application_id)},
        )
        return job_application_document_entity_to_dto(job_application.document)
