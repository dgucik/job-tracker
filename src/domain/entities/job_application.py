from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, UTC, date

from domain.exceptions import CompensationException
from domain.value_objects.compensation import Compensation
from domain.value_objects.work_location import WorkLocation


class ApplicationStatus(Enum):
    APPLIED = "APPLIED"
    INTERVIEWED = "INTERVIEWED"
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass
class JobApplication:
    """
    Represents a job application entity with relevant details.

    Attributes:
        id: Unique identifier for the job application.
        applied_at: Timestamp when the application was created.
        company_name: Name of the company applied to.
        role_name: Name of the role applied for.
        posting_url: URL of the job posting.
        status: Current status of the application.
        work_location: WorkLocation object containing work model and location.
        compensations: List of Compensation objects.
        notes: Additional notes regarding the application.
    """

    id: UUID
    applied_at: date = field(
        default_factory=lambda: datetime.now(UTC).date(), init=False
    )
    company_name: str
    role_name: str
    posting_url: str
    status: ApplicationStatus
    work_location: WorkLocation
    compensations: list[Compensation]
    notes: str | None = None

    @classmethod
    def create(
        cls,
        company_name: str,
        role_name: str,
        posting_url: str,
        status: ApplicationStatus,
        work_location: WorkLocation,
        compensations: list[Compensation],
        notes: str | None = None,
    ) -> "JobApplication":
        """
        Factory method to create a new JobApplication instance.

        Args:
            id: Unique identifier for the job application.
            company_name: Name of the company applied to.
            role_name: Name of the role applied for.
            posting_url: URL of the job posting.
            status: Current status of the application.
            work_location: WorkLocation object containing work model and location.
            compensations: List of Compensation objects.
            notes: Additional notes regarding the application.

        Returns:
            A new instance of JobApplication.
        """

        obj = cls(
            id=uuid4(),
            company_name=company_name,
            role_name=role_name,
            posting_url=posting_url,
            status=status,
            work_location=work_location,
            compensations=[],
            notes=notes,
        )
        for compensation in compensations:
            obj._add_compensation(compensation)

        return obj

    def _add_compensation(self, compensation: Compensation) -> None:
        """
        Add a Compensation object to the job application.

        Args:
            compensation: The Compensation object to add.

        Raises:
            CompensationException: If a compensation with the same employment type already exists.
        """
        if compensation.employment_type in [
            c.employment_type for c in self.compensations
        ]:
            raise CompensationException(
                f"Compensation with employment {compensation.employment_type.name} already exists."
            )
        self.compensations.append(compensation)

    def update_status(self, new_status: ApplicationStatus) -> None:
        """
        Update the status of the job application.

        Args:
            new_status: The new status to set for the application.
        """
        self.status = new_status

    def add_notes(self, notes: str | None) -> None:
        """
        Add notes to the job application.

        Args:
            notes: The notes to add to the application.
        """
        self.notes = notes
