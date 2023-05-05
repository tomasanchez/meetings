"""
Text formatter
"""
import json
from re import sub
from typing import Any

from pydantic import BaseModel


def to_camel(s: str) -> str:
    """
    Translates a string to camel case.

    Args:
        s (str): The string to translate.
    """
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def to_jsonable_dict(model: BaseModel) -> dict[str, Any]:
    """
    Converts a pydantic model to a json-encode-able dictionary.

    Args:
        model (BaseModel): The model to convert.

    Returns:
        dict[str, Any]: The converted model.
    """
    return json.loads(model.json(by_alias=True))
