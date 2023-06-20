"""
FastAPI dependencies injection.
"""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.adapters.http_client import AsyncHttpClient, aio_http_client
from app.adapters.redis_connector import RedisClient, RedisClusterConnection, RedisConnector
from app.domain.models import Service
from app.service_layer.rate_limiter import RateLimiter, RedisRateLimiter
from app.settings.app_settings import ApplicationSettings
from app.settings.gateway_settings import GatewaySettings
from app.settings.redis_config import RedisSettings

redis_connector: RedisConnector | None = None
bearer_auth = HTTPBearer(scheme_name='JSON Web Token', description='Bearer JWT')

BearerTokenAuth = Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth)]

app_settings = ApplicationSettings()


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


def get_rate_limiter(redis: RedisDependency) -> RateLimiter | None:
    """Get rate limiter."""
    settings = ApplicationSettings()

    if not settings.USE_LIMITER:
        return None

    return RedisRateLimiter(redis=redis, threshold=settings.LIMITER_THRESHOLD, time_to_live=settings.LIMITER_INTERVAL)


RateLimiterDependency = Annotated[RateLimiter | None, Depends(get_rate_limiter)]
