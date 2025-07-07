from pymongo import MongoClient
from pymongo.database import Database, Collection
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)


class MongoDBConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str):
        if not hasattr(self, "client"):
            self.client = MongoClient(host)

    def get_database(self, db_name: str) -> Database:
        if not self.client:
            raise RuntimeError("MongoDB client is not initialized.")
        return self.client[db_name]

    def get_collection(self, db_name: str, collection: str) -> Collection:
        if not self.client:
            raise RuntimeError("MongoDB client is not initialized.")
        return self.client[db_name][collection]

    def close(self):
        if self.client:
            self.client.close()


class MongoDBAsyncConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host: str):
        if not hasattr(self, "client"):
            self.client = AsyncIOMotorClient(host)

    def get_database(self, db_name: str) -> AsyncIOMotorDatabase:
        if not self.client:
            raise RuntimeError("MongoDB client is not initialized.")
        return self.client[db_name]

    def get_collection(
            self,
            db_name: str,
            collection: str
    ) -> AsyncIOMotorCollection:
        if not self.client:
            raise RuntimeError("MongoDB client is not initialized.")
        return self.client[db_name][collection]

    async def close(self):
        if self.client:
            self.client.close()
