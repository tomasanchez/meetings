"""
Events from scheduler service.
"""
import datetime

from pydantic import Field

from app.domain.schemas import CamelCaseModel


class OptionVoted(CamelCaseModel):
    """
    Event emitted when an option is voted.
    """
    date: datetime.datetime = Field(description="A tentative date for a meeting")
    votes: list[str] = Field(description="A list of usernames that voted for the option.", example=["johndoe"])


class MeetingScheduled(CamelCaseModel):
    """
    Event emitted when a meeting is scheduled.
    """

    id: str = Field(description="The meeting's unique identifier.", example="6442ee3291a1304d4c88ffc9")
    organizer: str = Field(description="Username of who scheduled the meeting.", example="johndoe")
    voting: bool = Field(description="Whether mode voting is enabled.", example=True)
    title: str = Field(description="The meeting's title.", example="Sprint Planning")
    description: str | None = Field(description="The meeting's description.", example="Planning the next sprint.")
    location: str | None = Field(description="The meeting's location.", example="Room 1")
    date: datetime.datetime | None = Field(description="The meeting's date.", example="2021-01-01T09:30:00Z")
    guests: list[str] = Field(description="A list of guests.", example=["johndoe", "clarasmith"], default_factory=list)
    options: list[OptionVoted] = Field(description="A list of options.")
