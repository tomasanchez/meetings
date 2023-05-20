"""
Session Factories
"""
from pymongo import MongoClient

mongo_client: MongoClient | None = None


class ClientFactory:
    """
    Database Client Factory
    """

    def __init__(self,
                 client: str,
                 **kwargs):
        """
        Args:
            client: The client to use.
        """
        global mongo_client

        if mongo_client is None:
            mongo_client = MongoClient(client, **kwargs)

        self._client: MongoClient = mongo_client

    def __call__(self):
        return self._client
