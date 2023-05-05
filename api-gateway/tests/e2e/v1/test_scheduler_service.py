"""
Tests for the scheduler service gateway.
"""
from typing import Any, Callable
import uuid

from aioresponses import aioresponses
import pytest
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, \
    HTTP_503_SERVICE_UNAVAILABLE

from app.dependencies import get_async_http_client, get_services
from app.domain.commands.scheduler_service import ToggleVoting
from app.domain.events.scheduler_service import MeetingScheduled
from app.domain.models import Service
from app.domain.schemas import ResponseModel
from app.utils.formatter import to_jsonable_dict
from tests.conftest import DependencyOverrider
from tests.mocks import schedule_command_factory, user_registered_factory

FAKE_SCHEDULER_URL = "http://fake-scheduler-service:8001"
FAKE_AUTH_URL = "http://fake-auth-service:8002"


def fake_schedule_response(meeting_id: str | None = None,
                           organizer: str = "johndoe",
                           guests: list[str] | None = None) -> dict[str, Any]:
    """
    Fake schedule response.

    Returns:
        dict[str, Any]: The fake schedule response.
    """
    return {"data": {
        "id": meeting_id or str(uuid.uuid4()),
        "organizer": organizer,
        "voting": False,
        "title": "Meeting with the team",
        "description": "We will discuss the new project",
        "location": "Zoom",
        "guests": guests or list(),
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
        get_services: lambda: [Service(name="scheduler", base_url=FAKE_SCHEDULER_URL),
                               Service(name="auth", base_url=FAKE_AUTH_URL),
                               ],
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


class TestSchedulerCommands(TestSchedulerServiceGateway):

    def test_schedule_meeting(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to schedule a meeting, with valid organizer
        WHEN the request is made
        THEN it should return the schedule.
        """
        command = schedule_command_factory(organizer="johndoe")

        fake_web.post(f"{FAKE_SCHEDULER_URL}/api/v1/schedules",
                      payload=fake_schedule_response(meeting_id="1"),
                      status=HTTP_201_CREATED)

        fake_web.get(f"{FAKE_AUTH_URL}/api/v1/users?usernames=johndoe",
                     payload={"data": [to_jsonable_dict(user_registered_factory(username="johndoe"))]},
                     status=HTTP_200_OK,
                     )

        self.overrides[get_async_http_client] = lambda: aio_http_client

        json = to_jsonable_dict(command)

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post("/api/v1/scheduler-service/schedules", json=json)
            # then
            assert response.status_code == HTTP_201_CREATED

    def test_scheduling_meeting_with_guests(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to schedule a meeting, with valid organizer and guests
        WHEN the request is made
        THEN it should return the schedule.
        """
        guest_1, guest_2, organizer = "carl", "jane", "johndoe"
        command = schedule_command_factory(organizer=organizer, guests={guest_1, guest_2})

        guests = {guest_1, guest_2, organizer}
        query = ", ".join(guests)
        fake_web.get(f"{FAKE_AUTH_URL}/api/v1/users?usernames={query}",
                     payload={"data": [to_jsonable_dict(user_registered_factory(username="johndoe")),
                                       to_jsonable_dict(user_registered_factory(username="carl")),
                                       to_jsonable_dict(user_registered_factory(username="jane"))
                                       ]
                              },
                     status=HTTP_200_OK,
                     )

        fake_web.post(f"{FAKE_SCHEDULER_URL}/api/v1/schedules",
                      payload=fake_schedule_response(guests=[guest_1, guest_2]),
                      status=HTTP_201_CREATED)

        json = to_jsonable_dict(command)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post("/api/v1/scheduler-service/schedules", json=json)

            response_body = ResponseModel[MeetingScheduled](**response.json())
            # then
            assert response.status_code == HTTP_201_CREATED
            assert guest_1, guest_2 in response_body.data.guests

    def test_scheduling_meeting_with_guests_not_found(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to schedule a meeting, with valid organizer and not valid guests
        WHEN the request is made
        THEN it schedules without guests
        """
        guest_1, guest_2, organizer = "carl", "jane", "johndoe"
        command = schedule_command_factory(organizer=organizer, guests={guest_1, guest_2})
        guests = {guest_1, guest_2, organizer}

        query = ", ".join(guests)
        fake_web.get(f"{FAKE_AUTH_URL}/api/v1/users?usernames={query}",
                     payload={"data": [to_jsonable_dict(user_registered_factory(username="johndoe")),
                                       ]
                              },
                     status=HTTP_200_OK,
                     )
        fake_web.post(f"{FAKE_SCHEDULER_URL}/api/v1/schedules",
                      payload=fake_schedule_response(),
                      status=HTTP_201_CREATED)

        json = to_jsonable_dict(command)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post("/api/v1/scheduler-service/schedules", json=json)

            response_body = ResponseModel[MeetingScheduled](**response.json())
            # then
            assert response.status_code == HTTP_201_CREATED
            assert guest_1, guest_2 not in response_body.data.guests

    def test_scheduling_meeting_with_organizer_not_found(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to schedule a meeting, with invalid organizer
        WHEN the request is made
        THEN it is a conflict
        """
        command = schedule_command_factory(organizer="johndoe")

        fake_web.get(f"{FAKE_AUTH_URL}/api/v1/users?usernames=johndoe",
                     payload={"data": []},
                     status=HTTP_200_OK,
                     )

        json = to_jsonable_dict(command)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.post("/api/v1/scheduler-service/schedules", json=json)
            # then
            assert response.status_code == HTTP_409_CONFLICT

    def test_toggle_voting(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to toggle voting
        WHEN the request is made
        THEN it should return the schedule.
        """
        command = ToggleVoting(username="johndoe")
        fake_web.patch(f"{FAKE_SCHEDULER_URL}/api/v1/schedules/1/voting",
                       payload=fake_schedule_response(meeting_id="1"),
                       status=HTTP_200_OK)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.patch("/api/v1/scheduler-service/schedules/1/voting",
                                         json=to_jsonable_dict(command))
            # then
            assert response.status_code == HTTP_200_OK

    def test_toggle_voting_not_found(self, test_client, fake_web, aio_http_client):
        """
        GIVEN a request to toggle voting for an invalid schedule
        WHEN the request is made
        THEN it should return NOT FOUND.
        """
        command = ToggleVoting(username="johndoe")
        fake_web.patch(f"{FAKE_SCHEDULER_URL}/api/v1/schedules/non-found/voting",
                       payload={"detail": "Not found"},
                       status=HTTP_404_NOT_FOUND)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.patch("/api/v1/scheduler-service/schedules/non-found/voting",
                                         json=to_jsonable_dict(command))
            # then
            assert response.status_code == HTTP_404_NOT_FOUND

    def test_toggle_voting_non_organizer(self, test_client, fake_web, aio_http_client):
        """
        Given a request to toggle voting for a schedule that the user is not the organizer
        WHEN the request is made
        THEN it should return FORBIDDEN.
        """
        command = ToggleVoting(username="johndoe")
        fake_web.patch(f"{FAKE_SCHEDULER_URL}/api/v1/schedules/1/voting",
                       payload={"detail": "Forbidden"},
                       status=HTTP_403_FORBIDDEN)

        self.overrides[get_async_http_client] = lambda: aio_http_client

        with DependencyOverrider(self.overrides):
            # when
            response = test_client.patch("/api/v1/scheduler-service/schedules/1/voting",
                                         json=to_jsonable_dict(command))
            # then
            assert response.status_code == HTTP_403_FORBIDDEN
