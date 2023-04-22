"""
Events that may occur in the application.
"""
from pydantic import Field

from auth.domain.schemas import CamelCaseModel


class HealthChecked(CamelCaseModel):
    """
    Event that occurs when the application is health checked.
    """
    status: str = Field(description="The status of the application.", example="OK", default="OK")
