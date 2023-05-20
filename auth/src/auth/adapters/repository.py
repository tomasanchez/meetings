"""
This module abstracts the Database layer with a Repository pattern.
"""
import abc
from typing import TypeVar

from auth.domain.models import BaseEntity, User

T = TypeVar("T", bound=BaseEntity)


class ReadOnlyRepository(abc.ABC):
    """
    Abstract base class for read-only repository implementations.
    """

    @abc.abstractmethod
    def find_all(self) -> list[T]:
        """
        Finds all entities.

        Returns:
            list[T] : A list of entities.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def find_by(self, **kwargs) -> T | None:
        """
        Finds an entity by its attributes.

        Args:
            **kwargs: The attributes of an entity.

        Returns:
            T : An entity if exists, otherwise None.

        """
        raise NotImplementedError


class WriteOnlyRepository(abc.ABC):
    """
    Abstract base class for write-only repository implementations.
    """

    @abc.abstractmethod
    def save(self, entity: T) -> None:
        """
        Saves an entity to the repository.

        Args:
            entity (T): The entity to save.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: T) -> None:
        """
        Deletes an entity from the repository.

        Args:
            entity (T): The entity to delete.
        """
        raise NotImplementedError


class Repository(ReadOnlyRepository, WriteOnlyRepository, abc.ABC):
    """
    Abstract base class for repository implementations.
    """
    pass


class UserRepository(Repository, abc.ABC):
    """
    Abstract base class for user repository implementations.
    """

    @abc.abstractmethod
    def find_by_username(self, username: str) -> User | None:
        """
        Finds a user by its username.

        Args:
            username (str): The username of a user.

        Returns:
            User : A user if exists, otherwise None.

        """
        raise NotImplementedError
