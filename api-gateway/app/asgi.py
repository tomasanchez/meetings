"""Application implementation - ASGI."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.adapters.http_client import aio_http_client
from app.dependencies import get_redis
from app.router import api_router_v1, root_router
from app.settings.app_settings import ApplicationSettings

log = logging.getLogger(__name__)


async def on_startup():
    """
    Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event
    """
    log.debug("Execute FastAPI startup event handler.")
    aio_http_client.get_aiohttp_client()
    get_redis()


async def on_shutdown():
    """
    Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event
    """
    log.debug("Execute FastAPI shutdown event handler.")
    await aio_http_client.close_aiohttp_client()
    await get_redis().close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Define FastAPI lifespan event handler.

    Args:
        app (FastAPI): Application object instance.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#lifespan-event
    """
    log.debug("Execute FastAPI lifespan event handler.")

    await on_startup()
    yield
    await on_shutdown()


def get_application() -> FastAPI:
    """
    Initialize FastAPI application.

    Returns:
       FastAPI: Application object instance.
    """
    log.debug("Initialize FastAPI application node.")

    settings = ApplicationSettings()

    contact = {
        "name": "Tomas Sanchez",
        "url": "https://tomasanchez.github.io/",
        "email": "tosanchez@frba.utn.edu.ar"
    }

    license_info = {
        "name": "MIT",
        "url": "https://mit-license.org/",
    }

    tags_metadata = [
        {
            "name": "Actuator",
            "description": "Verifies application's liveliness and readiness.",
        },
        {
            "name": "Queries",
            "description": "A request for data from the system.",
        },
        {
            "name": "Commands",
            "description": "A request to change the state of the system.",
        },
        {
            "name": "Scheduler",
            "description": "Manages meeting's schedule workflows.",
        },
        {
            "name": "Auth",
            "description": "Manages user's validation workflows.",
        }
    ]

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        lifespan=lifespan,
        license_info=license_info,
        contact=contact,
        openapi_tags=tags_metadata,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    log.debug("Add application routes.")

    app.include_router(root_router)
    app.include_router(api_router_v1)

    return app
