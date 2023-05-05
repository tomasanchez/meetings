"""
Test for the gateway service layer
"""
import json
from typing import Any

from aioresponses import aioresponses
from fastapi import HTTPException
import pytest
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, \
    HTTP_503_SERVICE_UNAVAILABLE

from app.domain.models import Service
from app.service_layer.gateway import get_users, verify_scheduling_meeting, verify_status
from tests.mocks import schedule_command_factory, user_registered_factory


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

    @pytest.mark.asyncio
    async def test_schedule_command_is_ok(self, fake_web, auth_service, aio_http_client):
        """
        GIVEN a schedule command with a valid organizer
        WHEN verification is made
        THEN it should return the same command.
        """
        # given
        organizer = "johndoe"
        command = schedule_command_factory(organizer=organizer)
        json_dict = json.loads(user_registered_factory(username=organizer).json(by_alias=True))
        payload = {"data": [json_dict]}
        fake_web.get(f"{auth_service.base_url}/api/v1/users?users=johndoe", payload=payload, status=HTTP_200_OK)

        # when
        updated_command = await verify_scheduling_meeting(command=command, service=auth_service, client=aio_http_client)

        # then
        assert command == updated_command

    @pytest.mark.asyncio
    async def test_schedule_command_is_ok_with_guests(self, fake_web, auth_service, aio_http_client):
        """
        GIVEN a schedule command with a valid organizer and guests
        WHEN verification is made
        THEN it should return the same command.
        """
        # given
        organizer = "johndoe"
        guest_1 = "janedoe"
        guest_2 = "mark"
        guests = {guest_1, guest_2}

        command = schedule_command_factory(organizer=organizer, guests=guests)
        users = guests.copy()
        users.add(organizer)
        query = f"users={', '.join(users)}"

        json_dict = json.loads(user_registered_factory(username=organizer).json(by_alias=True))
        json_dict_2 = json.loads(user_registered_factory(username=guest_1).json(by_alias=True))
        json_dict_3 = json.loads(user_registered_factory(username=guest_2).json(by_alias=True))
        payload = {"data": [json_dict, json_dict_2, json_dict_3]}

        fake_web.get(f"{auth_service.base_url}/api/v1/users?{query}", payload=payload, status=HTTP_200_OK)

        # when
        updated_command = await verify_scheduling_meeting(command=command, service=auth_service, client=aio_http_client)

        # then
        assert command == updated_command

    @pytest.mark.asyncio
    async def test_schedule_command_with_missing_guests(self, fake_web, auth_service, aio_http_client):
        """
        GIVEN a schedule command with a valid organizer but invalid guests
        WHEN verification is made
        THEN only valid guests should be returned.
        """
        # given
        organizer = "johndoe"
        guest_1 = "janedoe"
        guest_2 = "mark"
        guests = {guest_1, guest_2}

        command = schedule_command_factory(organizer=organizer, guests=guests)
        users = guests.copy()
        users.add(organizer)
        query = f"users={', '.join(users)}"

        json_dict = json.loads(user_registered_factory(username=organizer).json(by_alias=True))
        json_dict_2 = json.loads(user_registered_factory(username=guest_1).json(by_alias=True))
        payload = {"data": [json_dict, json_dict_2]}

        fake_web.get(f"{auth_service.base_url}/api/v1/users?{query}", payload=payload, status=HTTP_200_OK)

        # when
        updated_command = await verify_scheduling_meeting(command=command, service=auth_service, client=aio_http_client)

        # then
        assert command != updated_command
        assert guest_2 not in updated_command.guests

    @pytest.mark.asyncio
    async def test_schedule_command_with_missing_organizer(self, fake_web, auth_service, aio_http_client):
        """
        GIVEN a schedule command an invalid organizer
        WHEN verification is made
        THEN should raise an exception.
        """
        # given
        organizer = "johndoe"

        command = schedule_command_factory(organizer=organizer)

        fake_web.get(f"{auth_service.base_url}/api/v1/users?users={organizer}",
                     payload={"data": []},
                     status=HTTP_200_OK)

        # when
        with pytest.raises(HTTPException):
            updated_command = await verify_scheduling_meeting(command=command,
                                                              service=auth_service,
                                                              client=aio_http_client)
