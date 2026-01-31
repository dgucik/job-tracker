from application.mappers.job_application import job_application_to_list_item_dto
from application.ports import Query, QueryHandler, UnitOfWork
from application.queries.dtos import JobApplicationItemDTO


class GetJobApplicationListQuery(Query):
    pass


class GetJobApplicationListQueryHandler(
    QueryHandler[GetJobApplicationListQuery, list[JobApplicationItemDTO]]
):
    """
    Handler for getting a list of job applications.

    Attributes:\
        _uow: The unit of work to use to access the database.
    """

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, query: GetJobApplicationListQuery
    ) -> list[JobApplicationItemDTO]:
        async with self._uow:
            job_applications = await self._uow.job_applications.get_all()
        job_application_list_items = [
            job_application_to_list_item_dto(job_application)
            for job_application in job_applications
        ]
        return job_application_list_items
