"""
FastAPI dependencies injection.
"""
from typing import Annotated

from fastapi import Depends

from app.adapters.http_client import AsyncHttpClient, aio_http_client
from app.adapters.redis_connector import RedisClient, RedisClusterConnection, RedisConnector
from app.domain.models import Service
from app.settings.gateway_settings import GatewaySettings
from app.settings.redis_config import RedisSettings

redis_connector: RedisConnector | None = None


def get_async_http_client() -> AsyncHttpClient:
    """Get async http client."""
    return aio_http_client


AsyncHttpClientDependency = Annotated[AsyncHttpClient, Depends(get_async_http_client)]


def get_services() -> list[Service]:
    """Get service provider."""
    return GatewaySettings().SERVICES


ServiceProvider = Annotated[list[Service], Depends(get_services)]


def get_redis() -> RedisConnector:
    """Get redis connector."""

    global redis_connector

    settings = RedisSettings()

    host = settings.HOST
    port = settings.PORT

    if redis_connector is None:
        redis_connector = RedisClusterConnection(url=host, port=port) if settings.CLUSTER else RedisClient(url=host,
                                                                                                           port=port)

    return redis_connector


RedisDependency = Annotated[RedisConnector, Depends(get_redis)]
