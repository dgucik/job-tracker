import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def uow():
    uow = AsyncMock()
    uow.job_applications = AsyncMock()
    uow.commit = AsyncMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    return uow
