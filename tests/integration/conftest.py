from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from api.dependencies.unit_of_work import get_unit_of_work
from infrastructure.db.uow import SqlAlchemyUnitOfWork
from main import create_app


def _get_async_database_url(container: PostgresContainer) -> str:
    """Convert postgres URL to asyncpg dialect for SQLAlchemy."""
    url = container.get_connection_url(driver=None)
    return url.replace("postgresql://", "postgresql+asyncpg://", 1)


def _run_migrations(database_url: str) -> None:
    """Run Alembic migrations against the given database URL."""
    from alembic import command
    from alembic.config import Config

    # conftest.py is in tests/integration/ -> parent.parent.parent = project root
    project_root = Path(__file__).resolve().parent.parent.parent
    alembic_ini = project_root / "alembic.ini"
    script_location = project_root / "alembic"
    cfg = Config(str(alembic_ini))
    cfg.set_main_option("script_location", str(script_location))
    cfg.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(cfg, "head")


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL in Docker once per test session (Testcontainers)."""
    with PostgresContainer(
        image="postgres:15-alpine",
        driver=None,
    ) as container:
        yield container


@pytest.fixture(scope="session")
def database_url(postgres_container: PostgresContainer) -> str:
    """Async database URL for the test PostgreSQL container."""
    return _get_async_database_url(postgres_container)


@pytest.fixture(scope="session")
def test_engine(database_url: str):
    """Async SQLAlchemy engine bound to the test database (session scope for reuse)."""
    engine = create_async_engine(
        database_url,
        echo=False,
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Session factory for the test database."""
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


@pytest.fixture(scope="session")
def run_migrations(database_url: str) -> None:
    """Run Alembic migrations on the test database (once per session)."""
    _run_migrations(database_url)


@pytest.fixture
def test_engine_per_test(database_url: str):
    """
    Fresh async engine per test to avoid event loop mismatch.
    Session-scoped engine is created in sync context; each test runs in its own loop.
    """
    engine = create_async_engine(
        database_url,
        echo=False,
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture
def test_session_factory_per_test(test_engine_per_test):
    """Session factory per test (same event loop as the test)."""
    return async_sessionmaker(
        bind=test_engine_per_test,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


@pytest.fixture
def app(
    test_session_factory_per_test: async_sessionmaker[AsyncSession],
    run_migrations: None,
):
    """
    FastAPI app with dependencies overridden to use test database.

    Migrations are run before the app is used (via run_migrations fixture).
    """
    app = create_app()

    def get_test_uow():
        uow = SqlAlchemyUnitOfWork(test_session_factory_per_test)
        yield uow

    app.dependency_overrides[get_unit_of_work] = get_test_uow
    return app


@pytest.fixture
async def clean_database(test_engine_per_test):
    """Clean database tables before and after each test for isolation."""
    # Cleanup before test
    async with test_engine_per_test.begin() as conn:
        await conn.execute(
            text("TRUNCATE TABLE job_compensations, job_applications CASCADE")
        )

    yield

    # Cleanup after test
    async with test_engine_per_test.begin() as conn:
        await conn.execute(
            text("TRUNCATE TABLE job_compensations, job_applications CASCADE")
        )


@pytest.fixture
async def client(app, clean_database):
    """Async HTTP client for integration tests (fresh for each test)."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
