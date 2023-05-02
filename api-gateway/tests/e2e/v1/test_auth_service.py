"""
Test Auth Service
"""
from typing import Any, Callable
import uuid

from aioresponses import aioresponses
from pydantic import EmailStr
import pytest
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, \
    HTTP_405_METHOD_NOT_ALLOWED, \
    HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_501_NOT_IMPLEMENTED, HTTP_502_BAD_GATEWAY, \
    HTTP_503_SERVICE_UNAVAILABLE, \
    HTTP_504_GATEWAY_TIMEOUT

from app.dependencies import get_async_http_client, get_services
from app.domain.commands.auth_service import AuthenticateUser, RegisterUser
from app.domain.events.auth_service import TokenGenerated, UserRegistered
from app.domain.models import Service
from app.domain.schemas import ResponseModel, ResponseModels
from tests.conftest import DependencyOverrider

fake_auth_base_url = "http://fake-auth:8000"


def fake_user_response(username: str, user_id: str | None = None, ) -> dict[str, Any]:
    """
    Fake user response.

    Args:
        username (str): The username.
        user_id (str | None): The user id.

    Returns:
        dict[str, str]: The response.
    """
    user_data = UserRegistered(id=user_id or str(uuid.uuid4()),
                               username=username, email=EmailStr(f"{username}@e.mail"), )

    return ResponseModel[UserRegistered](data=user_data).dict(by_alias=True)


class TestAuthServiceGateway:

    @pytest.fixture
    def fake_web(self):
        with aioresponses() as mock:
            yield mock

    overrides: dict[Callable, Callable] = {
        get_services: lambda: [Service(name="auth", base_url=fake_auth_base_url)],
    }


class TestAuthQueries(TestAuthServiceGateway):

    def test_get_user(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a FastAPI application
        WHEN the get user path is requested (GET) to a valid user
        THEN it returns Ok with the user
        """
        # given
        username = "johndoe"
        fake_web.get(f"{fake_auth_base_url}/api/v1/users/{username}/", payload=fake_user_response(username))
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get(f"/api/v1/auth-service/users/{username}")

            # then
            assert response.status_code == HTTP_200_OK
            assert ResponseModel[UserRegistered](**response.json()).data.username == username

    def test_get_user_not_found(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a FastAPI application
        WHEN the get user path is requested (GET) to a non-existing user
        THEN it returns Ok with the user
        """
        # given
        username = "johndoe"
        fake_web.get(f"{fake_auth_base_url}/api/v1/users/{username}/", status=HTTP_404_NOT_FOUND, payload=dict())
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get(f"/api/v1/auth-service/users/{username}")

            # then
            assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("error_status", [
        HTTP_405_METHOD_NOT_ALLOWED,
        HTTP_500_INTERNAL_SERVER_ERROR,
        HTTP_501_NOT_IMPLEMENTED,
        HTTP_502_BAD_GATEWAY,
        HTTP_503_SERVICE_UNAVAILABLE,
        HTTP_504_GATEWAY_TIMEOUT
    ])
    def test_get_user_server_error(self, test_client, fake_web, aio_http_client, error_status: int):
        """
        GIVEN a FastAPI application
        WHEN the get user path is requested (GET) and the auth service returns an error
        THEN it returns Ok with the user
        """
        # given
        username = "johndoe"
        fake_web.get(f"{fake_auth_base_url}/api/v1/users/{username}/", status=error_status,
                     payload=dict())
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get(f"/api/v1/auth-service/users/{username}")

            # then
            assert response.status_code == error_status

    def test_get_users(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a FastAPI application
        WHEN the get users path is requested (GET)
        THEN it returns Ok with the users
        """
        # given
        fake_web.get(f"{fake_auth_base_url}/api/v1/users",
                     payload=ResponseModels[UserRegistered](data=list()).dict(by_alias=True))
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get("/api/v1/auth-service/users")

            # then
            assert response.status_code == HTTP_200_OK

    @pytest.mark.parametrize("error_status", [
        HTTP_405_METHOD_NOT_ALLOWED,
        HTTP_500_INTERNAL_SERVER_ERROR,
        HTTP_501_NOT_IMPLEMENTED,
        HTTP_502_BAD_GATEWAY,
        HTTP_503_SERVICE_UNAVAILABLE,
        HTTP_504_GATEWAY_TIMEOUT
    ])
    def test_get_users_error(self, test_client, fake_web, aio_http_client, error_status: int):
        """
        GIVEN a FastAPI application
        WHEN the get user path is requested (GET) and the auth service returns an error
        THEN it returns Ok with the user
        """
        # given
        fake_web.get(f"{fake_auth_base_url}/api/v1/users", status=error_status,
                     payload=dict())
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get(f"/api/v1/auth-service/users")

            # then
            assert response.status_code == error_status


class TestAuthCommands(TestAuthServiceGateway):

    def test_create_user(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a FastAPI application, and a valid command.
        WHEN the create user command is requested (POST)
        THEN it returns Ok with the user
        """
        # given
        username, email, password = "johndoe", EmailStr("johndoe@e.mail"), "password"

        command = RegisterUser(username=username, email=email, password=password)

        fake_web.post(f"{fake_auth_base_url}/api/v1/users/",
                      payload=fake_user_response(username),
                      status=HTTP_201_CREATED)
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post(f"/api/v1/auth-service/users", json=command.dict(by_alias=True))

            # then
            assert response.status_code == HTTP_201_CREATED
            assert ResponseModel[UserRegistered](**response.json()).data.username == username

    def test_create_user_conflict(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a FastAPI application, and a valid command.
        WHEN the create user command is requested (POST) and the user already exists
        THEN it returns Not Found with the user
        """
        # given
        username, email, password = "johndoe", EmailStr("john@doe.mail"), "password"
        command = RegisterUser(username=username, email=email, password=password)
        fake_web.post(f"{fake_auth_base_url}/api/v1/users/",
                      payload={"detail": "User already exists"},
                      status=HTTP_404_NOT_FOUND)
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post(f"/api/v1/auth-service/users",
                                        json=command.dict(by_alias=True))

            # then
            assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "username, email, password",
        [
            ("valid_username", "invalid_email", "valid_password"),
            ("valid_username", "", "valid_password"),
            ("", "valid@e.mail", "valid_password"),
            ("   ", "   ", "   "),
            ("valid_password", "valid@e.mail", ""),
        ],
    )
    def test_create_user_invalid_command(self, test_client, aio_http_client, username, email, password):
        """
        GIVEN a FastAPI application, and an invalid command.
        WHEN the create user command is requested (POST)
        THEN it returns UNPROCESSABLE_ENTITY
        """
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(overrides=self.overrides):
            # when
            response = test_client.post(f"/api/v1/auth-service/users",
                                        json=dict(username=username, email=email, password=password))

            # then
            assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    def test_authenticate(self, test_client, aio_http_client, fake_web):
        """
        GIVEN a FastAPI application, and a valid command.
        WHEN the authenticate command is requested (POST)
        THEN it returns a JSON Web Token
        """
        # given
        username, password = "johndoe", "password"
        command = AuthenticateUser(username=username, password=password)

        fake_web.post(f"{fake_auth_base_url}/api/v1/auth/token",
                      payload={"data": TokenGenerated(token="eyExampleToken").dict(by_alias=True)},
                      status=HTTP_200_OK)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post(f"/api/v1/auth-service/auth/token", json=command.dict(by_alias=True))

            # then
            assert response.status_code == HTTP_200_OK

    def test_authentication_error_then_unauthorized(self, test_client, aio_http_client, fake_web):
        # given
        username, password = "johndoe", "password"
        command = AuthenticateUser(username=username, password=password)
        fake_web.post(f"{fake_auth_base_url}/api/v1/auth/token",
                      payload={"detail": "Invalid credentials"},
                      status=HTTP_401_UNAUTHORIZED)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post(f"/api/v1/auth-service/auth/token", json=command.dict(by_alias=True))

            # then
            assert response.status_code == HTTP_401_UNAUTHORIZED
