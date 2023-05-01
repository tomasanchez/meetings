"""Aiohttp client class utility."""
import abc
import asyncio
import logging
from socket import AF_INET
from typing import Any, AnyStr, Dict
from typing import Optional

import aiohttp

SIZE_POOL_AIOHTTP = 100


class AsyncHttpClient(abc.ABC):
    """
    Abstract class for async http client.
    """

    @abc.abstractmethod
    async def get(
            self,
            url: str,
            headers: dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        """Execute HTTP GET request.

        Args:
            url (str): HTTP GET request endpoint.
            headers (typing.Dict[str, typing.AnyStr]): Optional HTTP Headers to send
                with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP GET request response - aiohttp.ClientResponse
                object instance.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def post(
            self,
            url: str,
            data: Any | None = None,
            headers: dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        """Execute HTTP POST request.

        Args:
            url (str): HTTP POST request endpoint.
            data (Any | None): The data to send in the body of the
                request. This can be a FormData object or anything that can be passed
                into FormData, e.g. a dictionary, bytes, or file-like object.
            headers (dict[str, typing.AnyStr]): Optional HTTP Headers to send
                with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP POST request response - aiohttp.ClientResponse
                object instance.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def put(
            self,
            url: str,
            data: Any | None = None,
            headers: dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        """Execute HTTP PUT request.

        Args:
            url (str): HTTP PUT request endpoint.
            data (typing.Optional[typing.Any]): The data to send in the body of the
                request. This can be a FormData object or anything that can be passed
                into FormData, e.g. a dictionary, bytes, or file-like object.
            headers (typing.Dict[str, typing.AnyStr]): Optional HTTP Headers to send
                with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            aiohttp.ClientResponse: HTTP PUT request response - aiohttp.ClientResponse
                object instance.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(
            self,
            url: str,
            headers: dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        """Execute HTTP DELETE request.

        Args:
            url (str): HTTP DELETE request endpoint.
            headers (typing.Dict[str, typing.AnyStr]): Optional HTTP Headers to send
                with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP DELETE request response - aiohttp.ClientResponse
                object instance.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def patch(
            self,
            url: str,
            data: Optional[Any] = None,
            headers: Dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        """Execute HTTP PATCH request.

        Args:
            url (str): HTTP PATCH request endpoint.
            data (typing.Optional[typing.Any]): The data to send in the body of the
                request. This can be a FormData object or anything that can be passed
                into FormData, e.g. a dictionary, bytes, or file-like object.
            headers (typing.Dict[str, typing.AnyStr]): Optional HTTP Headers to send
                with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP PATCH request response - aiohttp.ClientResponse
                object instance.
        """
        raise NotImplementedError


class AiohttpClient(AsyncHttpClient):
    """Aiohttp session client utility.

    Utility class for handling HTTP async request for whole FastAPI application
    scope.
    Attributes:
        sem (asyncio.Semaphore, optional): Semaphore value.
        aiohttp_client (aiohttp.ClientSession, optional): Aiohttp client session
            object instance.
    """

    def __init__(self, aiohttp_client: aiohttp.ClientSession | None = None):
        self.sem: Optional[asyncio.Semaphore] = None
        self.aiohttp_client: Optional[aiohttp.ClientSession] = aiohttp_client
        self.log: logging.Logger = logging.getLogger(__name__)

    def get_aiohttp_client(self) -> aiohttp.ClientSession:
        """Create aiohttp client session object instance.
        Returns:
            aiohttp.ClientSession: ClientSession object instance.
        """
        if self.aiohttp_client is None:
            self.log.debug("Initialize AiohttpClient session.")
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET,
                limit_per_host=SIZE_POOL_AIOHTTP,
            )
            self.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )

        return self.aiohttp_client

    async def close_aiohttp_client(self) -> None:
        """Close aiohttp client session."""
        if self.aiohttp_client:
            self.log.debug("Close AiohttpClient session.")
            await self.aiohttp_client.close()
            self.aiohttp_client = None

    async def get(
            self,
            url: str,
            headers: Dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        client = self.get_aiohttp_client()

        self.log.debug(f"Started GET {url}")
        response = await client.get(
            url,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        return response

    async def post(
            self,
            url: str,
            data: Optional[Any] = None,
            headers: Dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        client = self.get_aiohttp_client()

        self.log.debug(f"Started POST: {url}")
        response = await client.post(
            url,
            json=data,
            headers=headers,
            raise_for_status=raise_for_status,
            allow_redirects=False,
        )

        return response

    async def put(
            self,
            url: str,
            data: Optional[Any] = None,
            headers: Dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        client = self.get_aiohttp_client()

        self.log.debug(f"Started PUT: {url}")
        response = await client.put(
            url,
            json=data,
            headers=headers,
            raise_for_status=raise_for_status,
            allow_redirects=False,
        )

        return response

    async def delete(
            self,
            url: str,
            headers: Dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        client = self.get_aiohttp_client()

        self.log.debug(f"Started DELETE: {url}")
        response = await client.delete(
            url,
            headers=headers,
            raise_for_status=raise_for_status,
            allow_redirects=False,
        )

        return response

    async def patch(
            self,
            url: str,
            data: Optional[Any] = None,
            headers: Dict[str, AnyStr] = None,
            raise_for_status: bool = False,
    ) -> aiohttp.ClientResponse:
        client = self.get_aiohttp_client()

        self.log.debug(f"Started PATCH: {url}")
        response = await client.patch(
            url,
            json=data,
            headers=headers,
            raise_for_status=raise_for_status,
            allow_redirects=False,
        )

        return response


aio_http_client = AiohttpClient()
