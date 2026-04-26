"""CRUD_Python_Module.py

Reusable MongoDB CRUD module.

This module implements a MongoDB CRUD class.
Authentication is configured in the class initializer.
The create, read, update, and delete methods allow specifying the target
database and collection.
"""

# Imports
from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.errors import PyMongoError


# Class definition
class PyCRUD:
    """Implements CRUD operations for MongoDB collections."""

    def __init__(
            self,
            username: str,
            password: str,
            host: str = "localhost",
            port: int = 27017,
    ):
        """Initialize the MongoDB client using provided credentials.

        Args:
            username: MongoDB username.
            password: MongoDB password.
            host: MongoDB host name or IP address.
            port: MongoDB port number.
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        # Attempt to connect to DB
        try:
            self.client = MongoClient(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}",
                                      serverSelectionTimeoutMS=5000)
        except PyMongoError as exc:
            raise ConnectionError("Unable to connect to MongoDB with the provided credentials.") from exc

    def create(self, database_name: str, collection_name: str, data: Dict[str, Any]) -> bool:
        """Attempts to insert a document into the provided database and collection.

        Args:
            database_name: Target MongoDB database name.
            collection_name: Target MongoDB collection name.
            data: Dictionary of key/value pairs to insert.

        Returns:
            True if the insert succeeds, otherwise False.
        """
        if not isinstance(data, dict) or not data:
            return False

        try:
            database = self.client[database_name]
            collection = database[collection_name]
            result = collection.insert_one(data)
            return result.acknowledged
        except PyMongoError:
            return False

    def read(self, database_name: str, collection_name: str, query: Optional[Dict[str, Any]] = None) -> List[
        Dict[str, Any]]:
        """Query documents from the provided database and collection.

        Args:
            database_name: Target MongoDB database name.
            collection_name: Target MongoDB collection name.
            query: Dictionary of key/value pairs used by the find() call.
                When omitted, all documents in the collection are returned.

        Returns:
            A list of matching documents if successful, otherwise an empty list.
        """
        if query is None:
            query = {}

        if not isinstance(query, dict):
            return []

        try:
            database = self.client[database_name]
            collection = database[collection_name]
            cursor = collection.find(query)
            return list(cursor)
        except PyMongoError:
            return []

    def update(self, database_name: str, collection_name: str, query: Dict[str, Any],
               update_data: Dict[str, Any]) -> int:
        """Query for and update documents in the provided database and collection.

        Args:
            database_name: Target MongoDB database name.
            collection_name: Target MongoDB collection name.
            query: Dictionary of key/value pairs used by the find() call.
            update_data: Dictionary of update operators/data for update_one() or update_many().

        Returns:
            The number of modified documents.
        """
        if not isinstance(query, dict) or not query:
            return 0

        if not isinstance(update_data, dict) or not update_data:
            return 0

        try:
            database = self.client[database_name]
            collection = database[collection_name]

            # Use update_many so the method can affect all matching documents.
            result = collection.update_many(query, update_data)
            return result.modified_count
        except PyMongoError:
            return 0

    def delete(self, database_name: str, collection_name: str, query: Dict[str, Any]) -> int:
        """Query for and remove documents from the provided database and collection.

        Args:
            database_name: Target MongoDB database name.
            collection_name: Target MongoDB collection name.
            query: Dictionary of key/value pairs used by the find() call.

        Returns:
            The number of deleted documents.
        """
        if not isinstance(query, dict) or not query:
            return 0

        try:
            database = self.client[database_name]
            collection = database[collection_name]
            result = collection.delete_many(query)
            return result.deleted_count
        except PyMongoError:
            return 0
