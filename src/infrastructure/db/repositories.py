from typing import Any
from uuid import UUID
from domain.entities.job_application import JobApplication
from domain.repositories import JobApplicationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, Select, select

from domain.value_objects.compensation import Compensation
from domain.value_objects.work_location import WorkLocation
from infrastructure.db.models import JobApplicationModel, JobCompensationModel


class SqlAlchemyJobApplicationRepository(JobApplicationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, entity: JobApplication) -> None:
        """
        Adds a new JobApplication entity to the database.

        Args:
            entity: The JobApplication entity to add.
        """
        model = self._to_model(entity)
        self._session.add(model)

    async def get_by_id(self, id: UUID) -> JobApplication | None:
        """
        Retrieves a JobApplication entity by its ID.

        Args:
            id: The unique identifier of the JobApplication.

        Returns:
            The JobApplication entity if found, else None.
        """
        stmt = select(JobApplicationModel).where(JobApplicationModel.id == id)
        return await self._execute(stmt)

    async def update(self, entity: JobApplication) -> None:
        """
        Updates an existing JobApplication entity in the database.

        Args:
            entity: The JobApplication entity to update.
        """
        model = self._to_model(entity)
        await self._session.merge(model)

    async def delete(self, entity: JobApplication) -> None:
        """
        Deletes a JobApplication entity from the database.

        Args:
            entity: The JobApplication entity to delete.
        """
        model = self._to_model(entity)
        await self._session.delete(model)

    def _to_domain(self, model: JobApplicationModel) -> JobApplication:
        return JobApplication(
            id=model.id,
            company_name=model.company_name,
            role_name=model.role_name,
            posting_url=model.posting_url,
            status=model.status,
            work_location=WorkLocation(
                work_model=model.work_model, location=model.location
            ),
            compensations=[
                Compensation(
                    min_salary=comp.min_salary,
                    max_salary=comp.max_salary,
                    currency=comp.currency,
                    employment_type=comp.employment_type,
                )
                for comp in model.compensations
            ],
            notes=model.notes,
        )

    def _to_model(self, entity: JobApplication) -> JobApplicationModel:
        model = JobApplicationModel(
            id=entity.id,
            company_name=entity.company_name,
            role_name=entity.role_name,
            posting_url=entity.posting_url,
            status=entity.status,
            work_model=entity.work_location.work_model,
            location=entity.work_location.location,
            compensation=[
                JobCompensationModel(
                    min_salary=comp.min_salary,
                    max_salary=comp.max_salary,
                    currency=comp.currency,
                    employment_type=comp.employment_type,
                )
                for comp in entity.compensations
            ],
            notes=entity.notes,
        )
        return model

    async def _execute(self, stmt: Select[Any]) -> JobApplication | None:
        result: Result[Any] = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
