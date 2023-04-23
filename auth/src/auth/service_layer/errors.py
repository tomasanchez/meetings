""" Application Service Errors
"""


class InvalidCredentialsError(Exception):
    """
    Exception raised when the username or passwords are invalid.
    """
    pass


class UserAlreadyExistsError(Exception):
    """
    Raised when a user wants to use a taken username or taken email.
    """
    pass
