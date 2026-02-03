from dataclasses import dataclass
import logging
from uuid import UUID

from application.ports import CommandHandler, UnitOfWork
from domain.entities.job_application_document import JobApplicationDocument
from domain.exceptions import JobApplicationNotFoundException

logger = logging.getLogger(__name__)


@dataclass
class UploadJobApplicationDocumentCommand:
    job_application_id: UUID
    filename: str
    content: bytes
    mime_type: str = "application/pdf"


class UploadJobApplicationDocumentCommandHandler(
    CommandHandler[UploadJobApplicationDocumentCommand, UUID]
):
    """
    Handler for uploading a job application document.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, command: UploadJobApplicationDocumentCommand) -> UUID:
        async with self._uow:
            job_application = await self._uow.job_applications.get_by_id(
                command.job_application_id
            )
            if not job_application:
                raise JobApplicationNotFoundException(
                    f"Job application with id {command.job_application_id} not found"
                )
            document = JobApplicationDocument.create(
                filename=command.filename,
                content=command.content,
                mime_type=command.mime_type,
            )
            job_application.add_document(document)
            await self._uow.job_applications.update(job_application)
            await self._uow.commit()
        logger.info(
            "Job application document uploaded",
            extra={"job_application_id": str(command.job_application_id)},
        )
        return job_application.id
