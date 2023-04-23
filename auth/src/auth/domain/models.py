"""Models.
 This module contains the models used by the Auth service.
"""
from enum import Enum
import uuid

from pydantic import BaseModel, EmailStr, Field, validator


def object_id() -> str:
    """
    Id generator ObjectID
    """
    return str(uuid.uuid4())


class BaseEntity(BaseModel):
    """
    Base Model
    """
    id: str = Field(default_factory=object_id, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


class Role(str, Enum):
    """Role enum.
    This class represents the role of a user.
    """
    ADMIN = "admin"
    USER = "user"


class User(BaseEntity):
    """User model.
    This class represents a user.
    """
    username: str
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None
    profile_picture: str | None
    is_active: bool = True
    role: Role = Role.USER

    @validator("username")
    def lowercase_username(cls, v, **kwargs):
        return v.lower()
