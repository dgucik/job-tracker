from dataclasses import dataclass
from application.queries.mappers import job_application_entity_to_dto
from application.ports import QueryHandler, UnitOfWork
from application.queries.dtos import JobApplicationDTO


@dataclass
class GetJobApplicationListQuery:
    pass


class GetJobApplicationListQueryHandler(
    QueryHandler[GetJobApplicationListQuery, list[JobApplicationDTO]]
):
    """
    Handler for getting a list of job applications.

    Attributes:
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, query: GetJobApplicationListQuery
    ) -> list[JobApplicationDTO]:
        async with self._uow:
            job_applications = await self._uow.job_applications.get_all()
        job_application_list_items = [
            job_application_entity_to_dto(job_application)
            for job_application in job_applications
        ]
        return job_application_list_items
