"""
Uvicorn Configuration Settings
"""
from pydantic import BaseSettings


class UvicornSettings(BaseSettings):
    """Uvicorn Configuration Settings

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * UVICORN_APP
        * UVICORN_HOST
        * UVICORN_PORT
        * UVICORN_RELOAD

    Attributes:
        APP (str): The application module path.
        HOST (str): The host to bind to.
        PORT (int): The port to bind to.
        RELOAD (bool): Whether to reload the server on code changes.
    """

    APP: str = "src.auth.main:app"
    HOST: str = "127.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

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
        env_prefix = "UVICORN_"
