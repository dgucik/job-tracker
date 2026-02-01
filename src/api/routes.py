from uuid import UUID
from fastapi import APIRouter, Body, Depends, status

from api.dependencies.command_bus import get_command_bus
from api.schemas.mappers import job_application_dto_to_response
from api.schemas.responses import JobApplicationListItemResponse
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
from application.queries.dtos import JobApplicationListItemDTO
from application.commands.create_job_application import CreateJobApplicationCommand

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[JobApplicationListItemResponse],
)
async def get_job_application_list(
    query_bus: QueryBus = Depends(get_query_bus),
) -> list[JobApplicationListItemResponse]:
    query = GetJobApplicationListQuery()
    dtos: list[JobApplicationListItemDTO] = await query_bus.execute(query)
    return [job_application_dto_to_response(dto) for dto in dtos]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_job_application(
    command: CreateJobApplicationCommand = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationListItemDTO:
    return await command_bus.execute(command)


@router.patch("/{job_application_id}/status", status_code=status.HTTP_200_OK)
async def update_job_application_status(
    job_application_id: UUID,
    command: UpdateJobApplicationStatusCommand = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationListItemDTO:
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
) -> JobApplicationListItemDTO:
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
