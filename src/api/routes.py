from uuid import UUID
from fastapi import APIRouter, Body, Depends, status

from api.dependencies.command_bus import get_command_bus
from api.mappers import (
    job_application_dto_to_response,
    job_application_request_to_command,
)
from api.schemas.requests import (
    CreateJobApplicationRequest,
    UpdateJobApplicationNotesRequest,
    UpdateJobApplicationStatusRequest,
)
from api.schemas.responses import (
    JobApplicationIdResponse,
    JobApplicationResponse,
)
from application.commands.delete_job_application import DeleteJobApplicationCommand
from application.commands.update_job_application_notes import (
    UpdateJobApplicationNotesCommand,
)
from application.commands.update_job_application_status import (
    UpdateJobApplicationStatusCommand,
)
from application.ports import CommandBus, QueryBus
from application.queries.dtos import JobApplicationDTO
from application.queries.get_job_application_list import GetJobApplicationListQuery
from api.dependencies.query_bus import get_query_bus
from application.commands.create_job_application import CreateJobApplicationCommand

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[JobApplicationResponse],
)
async def get_job_application_list(
    query_bus: QueryBus = Depends(get_query_bus),
) -> list[JobApplicationResponse]:
    query = GetJobApplicationListQuery()
    dtos: list[JobApplicationDTO] = await query_bus.execute(query)
    return [job_application_dto_to_response(dto) for dto in dtos]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=JobApplicationIdResponse,
)
async def create_job_application(
    body: CreateJobApplicationRequest = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationIdResponse:
    command: CreateJobApplicationCommand = job_application_request_to_command(body)
    created_job_application_id: UUID = await command_bus.execute(command)
    return JobApplicationIdResponse(id=created_job_application_id)


@router.delete(
    "/{job_application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_job_application(
    job_application_id: UUID,
    command_bus: CommandBus = Depends(get_command_bus),
) -> None:
    command = DeleteJobApplicationCommand(job_application_id=job_application_id)
    await command_bus.execute(command)
    return None


@router.put(
    "/{job_application_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=JobApplicationIdResponse,
)
async def update_job_application_status(
    job_application_id: UUID,
    body: UpdateJobApplicationStatusRequest = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationIdResponse:
    command = UpdateJobApplicationStatusCommand(
        job_application_id=job_application_id, status=body.status
    )
    updated_job_application_id: UUID = await command_bus.execute(command)
    return JobApplicationIdResponse(id=updated_job_application_id)


@router.put(
    "/{job_application_id}/notes",
    status_code=status.HTTP_200_OK,
    response_model=JobApplicationIdResponse,
)
async def update_job_application_notes(
    job_application_id: UUID,
    body: UpdateJobApplicationNotesRequest = Body(...),
    command_bus: CommandBus = Depends(get_command_bus),
) -> JobApplicationIdResponse:
    command = UpdateJobApplicationNotesCommand(
        job_application_id=job_application_id, notes=body.notes
    )
    updated_job_application_id: UUID = await command_bus.execute(command)
    return JobApplicationIdResponse(id=updated_job_application_id)
