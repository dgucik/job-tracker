from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from application.ports import QueryBus
from application.queries.get_job_application_list import GetJobApplicationListQuery
from api.dependencies.query_bus import get_query_bus
from application.queries.dtos import JobApplicationListItemDTO

router = APIRouter()


@router.get("/")
async def get_job_application_list(
    query_bus: QueryBus = Depends(get_query_bus),
) -> JSONResponse:
    query = GetJobApplicationListQuery()
    result: list[JobApplicationListItemDTO] = await query_bus.execute(query)
    return result
