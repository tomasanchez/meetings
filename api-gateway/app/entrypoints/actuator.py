"""
Actuator entrypoint
"""
from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY, HTTP_503_SERVICE_UNAVAILABLE

from app.domain.events.actuator import ReadinessChecked, StatusChecked
from app.domain.models import ServiceStatus
from app.domain.schemas import ResponseModel

router = APIRouter(tags=["Actuator"])


@router.get("/readiness",
            status_code=HTTP_200_OK,
            summary="Readiness check",
            )
async def readiness() -> ResponseModel[ReadinessChecked]:
    """
    Checks if the service is ready to accept requests.
    """

    services: list[StatusChecked] = list()

    readiness_checked = ReadinessChecked(status=ServiceStatus.ONLINE, services=services)

    if any([service for service in services if service.status == ServiceStatus.OFFLINE]):
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=readiness_checked.json())

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
