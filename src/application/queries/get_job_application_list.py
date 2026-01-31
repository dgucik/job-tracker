from dataclasses import dataclass
from uuid import UUID

from application.mappers.job_application import job_application_to_list_item_dto
from application.ports import QueryHandler, UnitOfWork


@dataclass
class CompensationListItemDTO:
    min_salary: int | None
    max_salary: int | None
    currency: str | None
    employment_type: str


@dataclass
class JobApplicationListItemDTO:
    id: UUID
    company_name: str
    role_name: str
    posting_url: str
    status: str
    work_model: str
    work_location: str | None
    compensations: list[CompensationListItemDTO]
    notes: str | None


class GetJobApplicationListQuery:
    pass


class GetJobApplicationListQueryHandler(
    QueryHandler[GetJobApplicationListQuery, list[JobApplicationListItemDTO]]
):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, query: GetJobApplicationListQuery
    ) -> list[JobApplicationListItemDTO]:
        async with self._uow:
            job_applications = await self._uow.job_applications.get_all()
        job_application_list_items = [
            job_application_to_list_item_dto(job_application)
            for job_application in job_applications
        ]
        return job_application_list_items
