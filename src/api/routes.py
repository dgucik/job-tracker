from uuid import UUID
from fastapi import APIRouter, Body, Depends, status

from api.dependencies.command_bus import get_command_bus
from application.commands.delete_job_application import DeleteJobApplicationCommand
from application.commands.update_job_application_notes import (
    UpdateJobApplicationNotesCommand,
)
from application.commands.update_job_application_status import (
    UpdateJobApplicationStatusCommand,
)
from application.ports import CommandBus, QueryBus
from application.queries.get_job_application_list import GetJobApplicationListQuery
from api.dependencies.query_bus import get_query_bus
from application.queries.dtos import JobApplicationDTO
from application.commands.create_job_application import CreateJobApplicationCommand

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[JobApplicationDTO])
async def get_job_application_list(
    query_bus: QueryBus = Depends(get_query_bus),
) -> list[JobApplicationDTO]:
    query = GetJobApplicationListQuery()
    return await query_bus.execute(query)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_job_application(
    command: CreateJobApplicationCommand = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationDTO:
    return await command_bus.execute(command)


@router.patch("/{job_application_id}/status", status_code=status.HTTP_200_OK)
async def update_job_application_status(
    job_application_id: UUID,
    command: UpdateJobApplicationStatusCommand = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationDTO:
    command = UpdateJobApplicationStatusCommand(
        job_application_id=job_application_id,
        new_status=command.new_status,
    )
    return await command_bus.execute(command)


@router.patch("/{job_application_id}/notes", status_code=status.HTTP_200_OK)
async def update_job_application_notes(
    job_application_id: UUID,
    command: UpdateJobApplicationNotesCommand = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationDTO:
    command = UpdateJobApplicationNotesCommand(
        job_application_id=job_application_id,
        notes=command.notes,
    )
    return await command_bus.execute(command)


@router.delete("/{job_application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_application(
    job_application_id: UUID,
    command_bus: CommandBus = Depends(get_command_bus),
) -> None:
    command = DeleteJobApplicationCommand(
        job_application_id=job_application_id,
    )
    return await command_bus.execute(command)
