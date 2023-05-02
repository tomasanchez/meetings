"""
Gateway settings module.
"""

from pydantic import BaseConfig, BaseSettings

from app.domain.models import Service


class GatewaySettings(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * GATEWAY_SERVICES
        * GATEWAY_TIMEOUT

    Attributes:
        SERVICES (Service): List of services to be proxied.
        TIMEOUT (int): Timeout for requests.
    """
    SERVICES: list[Service] = [Service(name="Auth",
                                       base_url="http://localhost:8000")]
    TIMEOUT: int = 59

    class Config(BaseConfig):
        """Config subclass needed to customize BaseSettings settings.
        Attributes:
            case_sensitive (bool): When case_sensitive is True, the environment
                variable names must match field names (optionally with a prefix)
            env_prefix (str): The prefix for environment variable.
        Resources:
            https://pydantic-docs.helpmanual.io/usage/settings/
        """

        case_sensitive = True
        env_prefix = "GATEWAY_"
