"""
Test for Rate Limiter Service
"""
from unittest import mock

import pytest

from app.adapters.redis_connector import RedisClient
from app.service_layer.rate_limiter import RedisRateLimiter

TTL = 10
THRESHOLD = 3


class TestRateLimiter:

    @pytest.fixture
    def async_mock(self):
        yield mock.AsyncMock()

    @pytest.mark.asyncio
    async def test_increments(self, redis_client_connector: RedisClient):
        """
        Given a RedisRateLimiter instance
        When the increment method is called
        Then it should increment the number of requests for the given key
        """
        # given
        expected_count = 1
        redis_client_connector.redis_client.incr = mock.AsyncMock()
        redis_client_connector.redis_client.incr.return_value = expected_count
        identifier = "test"
        redis_rate_limiter = RedisRateLimiter(redis=redis_client_connector, time_to_live=TTL, threshold=THRESHOLD)

        # when
        result = await redis_rate_limiter.increment(identifier)

        # then
        assert result == expected_count

    @pytest.mark.asyncio
    async def test_number_bellow_threshold_is_allowed(self, redis_client_connector: RedisClient):
        """
        Given a RedisRateLimiter instance
        When a request number is bellow the threshold
        Then it should return True
        """
        # given
        value = THRESHOLD - 1
        redis_rate_limiter = RedisRateLimiter(redis=redis_client_connector, time_to_live=TTL, threshold=THRESHOLD)

        # when
        result = await redis_rate_limiter.is_allowed(request_number=value)

        # then
        assert result

    @pytest.mark.asyncio
    async def test_number_above_threshold_is_not_allowed(self, redis_client_connector: RedisClient):
        """
        Given a RedisRateLimiter instance
        When a request number is above the threshold
        Then it should return False
        """
        # given
        value = THRESHOLD + 1
        redis_rate_limiter = RedisRateLimiter(redis=redis_client_connector, time_to_live=TTL, threshold=THRESHOLD)

        # when
        result = await redis_rate_limiter.is_allowed(request_number=value)

        # then
        assert not result
