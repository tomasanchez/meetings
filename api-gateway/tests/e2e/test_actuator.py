"""
Test for actuator endpoints
"""
from aioresponses import aioresponses
import pytest
from starlette.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY, HTTP_404_NOT_FOUND, \
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_501_NOT_IMPLEMENTED, HTTP_502_BAD_GATEWAY, HTTP_503_SERVICE_UNAVAILABLE, HTTP_504_GATEWAY_TIMEOUT

from app.adapters.http_client import AsyncHttpClient
from app.dependencies import get_async_http_client, get_redis, get_services
from app.domain.models import Service
from tests.conftest import DependencyOverrider
from tests.mocks import FakeRedis


class TestActuator:
    """
    Tests for actuator endpoints.
    """

    LIVELINESS_PATH = "/health"
    READINESS_PATH = "/readiness"

    @pytest.fixture
    def fake_web(self):
        with aioresponses() as mock:
            yield mock

    def test_root_redirect_to_docs_permanently(self, test_client, ):
        """
        GIVEN a FastAPI application
        WHEN the root path is requested (GET)
        THEN it is redirected to the docs path
        """
        # when
        response = test_client.get("/").history[0]

        # then
        assert response.status_code == HTTP_301_MOVED_PERMANENTLY
        assert response.headers["location"] == "/docs"

    def test_health_check(self, test_client):
        """
        GIVEN a FastAPI application
        WHEN the health check path is requested (GET)
        THEN it returns a 200 status code
        """
        # when
        response = test_client.get(self.LIVELINESS_PATH)

        # then
        assert response.status_code == HTTP_200_OK

    def test_readiness_check_no_services(self, test_client, monkeypatch):
        """
        GIVEN a FastAPI application, and no services
        WHEN the readiness check path is requested (GET)
        THEN it returns a 200 status code
        """
        # given
        monkeypatch.setenv("REDIS_ACTIVE", "false")
        overrides = {
            get_services: lambda: []  # no services
        }

        with DependencyOverrider(overrides):
            # when
            response = test_client.get(self.READINESS_PATH)

            # then
            assert response.status_code == HTTP_200_OK

    def test_readiness_check_all_services_online(self, test_client,
                                                 fake_web,
                                                 aio_http_client: AsyncHttpClient,
                                                 ):
        """
        GIVEN a FastAPI application, and all services are online
        WHEN the readiness check path is requested (GET)
        THEN it returns a 200 status code
        """
        # given
        fake_web.get("http://service1/readiness", status=HTTP_200_OK, payload={"status": "fake"})
        fake_web.get("http://service2/readiness", status=HTTP_200_OK, payload={"status": "fake"})

        overrides = {
            get_services: lambda: [
                Service(name="service1", base_url="http://service1", readiness_url=self.READINESS_PATH),
                Service(name="service2", base_url="http://service2", readiness_url=self.READINESS_PATH),
            ],
            get_async_http_client: lambda: aio_http_client,
            get_redis: lambda: FakeRedis(ping=True)
        }

        with DependencyOverrider(overrides):
            # when
            response = test_client.get(self.READINESS_PATH)

            # then
            assert response.status_code == HTTP_200_OK

    @pytest.mark.parametrize("error_status", [
        HTTP_404_NOT_FOUND,
        HTTP_405_METHOD_NOT_ALLOWED,
        HTTP_500_INTERNAL_SERVER_ERROR,
        HTTP_501_NOT_IMPLEMENTED,
        HTTP_502_BAD_GATEWAY,
        HTTP_503_SERVICE_UNAVAILABLE,
        HTTP_504_GATEWAY_TIMEOUT
    ])
    def test_readiness_check_some_services_offline(self, test_client,
                                                   fake_web,
                                                   error_status,
                                                   aio_http_client: AsyncHttpClient):
        """
        GIVEN a FastAPI application, and some services are offline
        WHEN the readiness check path is requested (GET)
        THEN it returns a 503 status code
        """
        # given
        fake_web.get("http://service1/readiness", status=HTTP_200_OK, payload={"status": "fake"})
        fake_web.get("http://service2/readiness", status=error_status, payload={"status": "fake"})

        overrides = {
            get_services: lambda: [
                Service(name="service1", base_url="http://service1", readiness_url=self.READINESS_PATH),
                Service(name="service2", base_url="http://service2", readiness_url=self.READINESS_PATH),
            ],
            get_async_http_client: lambda: aio_http_client,
            get_redis: lambda: FakeRedis(ping=False)
        }

        with DependencyOverrider(overrides):
            # when
            response = test_client.get(self.READINESS_PATH)

            # then
            assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
