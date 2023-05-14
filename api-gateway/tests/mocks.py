"""
Tests Mocks
"""
import datetime
from datetime import timedelta
from typing import Any
from uuid import uuid4

from pydantic import EmailStr

from app.adapters.redis_connector import R, RedisConnector
from app.domain.commands.scheduler_service import ProposeOption, ScheduleMeeting
from app.domain.events.auth_service import UserRegistered


def user_registered_factory(username: str, user_id: str | None = None) -> UserRegistered:
    """
    Creates a UserRegistered event.

    Args:
        username (str): The username.
        user_id (str, optional): The user id. Defaults to uuid4.

    Returns:
        UserRegistered: The UserRegistered with the given username and user id, and a fake email.
    """
    return UserRegistered(username=username, id=user_id or str(uuid4()), email=EmailStr(f"{username}@e.mail"))


def user_registered_response_factory(username: str, user_id: str | None = None) -> dict[str, Any]:
    """
    Creates a UserRegistered response.

    Args:
        username (str): The username.
        user_id (str, optional): The user id. Defaults to uuid4.

    Returns:
        dict[str, Any]: The UserRegistered response with the given username and user id, and a fake email.
    """

    return {
        "data": user_registered_factory(username, user_id).dict(by_alias=True)
    }


def schedule_command_factory(organizer: str,
                             title: str = "Test Meeting", guests: set[str] | None = None) -> ScheduleMeeting:
    """
    Creates a schedule command.

    Args:
        organizer (str): The organizer.
        title (str, optional): The title. Defaults to "Test Meeting".
        guests (set[str], optional): The guests. Defaults to None.

    Returns:
        dict[str, Any]: The schedule command.
    """
    fake_options = [ProposeOption(date=datetime.date.today(), hour=12, minute=30)]
    return ScheduleMeeting(organizer=organizer, title=title, guests=guests or set(), options=fake_options)


class FakeRedis(RedisConnector):

    def __init__(self, ping: bool = False, data: dict | None = None):
        self._ping = ping
        self.data = data or dict()

    async def close(self):
        pass

    async def ping(self) -> bool:
        return self._ping

    async def set(self, key: str, value: str) -> R:
        self.data[key] = value
        return "OK"

    async def get(self, key: str) -> str | None:
        return self.data.get(key, None)

    async def exists(self, key: str) -> bool:
        return key in self.data

    async def expire(self, key: str, time: int | timedelta) -> bool:
        return True

    async def delete(self, key: str):
        del self.data[key]

    async def incr(self, key: str) -> int:
        if key not in self.data:
            await self.set(key, "0")

        incr = int(self.data[key]) + 1
        self.data[key] = str(incr)
        return incr
