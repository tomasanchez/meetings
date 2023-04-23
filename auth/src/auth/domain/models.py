"""Models.
 This module contains the models used by the Auth service.
"""
from enum import Enum

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    """Role enum.
    This class represents the role of a user.
    """
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    """User model.
    This class represents a user.
    """
    id: str
    username: str
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None
    profile_picture: str | None
    is_active: bool = True
    role: Role = Role.USER

    class Config:
        orm_mode = True
