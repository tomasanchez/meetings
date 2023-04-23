"""Commands
A command represents an intent to change the state of the system, it is a message that requests some action to be taken.

Commands are passed to command handlers, which interpret them and execute
the corresponding actions to produce new events that update the system state.

Commands should be immutable, and their properties should be as minimal as possible.
"""
from pydantic import EmailStr, Field, validator

from auth.domain.models import Role
from auth.domain.schemas import CamelCaseModel

min_length = 8


class RegisterUser(CamelCaseModel):
    """
    Command that represents the intent to register a new user.
    """
    username: str = Field(description="The user username.", example="johndoe")
    email: EmailStr = Field(description="The user email.", example="john@doe.com")
    password: str = Field(title="Password", description="Login Credential", min_length=min_length)
    role: Role = Field(description="The user role.", example=Role.USER, default=Role.USER)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v.strip()


class AuthenticateUser(CamelCaseModel):
    """
    Command that represents the intent to authenticate a user.
    """
    username: str = Field(description="The user username.", example="johndoe")
    password: str = Field(title="Password", description="Login Credential", min_length=min_length)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v.strip().lower()


class AuthorizeToken(CamelCaseModel):
    """
    Command that represents the intent to authorize a token.
    """
    token: str = Field(description="A JSON Web Token",
                       example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJlbWFpbCI6ImpvaG5kb"
                               "2VAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJleHAiOjE2MjUwMzg4MjB9.5Y2QJ7kx1yD6Bh0jzH2QX9Y8cZJ"
                               "6vZl6YpKj1Z8JUWU")
