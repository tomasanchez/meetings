"""Application implementation - ASGI."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

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


async def on_shutdown():
    """
    Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event
    """
    log.debug("Execute FastAPI shutdown event handler.")


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

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        lifespan=lifespan,
        license_info=license_info,
        contact=contact,
    )

    log.debug("Add application routes.")

    app.include_router(root_router)
    app.include_router(api_router_v1)

    return app
