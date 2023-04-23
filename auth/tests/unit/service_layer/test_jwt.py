"""
Tests for the JWT service.
"""
import pytest

from auth.domain.events import UserAuthenticated
from auth.domain.models import Role
from auth.service_layer.errors import InvalidCredentialsError
from auth.service_layer.jwt import JwtService


class TestJwt:

    def test_token_can_be_encoded(self, jwt_service: JwtService):
        """
        Tests that a token can be encoded.
        """
        # given
        event = UserAuthenticated(
            id="anId",
            username="test",
            email="test@e.mail",
            role=Role.USER,
        )

        # when
        token = jwt_service.get_token(event)

        # then
        assert len(token) > 0

    def test_token_can_be_decoded(self, jwt_service: JwtService):
        """
        Tests that a token can be decoded.
        """
        # given
        event = UserAuthenticated(
            id="anId",
            username="test",
            email="test@e.mail",
            role=Role.USER,
        )
        token = jwt_service.get_token(event)

        # when
        event_decoded = jwt_service.decode_user_token(token)

        # then
        assert event_decoded.email == event.email
        assert event_decoded.username == event.username
        assert event_decoded.role == event.role
        assert event_decoded.id == event.id

    def test_token_is_invalid(self, jwt_service: JwtService):
        """
        Tests that an invalid token raises an error.
        """
        # given
        token = "invalidToken"

        # when
        with pytest.raises(InvalidCredentialsError):
            jwt_service.decode_user_token(token)
