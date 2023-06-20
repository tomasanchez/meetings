"""
FastAPI middlewares
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from opentelemetry import trace
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.types import ASGIApp
import time

from app.adapters.network import gateway
from app.adapters.telemetry.prometheus import EXCEPTIONS, INFO, REQUESTS, REQUESTS_IN_PROGRESS, \
    REQUESTS_PROCESSING_TIME, RESPONSES
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

    if requests == 1:
        await rate_limiter.timer(key)

    if not await rate_limiter.is_allowed(requests):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Surpassed rate limit.")


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


########################################################################################
# Telemetry
########################################################################################


class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str = "app") -> None:
        super().__init__(app)
        self.app_name = app_name
        INFO.labels(app_name=self.app_name).inc()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        method = request.method
        path, is_handled_path = self.get_path(request)

        if not is_handled_path:
            return await call_next(request)

        REQUESTS_IN_PROGRESS.labels(
            method=method, path=path, app_name=self.app_name).inc()

        REQUESTS.labels(method=method, path=path, app_name=self.app_name).inc()

        before_time = time.perf_counter()

        try:
            response = await call_next(request)
        except BaseException as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            EXCEPTIONS.labels(method=method, path=path, exception_type=type(
                e).__name__, app_name=self.app_name).inc()
            raise e from None
        else:
            status_code = response.status_code
            after_time = time.perf_counter()
            # retrieve trace id for exemplar
            span = trace.get_current_span()
            trace_id = trace.format_trace_id(
                span.get_span_context().trace_id)

            REQUESTS_PROCESSING_TIME.labels(method=method, path=path, app_name=self.app_name).observe(
                after_time - before_time, exemplar={'TraceID': trace_id}
            )
        finally:
            RESPONSES.labels(method=method, path=path,
                             status_code=status_code, app_name=self.app_name).inc()
            REQUESTS_IN_PROGRESS.labels(
                method=method, path=path, app_name=self.app_name).dec()

        return response

    @staticmethod
    def get_path(request: Request) -> tuple[str, bool]:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False
