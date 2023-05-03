"""
Scheduler Service Gateway
"""
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.events.scheduler_service import MeetingScheduled
from app.domain.schemas import ResponseModel, ResponseModels
from app.service_layer.gateway import api_v1_url, get_service, verify_status

router = APIRouter(prefix="/scheduler-service", tags=["Scheduler"])


@router.get("/schedules",
            status_code=HTTP_200_OK,
            summary="Finds all schedules",
            tags=["Queries"]
            )
async def query_schedules(
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModels[MeetingScheduled]:
    """
    Retrieves schedules from the Database.
    """

    service = await get_service(service_name="scheduler", services=services)

    response, code = await gateway(service_url=service.base_url, path=f"{api_v1_url}/schedules",
                                   client=client, method="GET")

    verify_status(response=response, status_code=code)

    return ResponseModels[MeetingScheduled](**response)


@router.get("/schedules/{schedule_id}",
            status_code=HTTP_200_OK,
            summary="Finds schedule by id",
            tags=["Queries"]
            )
async def query_schedule_by_id(
        schedule_id: str,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    """
    Retrieves a specific schedule from the Database.
    """

    service = await get_service(service_name="scheduler", services=services)

    response, code = await gateway(service_url=service.base_url, path=f"{api_v1_url}/schedules/{schedule_id}",
                                   client=client, method="GET")

    verify_status(response=response, status_code=code)

    return ResponseModel[MeetingScheduled](**response)
