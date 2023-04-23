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
