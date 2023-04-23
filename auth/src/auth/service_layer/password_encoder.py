"""Password Encoder
Encodes and decodes passwords using the bcrypt algorithm.
"""
import abc

from passlib.context import CryptContext

from auth.service_layer.errors import InvalidCredentialsError


class PasswordEncoder(abc.ABC):
    """
    Abstract Password Encoder
    """

    @abc.abstractmethod
    def encode(self, password: str) -> str:
        """
        Encodes a password.

        Args:
            password (str): The password to encode.

        Returns:
            str: The encoded password.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def verify(self, password: str, encoded_password: str):
        """
        Verifies a password.

        Args:
            password (str): The password to verify.
            encoded_password (str): The encoded password to compare with.

        Raises:
            InvalidPasswordException: If the password is invalid.
        """
        raise NotImplementedError


class BcryptPasswordEncoder(PasswordEncoder):
    """
    BCrypt Password Encoder
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encode(self, password: str) -> str:
        """
        Encodes a password.

        Args:
            password (str): The password to encode.

        Returns:
            str: The encoded password.
        """
        return self.pwd_context.hash(password)

    def verify(self, password: str, encoded_password: str):
        """
        Verifies a password.

        Args:
            password (str): The password to verify.
            encoded_password (str): The encoded password to compare with.

        Raises:
            InvalidPasswordException: If the password is invalid.
        """

        try:
            result = self.pwd_context.verify(password, encoded_password)

            if result is None:
                return

            if isinstance(result, bool) and not result:
                raise ValueError("Password does not match.")

        except (ValueError, TypeError) as e:
            raise InvalidCredentialsError("Password does not match.") from e
