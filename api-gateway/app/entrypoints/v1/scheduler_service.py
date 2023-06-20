"""
Scheduler Service Gateway
"""
import logging
from typing import Annotated

from fastapi import APIRouter, Path, Request, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.adapters.http_client import AsyncHttpClient
from app.adapters.network import gateway
from app.adapters.telemetry.prometheus import EVENTS_SCHEDULED
from app.dependencies import AsyncHttpClientDependency, ServiceProvider, app_settings
from app.domain.commands.scheduler_service import ForwardScheduleMeeting, ForwardToggleVoting, ForwardVoteOption, \
    JoinMeeting, \
    ScheduleMeeting, ToggleVoting, \
    VoteOption
from app.domain.events.scheduler_service import MeetingScheduled
from app.domain.models import Service
from app.domain.schemas import ResponseModel, ResponseModels
from app.middleware import AuthMiddleware
from app.service_layer.gateway import api_v1_url, get_service, verify_status

router = APIRouter()


########################################################################################################################
# Queries
########################################################################################################################

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


########################################################################################################################
# Commands
########################################################################################################################

@router.post("/schedules",
             status_code=HTTP_201_CREATED,
             summary="Creates a schedule",
             tags=["Commands"],
             )
async def schedule(
        command: ScheduleMeeting,
        user: AuthMiddleware,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
        request: Request,
        response: Response,
) -> ResponseModel[MeetingScheduled]:
    """
    Schedules a meeting.
    """

    forwarded_command = ForwardScheduleMeeting(organizer=user.username, guests=set(), **command.dict())

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="scheduler", services=services)).base_url,
        path=f"{api_v1_url}/schedules",
        client=client,
        method="POST",
        request_body=forwarded_command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_201_CREATED])

    EVENTS_SCHEDULED.labels(app_name=app_settings.get_app_name()).inc()

    response_body = ResponseModel[MeetingScheduled](**service_response)

    logging.info(f"Event scheduled: {response_body.data.id}")

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
        user: AuthMiddleware,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    """
    Toggles voting on a schedule.
    """
    forwarded_command = ForwardToggleVoting(username=user.username, **command.dict())

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="scheduler", services=services)).base_url,
        path=f"{api_v1_url}/schedules/{schedule_id}/voting",
        client=client,
        method="PATCH",
        request_body=forwarded_command.json()
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
        user: AuthMiddleware,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    """
    Allows a valid user to join a meeting.
    """
    command = JoinMeeting(username=user.username)
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
        user: AuthMiddleware,
        command: VoteOption,
        services: ServiceProvider,
        client: AsyncHttpClientDependency,
) -> ResponseModel[MeetingScheduled]:
    forwarded_command = ForwardVoteOption(username=user.username, **command.dict())

    return await command_with_user_validation(
        path=f"{schedule_id}/options",
        command=forwarded_command,
        services=services,
        client=client,
    )


########################################################################################################################
# Helper functions
########################################################################################################################

async def command_with_user_validation(
        path: str,
        command: JoinMeeting | ForwardVoteOption,
        services: list[Service],
        client: AsyncHttpClient,
        method: str = "PATCH",
) -> ResponseModel[MeetingScheduled]:
    """
    Sends the command to the scheduler service.
    """
    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="scheduler", services=services)).base_url,
        client=client,
        path=f"{api_v1_url}/schedules/{path}",
        method=method,
        request_body=command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_200_OK])

    return ResponseModel[MeetingScheduled](**service_response)
