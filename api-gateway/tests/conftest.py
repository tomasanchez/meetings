"""
This module contains pytest fixtures.
"""

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from app.adapters.http_client import AiohttpClient, AsyncHttpClient
from app.main import app


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client for the app.
    """
    return TestClient(app)


@pytest_asyncio.fixture(name="aio_http_client")
async def fixture_aio_http_client() -> AsyncHttpClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client for the app.
    """
    client = AiohttpClient()
    client.get_aiohttp_client()
    yield client
    await client.close_aiohttp_client()
