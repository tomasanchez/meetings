"""
FastAPI middlewares
"""
from fastapi import HTTPException, Request
from starlette import status

from app.dependencies import RateLimiterDependency


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
