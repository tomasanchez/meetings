"""
Generic mocks for testing purposes.
"""

from typing import Generic

from auth.adapters.repository import Repository, T, UserRepository
from auth.domain.models import User


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
