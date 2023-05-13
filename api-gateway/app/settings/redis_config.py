"""Application configuration - Redis."""

from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    """Define Redis configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * REDIS_HOST
        * REDIS_PORT
        * REDIS_CLUSTER
        * REDIS_USERNAME
        * REDIS_PASSWORD

    Attributes:
        HOST (str): Redis host.
        PORT (int): Redis port.
        CLUSTER (bool): Redis cluster.
        USERNAME (typing.Optional[str]): Redis username.
        PASSWORD (typing.Optional[str]): Redis password.
    """

    HOST: str = "localhost"
    PORT: int = 6379
    CLUSTER: bool = False
    USERNAME: str | None = None
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
        env_prefix = "REDIS_"
