"""
Scheduler Service Gateway
"""
from typing import Annotated

from fastapi import APIRouter, Path, Request, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.commands.scheduler_service import ScheduleMeeting
from app.domain.events.scheduler_service import MeetingScheduled
from app.domain.schemas import ResponseModel, ResponseModels
from app.service_layer.gateway import api_v1_url, get_service, verify_scheduling_meeting, verify_status

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
        schedule_id: Annotated[str, Path(description="The schedule's id.", example="b455f6t63t7")],
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


@router.post("/schedules",
             status_code=HTTP_201_CREATED,
             summary="Creates a schedule",
             tags=["Commands"],
             )
async def schedule(
        command: ScheduleMeeting,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
        request: Request,
        response: Response,
) -> ResponseModel[MeetingScheduled]:
    """
    Schedules a meeting.
    """

    updated_command = await verify_scheduling_meeting(command=command,
                                                      service=await get_service(service_name="auth",
                                                                                services=services),
                                                      client=client)

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="scheduler", services=services)).base_url,
        path=f"{api_v1_url}/schedules",
        client=client,
        method="POST",
        request_body=updated_command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_201_CREATED])

    response_body = ResponseModel[MeetingScheduled](**service_response)

    response.headers["Location"] = f"{request.base_url}api/v1/scheduler-service/schedules/{response_body.data.id}"

    return response_body
