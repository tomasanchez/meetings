"""
Tests for the scheduler service gateway.
"""
from typing import Any, Callable
import uuid

from aioresponses import aioresponses
import pytest
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_503_SERVICE_UNAVAILABLE

from app.dependencies import get_async_http_client, get_services
from app.domain.models import Service
from tests.conftest import DependencyOverrider

FAKE_SCHEDULER_URL = "http://fake-scheduler-service:8001"


def fake_schedule_response(meeting_id: str | None = None) -> dict[str, Any]:
    """
    Fake schedule response.

    Returns:
        dict[str, Any]: The fake schedule response.
    """
    return {"data": {
        "id": meeting_id or str(uuid.uuid4()),
        "organizer": "johndoe",
        "voting": False,
        "title": "Meeting with the team",
        "description": "We will discuss the new project",
        "location": "Zoom",
        "guests": [],
        "options": [
            {
                "date": "2023-05-03T23:59:00",
                "votes": []
            }
        ]
    }}


class TestSchedulerServiceGateway:
    """
    Tests for the scheduler service gateway.
    """

    @pytest.fixture
    def fake_web(self):
        with aioresponses() as mock:
            yield mock

    overrides: dict[Callable, Callable] = {
        get_services: lambda: [Service(name="scheduler", base_url=FAKE_SCHEDULER_URL)],
    }


class TestSchedulerQueries(TestSchedulerServiceGateway):

    def test_get_schedules(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to get all schedules, and a working service
        WHEN the request is made
        THEN it should return all schedules.
        """
        fake_web.get(f"{FAKE_SCHEDULER_URL}/api/v1/schedules", payload={"data": []}, status=HTTP_200_OK)
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get("/api/v1/scheduler-service/schedules")
            # then
            assert response.status_code == HTTP_200_OK

    def test_service_unavailable(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to get all schedules, and a service that is not available
        WHEN the request is made
        THEN it should return a service unavailable error.
        """
        fake_web.get(f"{FAKE_SCHEDULER_URL}/api/v1/schedules", payload={}, status=HTTP_503_SERVICE_UNAVAILABLE)
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get("/api/v1/scheduler-service/schedules")
            # then
            assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE

    def test_get_schedule_by_id(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to get a schedule by id, and a working service
        WHEN the request is made
        THEN it should return the schedule.
        """
        fake_web.get(f"{FAKE_SCHEDULER_URL}/api/v1/schedules/1",
                     payload=fake_schedule_response(meeting_id="1"),
                     status=HTTP_200_OK)
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get("/api/v1/scheduler-service/schedules/1")
            # then
            assert response.status_code == HTTP_200_OK

    def test_get_schedule_by_id_not_found(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to get a schedule by id, and a working service
        WHEN the request is made
        THEN it should return the schedule.
        """
        fake_web.get(f"{FAKE_SCHEDULER_URL}/api/v1/schedules/1",
                     payload={"detail": "Not found."},
                     status=HTTP_404_NOT_FOUND)
        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.get("/api/v1/scheduler-service/schedules/1")
            # then
            assert response.status_code == HTTP_404_NOT_FOUND
