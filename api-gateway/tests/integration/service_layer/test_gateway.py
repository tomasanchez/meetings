"""
Test for the gateway service layer
"""
from typing import Any

import pytest
from aioresponses import aioresponses
from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, \
    HTTP_503_SERVICE_UNAVAILABLE

from app.domain.models import Service
from app.service_layer.gateway import get_users, verify_status


class TestGateway:

    @pytest.fixture
    def auth_service(self) -> Service:
        return Service(name="auth", base_url="http://fake-auth")

    @pytest.fixture
    def fake_web(self):
        with aioresponses() as mock:
            yield mock

    @pytest.mark.parametrize(
        "status_code, payload",
        [
            (HTTP_200_OK, {"data": []}),
            (HTTP_503_SERVICE_UNAVAILABLE, {"detail": "Service unavailable"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_users(self, fake_web, auth_service, aio_http_client,
                             status_code, payload
                             ):
        """
        GIVEN a request to get all users
        WHEN the request is made, and service is in a specific status
        THEN it should return corresponding data.
        """
        # given
        fake_web.get(f"{auth_service.base_url}/api/v1/users", payload=payload, status=status_code)

        # when
        response, status_code = await get_users(users="", service=auth_service, client=aio_http_client)

        # then
        assert status_code == status_code
        assert response == payload

    @pytest.mark.parametrize(
        "response_status, valid_values, payload",
        [
            (HTTP_503_SERVICE_UNAVAILABLE, [HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED],
             {"detail": "Service unavailable"}),
            (HTTP_404_NOT_FOUND, [HTTP_200_OK], {"detail": "object not found"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_raises_invalid_status(self, fake_web, auth_service,
                                         valid_values: list[int], response_status: int, payload: dict[str, Any]):
        """
        GIVEN a request to get all users
        WHEN the request is made, and service is in a specific status
        THEN it should return corresponding data.
        """

        # when / then
        with pytest.raises(HTTPException):
            await verify_status(response=payload, status_codes=valid_values, status_code=response_status)
