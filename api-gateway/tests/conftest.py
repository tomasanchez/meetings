"""
This module contains pytest fixtures.
"""
import typing

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from app.adapters.http_client import AiohttpClient, AsyncHttpClient
from app.main import app


class DependencyOverrider:
    """
    A context manager for overriding FastAPI dependencies.
    """

    def __init__(
            self, overrides: typing.Mapping[typing.Callable, typing.Callable]
    ) -> None:
        self.overrides = overrides
        self._app = app
        self._old_overrides = {}

    def __enter__(self):
        for dep, new_dep in self.overrides.items():
            if dep in self._app.dependency_overrides:
                # Save existing overrides
                self._old_overrides[dep] = self._app.dependency_overrides[dep]
            self._app.dependency_overrides[dep] = new_dep
        return self

    def __exit__(self, *args: typing.Any) -> None:
        for dep in self.overrides.keys():
            if dep in self._old_overrides:
                # Restore previous overrides
                self._app.dependency_overrides[dep] = self._old_overrides.pop(dep)
            else:
                # Just delete the entry
                del self._app.dependency_overrides[dep]


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
