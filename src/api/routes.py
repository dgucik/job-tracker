from fastapi import APIRouter, Body, Depends, status

from api.dependencies.command_bus import get_command_bus
from application.ports import CommandBus, QueryBus
from application.queries.get_job_application_list import GetJobApplicationListQuery
from api.dependencies.query_bus import get_query_bus
from application.dtos import JobApplicationDTO
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
