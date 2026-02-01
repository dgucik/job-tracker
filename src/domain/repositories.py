from typing import Protocol
from uuid import UUID

from domain.entities.job_application import JobApplication


class JobApplicationRepository(Protocol):
    """
    Repository interface for managing JobApplication entities.
    Defines async CRUD operations for job applications.
    """

    async def add(self, entity: JobApplication) -> None:
        """
        Add a new JobApplication entity to the repository.

        Args:
            entity: The JobApplication instance to add.
        """
        ...

    async def get_all(self) -> list[JobApplication]:
        """
        Retrieve all JobApplication entities from the repository.

        Returns:
            A list of JobApplication instances.
        """
        ...

    async def get_by_id(self, id: UUID) -> JobApplication | None:
        """
        Retrieve a JobApplication by its unique identifier.

        Args:
            id: The UUID of the JobApplication.

        Returns:
            The JobApplication instance if found, otherwise None.
        """
        ...

    async def update(self, entity: JobApplication) -> None:
        """
        Update an existing JobApplication entity in the repository.

        Args:
            entity: The JobApplication instance with updated data.
        """
        ...

    async def delete(self, id: UUID) -> None:
        """
        Delete a JobApplication entity from the repository.

        Args:
            id: The UUID of the JobApplication to delete.
        """
        ...
