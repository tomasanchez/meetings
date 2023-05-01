"""
FastAPI dependencies injection.
"""
from typing import Annotated

from fastapi import Depends

from app.adapters.http_client import AsyncHttpClient, aio_http_client
from app.domain.models import Service


def get_async_http_client() -> AsyncHttpClient:
    """Get async http client."""
    return aio_http_client


AsyncHttpClientDependency = Annotated[AsyncHttpClient, Depends(get_async_http_client)]


def get_services() -> list[Service]:
    """Get service provider."""
    return list()


ServiceProvider = Annotated[list[Service], Depends(get_services)]
