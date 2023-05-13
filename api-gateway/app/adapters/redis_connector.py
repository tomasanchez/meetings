"""
Redis Connection Adapter.
"""
import abc
from datetime import timedelta
import logging
from typing import TypeVar

import aioredis

R = TypeVar("R")


class RedisConnectionError(Exception):
    """Redis connection error.

    Exception raised when Redis client could not connect to Redis server.
    """
    pass


class RedisConnector(abc.ABC):
    """Define Redis utility.

    Utility class for handling Redis database connection and operations.
    """

    @abc.abstractmethod
    async def close(self):
        """
        Close Redis connection.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def ping(self) -> bool:
        """Execute Redis PING command.

        Ping the Redis server.

        Returns:
            bool: whether Redis client could ping Redis server.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, key: str, value: str) -> R:
        """Set value to Redis database.

        Args:
            key (str): Redis key.
            value (str): Redis value.

        Returns:
            R: Redis SET command response, for more info
                look: https://redis.io/commands/set#return-value

        Raises
            RedisConnectionError: If Redis client could not connect to Redis server.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, key: str) -> str | None:
        """Get value from Redis database.

        Args:
            key (str): Redis key.

        Returns:
            R: Redis response.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis database.

        Args:
            key (str): Redis key.

        Returns:
            bool: whether key exists in Redis database.

        Raises:
            RedisConnectionError: If Redis client could not connect to Redis server.
        """
        raise

    @abc.abstractmethod
    async def expire(self, key: str, time: int | timedelta) -> bool:
        """Set expiration time on key.

        Args:
            key (str): Redis key.
            time (int|timedelta): Expiration time in seconds or a time delta.

        Returns:
            bool: whether expiration time was set successfully.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, key: str):
        """Delete key from Redis database.

        Args:
            key (str): Redis key.

        Returns:
            int: the number of keys that were removed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def incr(self, key: str) -> int:
        """Increments a key.

        Args:
            key (str): Redis key.

        Returns:
            int: Incremented value.
        """
        raise NotImplementedError


class RedisClient(RedisConnector):
    """Define Redis utility.

    Utility class for handling Redis database connection and operations.
    Attributes:
        redis_client (aioredis.Redis, optional): Redis client object instance.
        log (logging.Logger): Logging handler for this class.
        base_redis_init_kwargs (typing.Dict[str, typing.Union[str, int]]): Common
            kwargs regardless other Redis configuration
        connection_kwargs (typing.Optional[typing.Dict[str, str]]): Extra kwargs
            for Redis object init.
    """

    log: logging.Logger = logging.getLogger(__name__)

    def __init__(self, url: str, port: int, username: str | None = None, password: str | None = None):
        """
        Creates a client connector wrapper.

        Args:
            url: the host of the redis server
            port: the port of the redis server
            username: the username of the redis server
            password: the password of the redis server
        """

        self.url: str = url
        self.port: int = port
        self.connection_kwargs: dict[str, str] = {}

        self.base_redis_init_kwargs: dict[str, str | int] = {
            "encoding": "utf-8",
            "port": port,
        }

        self.redis_client: aioredis.Redis = self._open_redis_client(username, password)

    def _open_redis_client(self, username: str | None = None, password: str | None = None) -> aioredis.Redis:
        """Create Redis client session object instance.

        Based on configuration create either Redis client.

        Returns:
            aioredis.Redis: Redis object instance.
        """

        if username and password:
            self.connection_kwargs = {
                "username": username,
                "password": password,
            }

        self.base_redis_init_kwargs.update(self.connection_kwargs)
        redis_client = aioredis.from_url(
            f"redis://{self.url}",
            **self.base_redis_init_kwargs,
        )

        return redis_client

    async def close(self):
        self.log.debug("Closing Redis client")
        await self.redis_client.close()

    async def ping(self) -> bool:
        self.log.debug("Execute Redis PING command")

        try:
            return await self.redis_client.ping()
        except (aioredis.RedisError, ConnectionError) as ex:
            self.log.exception(
                "Redis PING command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            return False

    async def set(self, key: str, value: str) -> R:
        redis_client = self.redis_client

        self.log.debug(f"Execute Redis SET command, key: {key}, value: {value}")

        try:
            return await redis_client.set(key, value)
        except aioredis.RedisError as ex:
            self.log.exception(
                "Redis SET command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise RedisConnectionError from ex

    async def exists(self, key: str) -> bool:
        self.log.debug(f"Execute Redis EXISTS command, key: {key}")
        try:
            return await self.redis_client.exists(key)
        except aioredis.RedisError as ex:
            self.log.exception(
                "Redis EXISTS command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise RedisConnectionError from ex

    async def get(self, key: str) -> str:
        redis_client = self.redis_client
        self.log.debug(f"Execute Redis GET command, key: {key}")

        try:
            return await redis_client.get(key)
        except aioredis.RedisError as ex:
            self.log.exception(
                "Redis GET command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise RedisConnectionError from ex

    async def expire(self, key: str, time: int | timedelta) -> bool:
        redis_client = self.redis_client
        self.log.debug(f"Execute Redis EXPIRE command, key: {key}, time: {time}")

        try:
            return await redis_client.expire(key, time)
        except aioredis.RedisError as ex:
            self.log.exception(
                "Redis EXPIRE command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise RedisConnectionError from ex

    async def delete(self, key: str):
        redis_client = self.redis_client
        self.log.debug(f"Execute Redis DELETE command, key: {key}")

        try:
            await redis_client.delete(key)
        except aioredis.RedisError as ex:
            self.log.exception(
                "Redis DELETE command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise RedisConnectionError from ex

    async def incr(self, key: str) -> int:
        redis_client = self.redis_client
        self.log.debug(f"Execute Redis INCR command, key: {key}")

        try:
            return await redis_client.incr(key)
        except aioredis.RedisError as ex:
            self.log.exception(
                "Redis INCR command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise RedisConnectionError from ex
