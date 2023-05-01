"""
Business objects
"""
from enum import Enum

from pydantic import BaseModel


class ServiceStatus(str, Enum):
    """Service status enumeration.

    Attributes:
        ONLINE (str): Service is online.
        OFFLINE (str): Service is offline.
    """

    ONLINE = "online"
    OFFLINE = "offline"


class Service(BaseModel):
    """Service business object.

    Attributes:
        name (str): Service name.
    """

    name: str
    base_url: str
    readiness_url: str = "/readiness"
    health_url: str = "/health"
