"""JWT Service

"""
from datetime import datetime, timedelta

from jose import jwt

from auth.domain.events import UserAuthenticated
from auth.service_layer.errors import InvalidCredentialsError


class JwtService:
    """
    JWT Service

    Handles the creation and decoding of JWT tokens.
    """

    def __init__(self,
                 secret_key: str = "25504cafb5843158167e6b423efab76f472d94f1b276eec960b9df1cb8a90569",
                 algorithm: str = "HS256",
                 token_expiration_minutes: int = 60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiration_minutes = token_expiration_minutes

    def get_token(self, event: UserAuthenticated) -> str:
        """
        Generates a JWT token for the user.

        Args:
            event: Credentials of the user.

        Returns:
            str: A Json Web Token.

        Raises:
            JwtError: If the token could not be encoded.
        """
        access_token_expires = timedelta(minutes=self.token_expiration_minutes)

        return self.create_token(payload=event.dict(), expires_delta=access_token_expires)

    def create_token(self, payload: dict, expires_delta: timedelta) -> str:
        """
        Encodes the payload into a JWT token.

        Args:
            payload:
            expires_delta:

        Returns:
            str: A JWT token.

        Raises:
            JwtError: If the token could not be encoded.
        """
        to_encode = payload.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_user_token(self, token: str) -> UserAuthenticated:
        """
        Decodes a JWT token.

        Args:
            token: A JWT token.

        Returns:
            dict: The decoded token.

        Raises:
            InvalidCredentialsError: If there's an error decoding the token.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            user_token = UserAuthenticated(**payload)

            return user_token
        except jwt.JWTError as e:
            raise InvalidCredentialsError(e) from e
