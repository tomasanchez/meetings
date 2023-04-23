"""
Maps the different domain objects.
"""
from auth.domain.events import UserRegistered
from auth.domain.models import User


def user_model_to_user_registered(user: User) -> UserRegistered:
    """
    Maps a user model to a user registered event.
    """
    return UserRegistered(**user.dict())
