"""
Events that may occur in the Auth Service.
"""
import datetime

from pydantic import EmailStr, Field

from app.domain.models import Role
from app.domain.schemas import CamelCaseModel


class UserRegistered(CamelCaseModel):
    """
    Event that occurs when a user is persisted or retrieved.
    """

    id: str = Field(description="The user id.", example="1")
    username: str = Field(description="The user username.", example="johndoe")
    email: EmailStr = Field(description="The user email.", example="johndoe@mail.com")
    role: Role = Field(description="The user role.", example=Role.USER, default=Role.USER)
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


class TokenGenerated(CamelCaseModel):
    """
    Event that occurs when a token is generated.
    """
    token: str = Field(description="A JSON Web Token",
                       example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJlbWFpbCI6ImpvaG5kb"
                               "2VAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJleHAiOjE2MjUwMzg4MjB9.5Y2QJ7kx1yD6Bh0jzH2QX9Y8cZJ"
                               "6vZl6YpKj1Z8JUWU")
    type: str = Field(description="Token Type", example="Bearer", default="Bearer")
