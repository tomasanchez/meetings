"""
Scheduler Service Gateway
"""
from typing import Annotated

from fastapi import APIRouter, Path, Request, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.adapters.http_client import AsyncHttpClient
from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.commands.scheduler_service import JoinMeeting, ScheduleMeeting, ToggleVoting, VoteOption
from app.domain.events.scheduler_service import MeetingScheduled
from app.domain.models import Service
from app.domain.schemas import ResponseModel, ResponseModels
from app.service_layer.gateway import api_v1_url, get_service, verify_scheduling_meeting, verify_status, \
    verify_user_existence

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


@router.patch("/schedules/{schedule_id}/voting",
              status_code=HTTP_200_OK,
              summary="Toggles voting on a schedule",
              tags=["Commands"],
              )
async def toggle_voting(
        schedule_id: Annotated[str, Path(description="The schedule's id.", example="b455f6t63t7")],
        command: ToggleVoting,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    """
    Toggles voting on a schedule.
    """
    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="scheduler", services=services)).base_url,
        path=f"{api_v1_url}/schedules/{schedule_id}/voting",
        client=client,
        method="PATCH",
        request_body=command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_200_OK])

    return ResponseModel[MeetingScheduled](**service_response)


@router.patch("/schedules/{schedule_id}/relationships/guests",
              status_code=HTTP_200_OK,
              summary="Adds a guest to a schedule",
              tags=["Commands"],
              )
async def join_meeting(
        schedule_id: Annotated[str, Path(description="The schedule's id.", example="b455f6t63t7")],
        command: JoinMeeting,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    """
    Allows a valid user to join a meeting.
    """
    return await command_with_user_validation(
        path=f"{schedule_id}/relationships/guests",
        command=command,
        services=services,
        client=client,
    )


@router.patch("/schedules/{schedule_id}/options",
              status_code=HTTP_200_OK,
              summary="Votes for an option",
              tags=["Commands"],
              )
async def vote_for_option(
        schedule_id: Annotated[str, Path(description="The schedule's id.", example="b455f6t63t7")],
        command: VoteOption,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    return await command_with_user_validation(
        path=f"{schedule_id}/options",
        command=command,
        services=services,
        client=client,
    )


########################################################################################################################
# Helper functions
########################################################################################################################

async def command_with_user_validation(
        path: str,
        command: JoinMeeting | VoteOption,
        services: list[Service],
        client: AsyncHttpClient,
        method: str = "PATCH",
) -> ResponseModel[MeetingScheduled]:
    """
    Validates the user and then sends the command to the scheduler service.
    """
    await verify_user_existence(username=command.username,
                                client=client,
                                service=await get_service(service_name="auth", services=services),
                                )

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="scheduler", services=services)).base_url,
        client=client,
        path=f"{api_v1_url}/schedules/{path}",
        method=method,
        request_body=command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_200_OK])

    return ResponseModel[MeetingScheduled](**service_response)
