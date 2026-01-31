from typing import List, Optional
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey, Integer, String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from domain.entities.job_application import ApplicationStatus
from domain.value_objects.compensation import EmploymentType


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""

    pass


class JobApplicationModel(Base):
    __tablename__ = "job_applications"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_name: Mapped[str] = mapped_column(String(255), nullable=False)
    posting_url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(
        SQLEnum(ApplicationStatus, native_enum=True), nullable=False
    )
    work_model: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    compensations: Mapped[List["JobCompensationModel"]] = relationship(
        back_populates="job_application", cascade="all, delete-orphan"
    )
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class JobCompensationModel(Base):
    __tablename__ = "job_compensations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    min_salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    employment_type: Mapped[EmploymentType] = mapped_column(
        SQLEnum(EmploymentType, native_enum=True), nullable=False
    )

    job_application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job_applications.id", ondelete="CASCADE"), nullable=False
    )

    job_application: Mapped["JobApplicationModel"] = relationship(
        back_populates="compensations"
    )
