from typing import Any
from uuid import UUID
from domain.entities.job_application import JobApplication
from domain.repositories import JobApplicationRepository
from infrastructure.exceptions import EntityNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, Select, select
from sqlalchemy.orm import selectinload

from domain.value_objects.compensation import Compensation
from domain.value_objects.work_location import WorkLocation
from infrastructure.db.models import JobApplicationModel, JobCompensationModel


class SqlAlchemyJobApplicationRepository(JobApplicationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, entity: JobApplication) -> None:
        model = self._to_model(entity)
        self._session.add(model)

    async def get_all(self) -> list[JobApplication]:
        stmt = select(JobApplicationModel).options(
            selectinload(JobApplicationModel.compensations)
        )
        return await self._execute_many(stmt)

    async def get_by_id(self, id: UUID) -> JobApplication | None:
        stmt = (
            select(JobApplicationModel)
            .where(JobApplicationModel.id == id)
            .options(selectinload(JobApplicationModel.compensations))
        )
        return await self._execute_scalar(stmt)

    async def update(self, entity: JobApplication) -> None:
        model = await self._get_model_or_raise(entity.id)
        self._apply_entity_to_model(model, entity)

    async def delete(self, entity: JobApplication) -> None:
        model = await self._get_model_or_raise(entity.id)
        await self._session.delete(model)

    def _to_domain(self, model: JobApplicationModel) -> JobApplication:
        return JobApplication(
            id=model.id,
            company_name=model.company_name,
            role_name=model.role_name,
            posting_url=model.posting_url,
            status=model.status,
            work_location=WorkLocation(
                work_model=model.work_model,
                location=model.location,
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
            compensations=[
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

    def _apply_entity_to_model(
        self, model: JobApplicationModel, entity: JobApplication
    ) -> None:
        model.company_name = entity.company_name
        model.role_name = entity.role_name
        model.posting_url = entity.posting_url
        model.status = entity.status
        model.work_model = entity.work_location.work_model
        model.location = entity.work_location.location
        model.notes = entity.notes

    async def _get_model_or_raise(self, id: UUID) -> JobApplicationModel:
        model = await self._session.get(JobApplicationModel, id)
        if model is None:
            raise EntityNotFoundError(f"Job application with id {id} not found")
        return model

    async def _execute_scalar(self, stmt: Select[Any]) -> JobApplication | None:
        result: Result[Any] = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def _execute_many(self, stmt: Select[Any]) -> list[JobApplication]:
        result: Result[Any] = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]
