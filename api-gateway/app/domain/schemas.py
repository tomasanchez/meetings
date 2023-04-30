"""Schemas

"Schemas" refers to the data models or data structures that are used to define the shape or structure of data
that your API receives or returns.

FastAPI relies on Pydantic, a data validation and settings management library, to define and use these schemas.

By defining schemas for your data, you can ensure that the data is correctly validated and formatted,
making your API more robust and reliable. Schemas can also be used to generate OpenAPI documentation automatically,
which can help both developers and consumers of your API understand its capabilities.
"""
from typing import Generic, TypeVar

from pydantic import BaseConfig, BaseModel, Field
from pydantic.generics import GenericModel

from app.utils.formatter import to_camel


class CamelCaseModel(BaseModel):
    """
    A base which attributes can be translated to camel case.
    """

    def dict(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        return super().dict(*args, **kwargs)

    def json(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        kwargs["by_alias"] = True
        return super().json(*args, **kwargs)

    class Config(BaseConfig):
        alias_generator = to_camel
        allow_population_by_field_name = True
        allow_arbitrary_types = True
        anystr_strip_whitespace = True


S = TypeVar("S", bound=CamelCaseModel)


class ResponseModel(GenericModel, Generic[S], CamelCaseModel):
    """
    A response wrapper for a single resource.
    """
    data: S = Field(description="The response data.")


class ResponseModels(GenericModel, Generic[S], CamelCaseModel):
    """
    A response wrapper for a collection of resources.
    """
    data: list[S] = Field(description="The response data list.")
