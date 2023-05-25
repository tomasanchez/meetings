"""
FastAPI middlewares
"""
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from starlette import status

from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, BearerTokenAuth, RateLimiterDependency, ServiceProvider
from app.domain.events.auth_service import UserAuthenticated
from app.service_layer.gateway import api_v1_url, get_service, verify_status


async def rate_limiter_middleware(request: Request, rate_limiter: RateLimiterDependency):
    """
    Rate limiter middleware.

    Limits the number of requests per user per interval.
    """

    if not rate_limiter:
        return

    issuer = request.headers.get("X-Forwarded-For") or request.client.host

    key = f"rate-{issuer}"

    requests = await rate_limiter.increment(key)

    if not await rate_limiter.is_allowed(requests):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Surpassed rate limit.")

    await rate_limiter.timer(key, time=rate_limiter.time_to_live)


async def auth_middleware(token: BearerTokenAuth,
                          services: ServiceProvider,
                          client: AsyncHttpClientDependency) -> UserAuthenticated:
    """
    Authentication middleware.

    Args:
        token: Authorization credentials
        services: available service
        client: HTTP client

    Returns:
        UserAuthenticated: User information

    Raises:
        HTTPException: if the token is invalid
    """
    auth_response, status_code = await gateway(
        service_url=(await get_service(service_name="auth", services=services)).base_url,
        path=f"{api_v1_url}/auth/me",
        client=client,
        method="GET",
        headers={"Authorization": f"Bearer {token.credentials}"}
    )

    verify_status(response=auth_response, status_code=status_code)

    return UserAuthenticated(**auth_response.get("data"))


AuthMiddleware = Annotated[UserAuthenticated, Depends(auth_middleware)]
