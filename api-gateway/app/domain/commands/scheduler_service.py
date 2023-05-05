"""
Scheduler Commands
"""
import datetime

from pydantic import Field

from app.domain.schemas import CamelCaseModel


class ProposeOption(CamelCaseModel):
    """
    Command to propose a meeting option.
    """

    date: datetime.date = Field(description="The date of the meeting.", example="2021-01-01")
    hour: int = Field(description="The hour of the meeting.", example="12", max=23, min=0)
    minute: int = Field(description="The minute of the meeting.", example="30", max=59, min=0)


class ScheduleMeeting(CamelCaseModel):
    """
    Command to schedule a meeting.
    """

    organizer: str = Field(description="Responsible for the meeting's username.", example="johndoe")
    title: str | None = Field(description="The meeting's title.", example="Coffee with John Doe")
    description: str | None = Field(description="The meeting's description.",
                                    example="A meeting to discuss the project.")
    location: str | None = Field(description="The meeting's location.", example="Floor 3, Cafeteria")
    options: list[ProposeOption] = Field(description="A list of options to schedule the meeting.", min_items=1)
    guests: set[str] = Field(description="A list of guests to invite to the meeting.",
                             example=["frank", "jane"], default_factory=set)


class ToggleVoting(CamelCaseModel):
    """
    Command to toggle voting on a meeting.
    """
    username: str = Field(description="Responsible for the meeting's username.", example="johndoe")
    voting: bool = Field(description="Whether voting is enabled", example=True, default=True)


class JoinMeeting(CamelCaseModel):
    """
    Command to join a meeting.
    """
    username: str = Field(description="Username of who wants to join a meeting", example="johndoe")


class VoteOption(CamelCaseModel):
    """
    Command to vote on a meeting option.
    """
    username: str = Field(description="Username of who wants to vote on a meeting option", example="johndoe")
    option: ProposeOption = Field(description="The option to vote on.")
