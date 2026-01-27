from typing import Protocol
from uuid import UUID

from domain.entities.job_application import JobApplication


class JobApplicationPort(Protocol):
    async def add(self, entity: JobApplication) -> None: ...

    async def get_by_id(self, id: UUID) -> JobApplication | None: ...

    async def update(self, entity: JobApplication) -> None: ...

    async def delete(self, id: UUID) -> None: ...
