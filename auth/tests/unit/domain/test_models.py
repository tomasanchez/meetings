"""
Tests for the models in the ``auth`` application.
"""
import pytest

from auth.domain.models import Role, User


class TestModels:

    def test_user_needs_valid_email(self):
        """Test that a user needs a valid email format."""
        with pytest.raises(ValueError):
            User(
                id="1",
                username="test",
                email="test",
                password="test",
                first_name="test",
                last_name="test",
                profile_picture="test",
                is_active=True,
                role=Role.USER,
            )

    def test_user_needs_valid_role(self):
        """Test that a user needs a valid role."""
        with pytest.raises(ValueError):
            User(
                id="1",
                username="test",
                email="aValid@email.com",
                password="test",
                first_name="test",
                last_name="test",
                profile_picture="test",
                is_active=True,
                role="invalid",
            )
