import pytest
from domain.exceptions import WorkLocationException
from domain.value_objects.work_location import WorkLocation, WorkModel


def test_should_raise_exception_for_missing_location():
    with pytest.raises(WorkLocationException) as exc_info:
        WorkLocation(
            work_model=WorkModel.ONSITE,
        )
    assert (
        str(exc_info.value)
        == "Location must be provided for HYBRID and ONSITE work models."
    )


def test_should_create_work_location_for_remote_model():
    work_location = WorkLocation(
        work_model=WorkModel.REMOTE,
    )
    assert work_location.work_model == WorkModel.REMOTE
    assert work_location.location is None
