"""
Actuator Entry Point.
"""

from fastapi import APIRouter
from starlette.responses import RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY

from auth.domain.events import HealthChecked
from auth.domain.schemas import ResponseModel

router = APIRouter(tags=["Actuator"])


@router.get("/health", status_code=HTTP_200_OK, )
async def health() -> ResponseModel[HealthChecked]:
    """
    Health check endpoint.
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
