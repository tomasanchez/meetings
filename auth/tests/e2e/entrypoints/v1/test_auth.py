"""
Test Authentication & Authorization Entry Points
"""
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from auth.app.dependencies import get_user_repository
from auth.domain.commands import AuthenticateUser, AuthorizeToken, RegisterUser
from auth.domain.events import UserAuthenticated
from auth.domain.models import Role
from tests.conftest import DependencyOverrider


class TestAuthEntryPoint:

    def test_registered_user_can_login(self, test_client, register_service, user_repository):
        """
        Tests that a user which has been registered can log in.
        """
        # given
        command = RegisterUser(username='johndoe', email="john@doe.mail", password='aStrongPassword')
        register_service.register(username=command.username, email=command.email, password=command.password)
        overrides = {get_user_repository: lambda: user_repository}
        log_in_command = AuthenticateUser(username=command.username, password=command.password)

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post('/api/v1/auth/token', json=log_in_command.dict())

            # then
            assert response.status_code == HTTP_200_OK

    def test_unregistered_user_cannot_login(self, test_client, user_repository):
        """
        Tests that a user which has not been registered cannot log in.
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        log_in_command = AuthenticateUser(username='johndoe', password='aStrongPassword')

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post('/api/v1/auth/token', json=log_in_command.dict())

            # then
            assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_user_cannot_login_with_wrong_password(self, test_client, register_service, user_repository):
        """
        Tests that a user which has been registered cannot log in with a wrong password.
        """
        # given
        command = RegisterUser(username='johndoe', email="john@doe.mail", password='aStrongPassword')
        register_service.register(username=command.username, email=command.email, password=command.password)
        overrides = {get_user_repository: lambda: user_repository}
        log_in_command = AuthenticateUser(username=command.username, password="anInvalidPassword")

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post('/api/v1/auth/token', json=log_in_command.dict())

            # then
            assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_user_can_be_authorized(self, test_client, register_service, auth_service, user_repository):
        """
        Tests that a user which has been registered can log in and be authorized.
        """
        # given
        command = RegisterUser(username='johndoe', email="a@email.com", password='aStrongPassword')
        register_service.register(username=command.username, email=command.email, password=command.password)
        token = auth_service.authenticate(username=command.username, password=command.password)
        overrides = {get_user_repository: lambda: user_repository}

        authorize_command = AuthorizeToken(token=token)

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post('/api/v1/auth/user', json=authorize_command.dict())

            username = response.json()['data']['username']

            # then
            assert response.status_code == HTTP_200_OK
            assert username == command.username

    def test_invalid_token_is_not_authorized(self, test_client, user_repository):
        """
        Tests that an invalid token format is not authorized.
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        authorize_command = AuthorizeToken(token="anInvalidToken")

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post('/api/v1/auth/user', json=authorize_command.dict())

            # then
            assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_fake_token_is_not_authorized(self, test_client, user_repository, jwt_service):
        """
        Tests that a fake token is not authorized.
        """
        # given
        overrides = {get_user_repository: lambda: user_repository}
        fake_event = UserAuthenticated(id="13", username="johndoe", email="j@doe.mail", role=Role.USER)
        authorize_command = AuthorizeToken(token=jwt_service.get_token(fake_event))

        with DependencyOverrider(overrides=overrides):
            # when
            response = test_client.post('/api/v1/auth/user', json=authorize_command.dict())

            # then
            assert response.status_code == HTTP_401_UNAUTHORIZED
