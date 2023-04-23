"""
Test Authentication & Authorization Service
"""
import pytest

from auth.service_layer.errors import InvalidCredentialsError


class TestAuth:

    def test_user_gets_working_token(self, auth_service, register_service):
        """
        Tests that a user can authenticate receiving a usable token.
        """
        # given
        username, email, password = ("user", "a@e.mail", "aGreatPassword")
        register_service.register(username=username, email=email, password=password)
        token = auth_service.authenticate(username=username, password=password)

        # when
        event = auth_service.authorize(token=token)

        # then
        assert event.username == username
        assert event.email == email

    def test_token_is_not_verifiable(self, auth_service):
        """
        Tests that a user cannot authenticate with invalid credentials.
        """
        # given
        token = "invalid_token"

        # when
        with pytest.raises(InvalidCredentialsError):
            auth_service.authorize(token=token)

    def test_user_can_not_authenticate_with_invalid_credentials(self, auth_service, register_service):
        """
        Tests that a user cannot authenticate with invalid credentials.
        """
        # given
        username, email, password = ("user", "user@e.mail", "aGreatPassword")
        register_service.register(username=username, email=email, password=password)

        # when
        with pytest.raises(InvalidCredentialsError):
            auth_service.authenticate(username=username, password="invalid_password")

    def test_user_can_not_authenticate_with_invalid_username(self, auth_service):
        """
        Tests that a user cannot authenticate with invalid username.
        """
        # given
        username, email, password = ("nonExistentUser", "user@e.mail", "aGreatPassword")

        # when
        with pytest.raises(InvalidCredentialsError):
            auth_service.authenticate(username=username, password=password)
