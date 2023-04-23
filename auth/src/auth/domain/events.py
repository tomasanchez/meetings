"""
Events that may occur in the application.
"""
import datetime

from pydantic import EmailStr, Field

from auth.domain.models import Role
from auth.domain.schemas import CamelCaseModel


class HealthChecked(CamelCaseModel):
    """
    Event that occurs when the application is health checked.
    """
    status: str = Field(description="The status of the application.", example="OK", default="OK")


class UserRegistered(CamelCaseModel):
    """
    Event that occurs when a user is persisted or retrieved.
    """

    id: str = Field(description="The user id.", example="1")
    username: str = Field(description="The user username.", example="johndoe")
    email: EmailStr = Field(description="The user email.", example="johndoe@mail.com")
    role: Role = Field(description="The user role.", example=Role.USER)
    first_name: str | None = Field(description="The user first name.", example="John")
    last_name: str | None = Field(description="The user last name.", example="Doe")
    profile_picture: str | None = Field(title="Profile Picture URL", description="The user profile picture.",
                                        example="https://example.com/profile.jpg")
    is_active: bool | None = Field(title="Is Active", description="The user is active.", example=True)


class UserAuthenticated(CamelCaseModel):
    """
    Event that occurs when a user is authenticated.
    """
    id: str = Field(description="The user id.", example="1")
    username: str = Field(description="The user username.", example="johndoe")
    email: EmailStr = Field(description="The user email.", example="john@doe.mail")
    role: Role = Field(description="The user role.", example=Role.USER)
    exp: datetime.datetime | None = Field(description="The expiration date of the token.",
                                          example="2021-01-01T00:00:00Z")
