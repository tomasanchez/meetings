"""
This module contains pytest fixtures.
"""
import pytest
from starlette.testclient import TestClient

from auth.app.asgi import get_application


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client for the app.
    """
    return TestClient(get_application())
