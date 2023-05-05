"""
Gateway Service functions.
"""
from typing import Any

from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_409_CONFLICT, HTTP_503_SERVICE_UNAVAILABLE

from app.adapters.http_client import AsyncHttpClient
from app.adapters.network import gateway
from app.domain.commands.scheduler_service import ScheduleMeeting
from app.domain.events.auth_service import UserRegistered
from app.domain.models import Service
from app.domain.schemas import ResponseModels

api_v1_url = "/api/v1"


def verify_status(response: dict[str, Any],
                  status_code: int,
                  default_err_msg: str = "Unknown error.",
                  status_codes: list[int] | None = None
                  ):
    """
    Verify response.

    Args:
        response (dict[str, Any]): The response.
        status_code (int): The status code.
        default_err_msg (str): The default error message.
        status_codes (tuple[int, ...]): The status codes to verify.

    Raises:
        HTTPException: If the status code is not 200.
    """

    if status_codes is None:
        status_codes = [HTTP_200_OK, ]

    if status_code not in status_codes:
        raise HTTPException(status_code=status_code, detail=response.get("detail", default_err_msg))


async def get_service(service_name: str, services: list[Service]) -> Service:
    """
    Get user service.

    Args:
        service_name (str): The name of the service.
        services (list[Service]): The list of services.

    Returns:
        Service: The service.

    Raises:
        HTTPException: If the service is not found.
    """
    [service] = [service for service in services if service.name.lower() == service_name.lower()]

    if not service:
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=f"{service_name} service unavailable.")

    return service


async def get_users(users: str, service: Service, client: AsyncHttpClient) -> tuple[dict[str, Any], int]:
    """
    Get users.

    Args:
        users (str): The usernames for filtering.
        service (Service): The service.
        client (AsyncHttpClient): The Async HTTP Client.

    Returns:
        tuple[dict[str, Any], int]: The response and the status code.
    """
    params = {"users": users.strip()} if users else None

    return await gateway(service_url=service.base_url, path=f"{api_v1_url}/users", query_params=params,
                         client=client, method="GET")


async def verify_scheduling_meeting(command: ScheduleMeeting,
                                    service: Service,
                                    client: AsyncHttpClient) -> ScheduleMeeting:
    """
    Verify scheduling meeting command by checking if the users exists.

    Updates the command with the verified guests: all non-existing guests are removed.

    Args:
        command (ScheduleMeeting): The schedule command.
        service (Service): The service.
        client (AsyncHttpClient): The Async HTTP Client.

    Returns:
        ScheduleMeeting: The schedule command with guests verified.

    Raises:
        HTTPException: If the organizer does not exist.
    """
    user_set = command.guests.copy()
    user_set.add(command.organizer)

    comma_separated_usernames = ", ".join(user_set)

    response, code = await get_users(users=comma_separated_usernames, service=service, client=client)

    verify_status(response=response, status_code=code)

    response_event = ResponseModels[UserRegistered](**response)

    usernames = [user.username for user in response_event.data]

    if command.organizer not in usernames:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="Organizer does not exists.")

    usernames.remove(command.organizer)

    return command.copy(update={"guests": set(usernames)})
