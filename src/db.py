from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]

    async def close(self):
        self.client.close()

    async def create_user(self, user_id: int, username: str = None, race: str = None, user_class: str = None):
        user_doc = {
            "user_id": user_id,
            "username": username,
            "race": race,
            "class": user_class,
            "coins": 1000,
            "inventory": []
        }
        result = await self.collection.insert_one(user_doc)
        return result.inserted_id

    async def read_user(self, user_id: int):
        return await self.collection.find_one({"user_id": user_id})

    async def update_user(self, user_id: int, update: dict):
        updated_document = await self.collection.find_one_and_update(
            {"user_id": user_id},
            {'$set': update},
            return_document=ReturnDocument.AFTER
        )
        return updated_document

    async def delete_user(self, user_id: int):
        result = await self.collection.delete_one({"user_id": user_id})
        return result.deleted_count

db_instance = Database()

def get_database():
    return db_instance