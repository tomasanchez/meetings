"""
Actuator entrypoint
"""
import asyncio

import aiohttp
from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY, HTTP_503_SERVICE_UNAVAILABLE

from app.adapters.http_client import AsyncHttpClient
from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.events.actuator import ReadinessChecked, StatusChecked
from app.domain.models import Service, ServiceStatus
from app.domain.schemas import ResponseModel

router = APIRouter(tags=["Actuator"])


@router.get("/readiness",
            status_code=HTTP_200_OK,
            summary="Readiness check",
            )
async def readiness(services: ServiceProvider, client: AsyncHttpClientDependency) -> ResponseModel[ReadinessChecked]:
    """
    Checks if the service is ready to accept requests.
    """
    services_status: list[StatusChecked] = await check_services(services=services, client=client)

    readiness_checked = ReadinessChecked(status=ServiceStatus.ONLINE, services=services_status)

    if any([service for service in services_status if service.status == ServiceStatus.OFFLINE]):
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=readiness_checked.dict())

    return ResponseModel(data=readiness_checked)


@router.get("/health",
            status_code=HTTP_200_OK,
            summary="Health check",
            )
async def health() -> ResponseModel[StatusChecked]:
    """
    Checks if the service is up and running.
    """
    return ResponseModel(data=StatusChecked(name="api-gateway", status=ServiceStatus.ONLINE))


@router.get("/",
            status_code=HTTP_301_MOVED_PERMANENTLY,
            include_in_schema=False,
            summary="Redirects to health check endpoint.")
async def root_redirect():
    """
    Redirects to health check endpoint.
    """
    return RedirectResponse(url="/docs", status_code=HTTP_301_MOVED_PERMANENTLY)


########################################################
# Internal Methods
########################################################
async def check_service(service: Service, client: AsyncHttpClient) -> StatusChecked:
    """
    Checks if the service is up and running.

    Args:
        service (Service): Service.
        client (AsyncHttpClient): Async http client.

    Returns:
        StatusChecked: Service status.
    """
    try:
        _, status_code = await gateway(client=client,
                                       method="GET",
                                       service_url=service.base_url,
                                       path=service.readiness_url)
        return StatusChecked(name=service.name,
                             status=ServiceStatus.ONLINE
                             if status_code == HTTP_200_OK else ServiceStatus.OFFLINE)
    except (asyncio.TimeoutError, aiohttp.ClientError, HTTPException):
        return StatusChecked(name=service.name, status=ServiceStatus.OFFLINE)


async def check_services(services: list[Service], client: AsyncHttpClient) -> list[StatusChecked]:
    """
    Checks if the services are up and running.

    Args:
        services (list[Service]): List of services.
        client (AsyncHttpClient): Async http client.

    Returns:
        list[StatusChecked]: List of services status.
    """
    services_status = [check_service(service=service, client=client) for service in services]

    return await asyncio.gather(*services_status)
