from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
import os

class Database:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def close(self):
        self.client.close()

    async def create_document(self, collection_name: str, document: dict):
        collection = self.db[collection_name]
        result = await collection.insert_one(document)
        return result.inserted_id

    async def read_document(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        document = await collection.find_one(query)
        return document

    async def update_document(self, collection_name: str, query: dict, update: dict):
        collection = self.db[collection_name]
        updated_document = await collection.find_one_and_update(
            query,
            {'$set': update},
            return_document=ReturnDocument.AFTER
        )
        return updated_document

    async def delete_document(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        result = await collection.delete_one(query)
        return result.deleted_count

def get_database():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    return Database(mongo_uri, db_name)