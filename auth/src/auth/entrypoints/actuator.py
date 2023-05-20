"""
Actuator Entry Point.
"""

from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY, HTTP_503_SERVICE_UNAVAILABLE

from auth.app.dependencies import ClientFactoryDependency
from auth.domain.events import HealthChecked, ReadinessChecked, ServiceStatus, StatusChecked
from auth.domain.schemas import ResponseModel

router = APIRouter(tags=["Actuator"])


@router.get("/readiness",
            status_code=HTTP_200_OK,
            summary="Readiness Check",
            )
async def readiness(db_client_factory: ClientFactoryDependency) -> ResponseModel[ReadinessChecked]:
    """
    Verifies if the application is ready to receive requests.
    """
    services = [_ping_database(db_client_factory())]

    readiness_status = ReadinessChecked(status=ServiceStatus.ONLINE, services=services)

    if any(service.status == ServiceStatus.OFFLINE for service in services):
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=readiness_status.dict())

    return ResponseModel(data=readiness_status)


@router.get("/health", status_code=HTTP_200_OK, )
async def health() -> ResponseModel[HealthChecked]:
    """
    Verifies if the application is running.
    """
    return ResponseModel(data=HealthChecked())


@router.get(
    "/",
    include_in_schema=False,
    status_code=HTTP_301_MOVED_PERMANENTLY,
)
def root_redirect():
    """
    Redirects the root path to the docs.
    """
    return RedirectResponse(url="/docs", status_code=301)


####################################################################################################
# Internal Methods
####################################################################################################

def _ping_database(client: MongoClient) -> StatusChecked:
    """
    Pings the database.

    Args:
        client (MongoClient): The database client.

    Returns:
        StatusChecked: The status of the database.
    """
    service_status = StatusChecked(name="mongodb", status=ServiceStatus.ONLINE)

    try:
        client.admin.command("ping")
    except ServerSelectionTimeoutError as e:
        service_status.status = ServiceStatus.OFFLINE
        service_status.detail = str(e)

    return service_status
