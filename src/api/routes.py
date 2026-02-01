from uuid import UUID
from fastapi import APIRouter, Body, Depends, status

from api.dependencies.command_bus import get_command_bus
from api.mappers import (
    job_application_dto_to_response,
    job_application_request_to_command,
)
from api.schemas.requests import CreateJobApplicationRequest
from api.schemas.responses import (
    JobApplicationIdResponse,
    JobApplicationListItemResponse,
)
from application.ports import CommandBus, QueryBus
from application.queries.dtos import JobApplicationListItemDTO
from application.queries.get_job_application_list import GetJobApplicationListQuery
from api.dependencies.query_bus import get_query_bus
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
    job_application_id: UUID = await command_bus.execute(command)
    return JobApplicationIdResponse(id=job_application_id)
