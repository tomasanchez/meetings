"""
Test Register Service
"""
import pytest

from auth.adapters.repository import UserRepository
from auth.domain.models import User
from auth.service_layer.errors import IllegalUserError
from auth.service_layer.password_encoder import PasswordEncoder
from auth.service_layer.register import RegisterService


class TestRegisterService:
    """
    Unit test suite for the register in the service layer
    """

    def test_registers_with_encoded_password(self,
                                             user_repository: UserRepository,
                                             password_encoder: PasswordEncoder,
                                             register_service: RegisterService):
        """
        Test that the register service registers a user with an encoded password
        """

        # Given
        username, email, password = ("user1", "user@mail.com", "password1")

        # When
        registered_user = register_service.register(username=username, email=email, password=password)

        # Then
        password_encoder.verify(password, registered_user.password)

        assert registered_user in user_repository.find_all()

    def test_cannot_register_with_existing_username(self,
                                                    user_repository: UserRepository,
                                                    register_service: RegisterService
                                                    ):
        """
        Test that the register service raises an error when an existing username is provided.
        """

        # Given
        user_repository.save(User(username="user1", password="password1", email="an@email.com"))

        username, email, password = ("user1", "another@email.com", "password1")

        # When / Then
        with pytest.raises(IllegalUserError):
            register_service.register(username=username, email=email, password=password)

    def test_cannot_register_with_existing_email(self,
                                                 user_repository: UserRepository,
                                                 register_service: RegisterService
                                                 ):
        """
        Test that the register service raises an error when an existing email is provided.
        """

        # Given
        username, email, password = ("user2", "user2@email.com", "password1")

        user_repository.save(User(username=username, password=password, email=email))

        other_username = "user3"

        # When / Then
        with pytest.raises(IllegalUserError):
            register_service.register(username=other_username, email=email, password=password)
