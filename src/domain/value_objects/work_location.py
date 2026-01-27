from dataclasses import dataclass
from enum import Enum

from domain.exceptions import WorkLocationException


class WorkModel(Enum):
    REMOTE = "REMOTE"
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"


@dataclass(frozen=True)
class WorkLocation:
    """
    Represents the work location details for a job.

    Attributes:
        work_model: Work model for the job (remote, hybrid, onsite).
        location: Location of the job, if applicable.
    """

    work_model: WorkModel
    location: str | None = None

    def __post_init__(self) -> None:
        if self.work_model != WorkModel.REMOTE and not self.location:
            raise WorkLocationException(
                "Location must be provided for HYBRID and ONSITE work models."
            )
