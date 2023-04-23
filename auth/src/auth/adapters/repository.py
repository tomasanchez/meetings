"""
This module abstracts the Database layer with a Repository pattern.
"""
import abc
from typing import Generic, TypeVar

from pydantic import BaseModel

from auth.domain.models import User

T = TypeVar("T", bound=BaseModel)


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


class InMemoryRepository(Repository, Generic[T]):
    """
    An in-memory repository implementation.
    """

    def __init__(self, data: dict[str, T] | None = None):
        self._data: dict[str, T] = data or dict()

    def find_all(self) -> list[T]:
        return list(self._data.values())

    def find_by(self, **kwargs) -> T | None:
        properties = kwargs.keys()
        return next(
            (entity for entity in self._data.values()
             if all(getattr(entity, p) == kwargs[p] for p in properties)),
            None)

    def save(self, entity: T) -> None:
        self._data[entity.id] = entity

    def delete(self, entity: T) -> None:
        del self._data[entity.id]


class InMemoryUserRepository(InMemoryRepository[User], UserRepository):
    """
    An in-memory user repository implementation.
    """

    def find_by_username(self, username: str) -> User | None:
        return self.find_by(username=username)
