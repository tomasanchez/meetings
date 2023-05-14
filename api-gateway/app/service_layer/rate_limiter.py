"""
Rate limiter service layer
"""
import abc
from datetime import timedelta

from app.adapters.redis_connector import RedisConnector


class RateLimiter(abc.ABC):
    """
    Rate limiter interface
    """

    @abc.abstractmethod
    async def increment(self, identifier: str) -> int:
        """
        Increment the number of requests for the given key

        Args:
            identifier (str): the key to increment the number of requests for

        Returns:
             int: the total number of requests for the given key
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def is_allowed(self, request_number: int) -> bool:
        """
        Check if the given key is allowed to make a request
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def timer(self, identifier: str, time: int | timedelta) -> bool:
        """
        Times to reset the number of requests for the given key.

        Args:
            identifier (str): the key to reset the number of requests for
            time (int | timedelta): the time in seconds

        Returns:
            bool: True if the key was given the timer to reset, False otherwise
        """
        raise NotImplementedError


class RedisRateLimiter(RateLimiter):
    """
    Rate limiter implementation using redis
    """

    def __init__(self, redis: RedisConnector, time_to_live: int, threshold: int):
        """

        Args:
            redis: A redis connector
            time_to_live: time in seconds to reset the number of requests for the given key
            threshold: the maximum number of requests allowed for any key
        """
        self.redis = redis
        self.time_to_live = time_to_live
        self.threshold = threshold

    async def increment(self, identifier: str) -> int:
        return await self.redis.incr(identifier)

    async def is_allowed(self, request_number: int) -> bool:
        return request_number <= self.threshold

    async def timer(self, identifier: str, time: int | timedelta) -> bool:
        return await self.redis.expire(identifier, time)
