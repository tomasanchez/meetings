"""
This module is responsible for making requests to in-network services.
"""
import asyncio
import json
import logging
from typing import Any, TypeVar
from urllib.parse import urlencode

import aiohttp
import async_timeout
from fastapi import HTTPException, status

from app.adapters.http_client import AsyncHttpClient, aio_http_client
from app.domain.schemas import CamelCaseModel

log = logging.getLogger("uvicorn")


async def make_request(
        url: str,
        method: str,
        data: dict | None = None,
        headers: dict | None = None,
        client: AsyncHttpClient = aio_http_client,

) -> tuple[dict, int]:
    """
    Make request to in-network services.

    Args:
        url: is the url for one of the in-network services
        method: is the lower version of one of the HTTP methods: GET, POST, PUT, DELETE # noqa
        data: is the payload
        headers: is the header to put additional headers into request
        client: is the async http client

    Returns:
        tuple[dict, int]: is the response body and status code
    """

    if not data:
        data = {}

    async with async_timeout.timeout(60):
        response: aiohttp.ClientResponse

        match method.lower():
            case 'get':
                response = await client.get(
                    url=url,
                    headers=headers,
                    raise_for_status=False,
                )
            case 'post':
                response = await client.post(
                    url=url,
                    data=data,
                    headers=headers,
                    raise_for_status=False,
                )
            case 'put':
                response = await client.put(
                    url=url,
                    data=data,
                    headers=headers,
                    raise_for_status=False,
                )
            case 'delete':
                response = await client.delete(
                    url=url,
                    headers=headers,
                    raise_for_status=False,
                )
            case 'patch':
                response = await client.patch(
                    url=url,
                    data=data,
                    headers=headers,
                    raise_for_status=False,
                )
            case _:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method {method} is not allowed",
                )

        return await response.json(), response.status


M = TypeVar('M', bound=CamelCaseModel)


async def gateway(
        client: AsyncHttpClient,
        method: str,
        service_url: str,
        path: str,
        query_params: dict | None = None,
        request_body: dict | str | None = None,
) -> tuple[dict[str, Any], int]:
    """
    Make request to in-network services.

    Args:
        client: an Async HTTP Client
        method: is the lower version of one of the HTTP methods: GET, POST, PUT, DELETE # noqa
        service_url: is the url for one of the in-network services
        path: is the path to bind (like app.post('/api/users/'))
        query_params: is the query params to add to url
        request_body: is the payload

    Returns:
        service result coming / non-blocking http request (coroutine)
    """

    if not query_params:
        query_params = {}

    if not request_body:
        request_body = {}

    if isinstance(request_body, str):
        request_body = json.loads(request_body)

    url = f'{service_url}{path}' if not query_params else f'{service_url}{path}?{urlencode(query_params)}'

    headers = dict()

    response: aiohttp.ClientResponse

    try:
        response_body, status_code_from_service = await make_request(
            url=url,
            method=method,
            data=request_body,
            headers=headers,
            client=client,
        )

    except asyncio.TimeoutError:
        log.error(f'Time our for: {url}, {method}')
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail='Service is timed out.',
        )

    except aiohttp.ClientConnectorError as e:
        log.error(f'Connection error for: {url}, {method}. {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service is unavailable.',
        )

    except aiohttp.ContentTypeError as e:
        log.error(f'Content type error for: {url}, {method}. {str(e)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Service error.',
        )

    return response_body, status_code_from_service
