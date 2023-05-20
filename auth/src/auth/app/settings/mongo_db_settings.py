"""
Mongo Settings module.
"""

from pydantic import BaseSettings


class MongoDbSettings(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * MONGO_CLIENT
        * MONGO_USER
        * MONGO_PASSWORD

    Attributes:
        CLIENT (str): MongoDB client url.
        USER (str): MongoDB user.
        PASSWORD (str): MongoDB password.
    """

    CLIENT: str = "mongodb://localhost:27017"
    DATABASE: str = "auth"
    USER: str | None = None
    PASSWORD: str | None = None

    class Config:
        """Config subclass needed to customize BaseSettings settings.
        Attributes:
            case_sensitive (bool): When case_sensitive is True, the environment
                variable names must match field names (optionally with a prefix)
            env_prefix (str): The prefix for environment variable.
        Resources:
            https://pydantic-docs.helpmanual.io/usage/settings/
        """

        case_sensitive = True
        env_prefix = "MONGO_"
