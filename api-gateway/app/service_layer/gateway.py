"""
Gateway Service functions.
"""
from typing import Any

from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.adapters.http_client import AsyncHttpClient
from app.adapters.network import gateway
from app.domain.models import Service

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
