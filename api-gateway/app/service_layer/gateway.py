"""
Gateway Service functions.
"""
import logging
from typing import Any

from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.adapters.http_client import AsyncHttpClient
from app.adapters.network import gateway
from app.domain.events.auth_service import UserRegistered
from app.domain.models import Service
from app.domain.schemas import ResponseModel

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
        logging.error("%s", response.get("detail", default_err_msg))
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
        logging.error("%s service unavailable.", service_name)
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
    params = {"usernames": users.strip()} if users else None

    return await gateway(service_url=service.base_url, path=f"{api_v1_url}/users", query_params=params,
                         client=client, method="GET")


async def verify_user_existence(username: str,
                                service: Service,
                                client: AsyncHttpClient) -> UserRegistered:
    """
    Verifies if a user exists

    Args:
        username: to verify
        service: service which validates users
        client: HTTP client to make requests

    Returns:
        UserRegistered: the user if it exists

    Raises:
        HTTPException: If the user does not exist, or service error.
    """
    response, code = await gateway(
        service_url=service.base_url,
        path=f"{api_v1_url}/users/{username}",
        client=client,
        method="GET"
    )

    verify_status(response=response, status_code=code)

    response_event = ResponseModel[UserRegistered](**response)

    return response_event.data
