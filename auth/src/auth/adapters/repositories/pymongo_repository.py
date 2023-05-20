"""
PyMongo Repository implementations
"""
import abc

from fastapi.encoders import jsonable_encoder
from pymongo.database import Database

from auth.adapters.repository import ReadOnlyRepository, T, UserRepository, WriteOnlyRepository
from auth.domain.models import User


class PyMongoRepositoryMixin:

    def __init__(self, database: Database, model_factory: type[T]):
        self._model_factory = model_factory
        self._collection = database.get_collection(model_factory.__name__)

    def to_output_model(self, document: dict) -> T:
        """
        Converts a document to the output model type.

        Args:
            document: a retrieved document from the database.

        Returns:
            T: an Entity instance
        """
        return self._model_factory(**document)

    def _build_query(self, query: dict | None = None) -> dict | None:
        """
        Builds a query from a dictionary.

        Args:
            query (dict | None): The query.

        Returns:
            dict: The built query.

        """
        if query is None:
            return None

        filter_query = dict()

        for filter_attribute, value in query.items():

            if filter_attribute not in self._model_factory.__fields__:
                continue

            if isinstance(value, list):
                filter_query[filter_attribute] = {"$in": value}
            else:
                filter_query[filter_attribute] = value

        return filter_query


class PyMongoReadOnlyRepository(PyMongoRepositoryMixin, ReadOnlyRepository, abc.ABC):
    """
    A PyMongo Read Only base implementation
    """

    def find_all(self, **kwargs) -> list[T]:
        query: dict | None = kwargs.get("filters", None)
        filters: dict | None = self._build_query(query)

        if filters is None:
            documents = self._collection.find(kwargs)
        else:
            kwargs.pop("filters")
            documents = self._collection.find(filters, kwargs)

        return [self.to_output_model(doc) for doc in documents]

    def find_by(self, **kwargs) -> T | None:
        result = self._collection.find_one(kwargs)

        return self._model_factory(**result) if result else None


class PyMongoWriteOnlyRepository(PyMongoRepositoryMixin, WriteOnlyRepository, ):
    """
    A PyMongo Write Only base implementation.
    """

    def save(self, *entries: T, **kwargs) -> None:
        documents = [jsonable_encoder(entity) for entity in entries]

        identifiers = [entity.id for entity in entries]

        if len(entries) == 1:
            [identifier] = identifiers
            [document] = documents
            criteria = {"_id": identifier}

            self._collection.replace_one(criteria, document, upsert=True)
            return

        self._collection.insert_many(documents, **kwargs)

    def delete(self, *deletions: T, **kwargs) -> None:

        identifiers = [entity.id for entity in deletions]

        if len(identifiers) == 1:
            [identifier] = identifiers
            self._collection.delete_one({"_id": identifier}, kwargs)
            return

        self._collection.delete_many({
            "_id": {"$in": identifiers}}, kwargs)


class PyMongoRepository(PyMongoReadOnlyRepository, PyMongoWriteOnlyRepository, abc.ABC):
    """
    A Pymongo Repository.
    """
    pass


class PymongoUserRepository(PyMongoRepository, UserRepository):
    """
    A User Repository
    """

    def __init__(self, database: Database):
        super().__init__(database, User)

    def find_by_username(self, username: str) -> User | None:
        return self.find_by(username=username)
