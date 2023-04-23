"""
Tests Users Entry point
"""
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from auth.app.dependencies import get_user_repository
from auth.domain.commands import RegisterUser
from auth.domain.events import UserRegistered
from tests.conftest import DependencyOverrider


class TestUsersEntryPoint:

    def test_query_users(self, test_client, user_repository):
        """
        Test get users
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.get("/api/v1/users")

            # then
            assert response.status_code == HTTP_200_OK

    def test_query_users_with_usernames(self, test_client, user_repository, register_service):
        """
        Tests you can filter by usernames
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        user1, user2, user3 = ("user1", "user2", "user3")

        register_service.register(username=user1, email=f"{user1}@e.mail", password="a_password")
        register_service.register(username=user2, email=f"{user2}@e.mail", password="a_password")

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.get(f"/api/v1/users?usernames={user1}, {user2.upper()}, {user3}")

            response_data = self._parse_data_list(response.json().get("data", []))

            # then
            assert response.status_code == HTTP_200_OK
            assert user1, user2 in [user.username for user in response_data]

    def test_query_existent_user(self, test_client, user_repository, register_service):
        """
        Test get existent user
        """
        # given
        username, email, password = ("johndoe", "john@doe.email", "password")
        register_service.register(username=username, email=email, password=password)
        overrides = {get_user_repository: lambda: user_repository}

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.get(f"/api/v1/users/{username}")

            user_response = self._parse_data(response.json()["data"])

            # then
            assert response.status_code == HTTP_200_OK
            assert username == user_response.username

    def test_query_non_existent_user(self, test_client, user_repository):
        """
        Test get non existent user
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.get("/api/v1/users/johndoe")

            # then
            assert response.status_code == HTTP_404_NOT_FOUND

    def test_register_user(self, test_client, user_repository):
        """
        Tests a user is registered
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        command = RegisterUser(
            username="user1",
            password="a_password",
            email="user1@e.mail"
        )

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post("/api/v1/users", json=command.dict())

            user_response = self._parse_data(response.json()["data"])

            assert response.status_code == HTTP_201_CREATED
            assert user_response.username == command.username
            assert user_response.email == command.email

    def test_cannot_register_username_in_use(self, test_client, user_repository, register_service):
        """
        Tests a user cannot be registered if username is taken
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        username = "user1"
        command = RegisterUser(
            username=username,
            password="a_password",
            email="user1@e.mail"
        )
        register_service.register(username=username, email="user@e.mail", password="a_password")

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post("/api/v1/users", json=command.dict())

            assert response.status_code == HTTP_409_CONFLICT

    def test_cannot_register_email_in_use(self, test_client, user_repository, register_service):
        """
        Tests a user cannot be registered if username is taken
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        email = "same@e.mail"
        command = RegisterUser(
            username="aUsername",
            password="a_password",
            email=email
        )
        register_service.register(username="anotherUsername", email=email, password="a_password")

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post("/api/v1/users", json=command.dict())

            assert response.status_code == HTTP_409_CONFLICT

    @staticmethod
    def _parse_data_list(data: list):
        return [TestUsersEntryPoint._parse_data(resource) for resource in data]

    @staticmethod
    def _parse_data(data: dict) -> UserRegistered:
        return UserRegistered(**data)
