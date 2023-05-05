"""
Tests Mocks
"""
import datetime
from typing import Any
from uuid import uuid4

from pydantic import EmailStr

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
