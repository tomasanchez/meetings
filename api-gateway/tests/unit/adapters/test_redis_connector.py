"""
Tests for the RedisConnector class.
"""
from unittest import mock

import aioredis as aioredis
import pytest

from app.adapters.redis_connector import RedisClient, RedisConnectionError


class TestRedisClient:

    @pytest.fixture
    def async_mock(self):
        yield mock.AsyncMock()

    def test_should_create_client(self):
        """
        GIVEN a RedisClient instance
        WHEN the connector is created
        THEN it should create a Redis client.
        """
        # given
        url = "localhost"
        port = 6379

        # when
        connector = RedisClient(url=url, port=port)

        # then
        assert isinstance(connector.redis_client, aioredis.Redis)
        assert connector.redis_client.connection_pool.connection_kwargs["host"] == url
        assert connector.redis_client.connection_pool.connection_kwargs["port"] == port

    @pytest.mark.asyncio
    async def test_should_execute_ping_and_return_true(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance
        WHEN the ping method is called
        THEN it should execute the ping command and return True.
        """
        # given
        redis_client_connector.redis_client.ping = async_mock
        async_mock.return_value = True

        # when
        result = await redis_client_connector.ping()

        # then
        assert result
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_ping_and_return_false(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance, and the aioredis.Redis cannot connect
        WHEN the ping method is called
        THEN it should execute the ping command and return False.
        """
        # given
        redis_client_connector.redis_client.ping = async_mock
        async_mock.side_effect = aioredis.RedisError()

        result = await redis_client_connector.ping()

        # then
        assert not result
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_set_and_return_response(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance
        WHEN the set method is called
        THEN it should execute the set command and return the response.
        """
        # given
        redis_client_connector.redis_client.set = async_mock
        async_mock.return_value = b"OK"

        # when
        result = await redis_client_connector.set("key", "value")

        # then
        assert result == b"OK"
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_set_and_raise(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance, and the aioredis.Redis cannot connect
        WHEN the set method is called
        THEN it should execute the set command and raise an exception.
        """
        redis_client_connector.redis_client.set = async_mock
        async_mock.side_effect = aioredis.RedisError()

        with pytest.raises(RedisConnectionError):
            await redis_client_connector.set("key", "value")

    @pytest.mark.asyncio
    async def test_should_execute_get_and_return_response(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance
        WHEN the get method is called
        THEN it should execute the get command and return the response.
        """
        # given
        redis_client_connector.redis_client.get = async_mock
        async_mock.return_value = b"value"

        # when
        result = await redis_client_connector.get("key")

        # then
        assert result == b"value"
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_get_and_raise(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance, and the aioredis.Redis cannot connect
        WHEN the get method is called
        THEN it should execute the get command and raise an exception.
        """
        redis_client_connector.redis_client.get = async_mock
        async_mock.side_effect = aioredis.RedisError()

        with pytest.raises(RedisConnectionError):
            await redis_client_connector.get("key")

    @pytest.mark.asyncio
    async def test_should_execute_delete_and_return_response(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance
        WHEN the delete method is called
        THEN it should execute the delete command and return the response.
        """
        # given
        redis_client_connector.redis_client.delete = async_mock

        # when
        await redis_client_connector.delete("key")

        # then
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_delete_and_raise(self, async_mock, redis_client_connector):
        """
        GIVEN a RedisClient instance, and the aioredis.Redis cannot connect
        WHEN the delete method is called
        THEN it should execute the delete command and raise an exception.
        """
        redis_client_connector.redis_client.delete = async_mock
        async_mock.side_effect = aioredis.RedisError()

        with pytest.raises(RedisConnectionError):
            await redis_client_connector.delete("key")

    @pytest.mark.asyncio
    async def test_should_execute_expire_and_return_response(self, async_mock, redis_client_connector: RedisClient):
        """
        GIVEN a RedisClient instance
        WHEN the expires method is called
        THEN it should execute the expires command and return the response.
        """
        redis_client_connector.redis_client.expire = async_mock
        async_mock.return_value = True

        # when
        result = await redis_client_connector.expire("key", time=1)

        # then
        assert result
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_expire_and_raise(self, async_mock, redis_client_connector: RedisClient):
        """
        GIVEN a RedisClient instance, and the aioredis.Redis cannot connect
        WHEN the expires method is called
        THEN it should execute the expires command and raise an exception.
        """
        redis_client_connector.redis_client.delete = async_mock
        async_mock.side_effect = aioredis.RedisError()

        with pytest.raises(RedisConnectionError):
            await redis_client_connector.expire("key", time=1)

    @pytest.mark.asyncio
    async def test_should_execute_incr_and_return_value(self, async_mock, redis_client_connector: RedisClient):
        """
        GIVEN a RedisClient instance
        WHEN the incr method is called
        THEN it should execute the incr command and return the value.
        """
        redis_client_connector.redis_client.incr = async_mock
        async_mock.return_value = 1

        # when
        result = await redis_client_connector.incr("key")

        # then
        assert result == 1
        async_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_execute_incr_and_raise(self, async_mock, redis_client_connector: RedisClient):
        """
        GIVEN a RedisClient instance, and the aioredis.Redis cannot connect
        WHEN the incr method is called
        THEN it should execute the incr command and raise an exception.
        """
        redis_client_connector.redis_client.incr = async_mock
        async_mock.side_effect = aioredis.RedisError()

        with pytest.raises(RedisConnectionError):
            await redis_client_connector.incr("key")
