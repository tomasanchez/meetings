"""
This module contains the schemas used for request/response validation in the allocation service.
"""
from typing import Generic, TypeVar

from pydantic import BaseConfig, BaseModel, Field
from pydantic.generics import GenericModel

from auth.utils.formatters import to_camel


class CamelCaseModel(BaseModel):
    """
    A base which attributes can be translated to camel case.
    """

    def dict(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)

    class Config(BaseConfig):
        alias_generator = to_camel
        allow_population_by_field_name = True
        allow_arbitrary_types = True
        anystr_strip_whitespace = True


T = TypeVar("T", bound=CamelCaseModel)


class ResponseModel(GenericModel, Generic[T], CamelCaseModel):
    """
    A base response model.
    """
    data: T = Field(..., description="The response data.")
