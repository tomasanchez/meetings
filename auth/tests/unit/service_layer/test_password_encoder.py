"""
Tests for the password encoder service.
"""
import pytest

from auth.service_layer.errors import InvalidCredentialsError


class TestPasswordEncoder:

    def test_encode(self, password_encoder):
        """
        Test that a password is encoded.
        """
        password = "password"
        encoded_password = password_encoder.encode(password)
        assert encoded_password != password

    def test_verify(self, password_encoder):
        """
        Test that a password is verified.
        """
        password = "password"
        encoded_password = password_encoder.encode(password)
        password_encoder.verify(password, encoded_password)

    def test_verify_invalid_password(self, password_encoder):
        """
        Test that an invalid password is not verified.
        """
        password = "password"
        encoded_password = password_encoder.encode(password)

        with pytest.raises(InvalidCredentialsError):
            password_encoder.verify("invalid_password", encoded_password)
