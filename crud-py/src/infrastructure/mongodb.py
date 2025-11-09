from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect(cls):
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/crud_db")
        cls.client = AsyncIOMotorClient(mongodb_uri)
        # Извлекаем имя базы данных из URI
        # Формат: mongodb://host:port/db_name или mongodb://host:port/
        if "/" in mongodb_uri:
            db_name = mongodb_uri.rsplit("/", 1)[-1].split("?")[0]  # Убираем query параметры
            if not db_name:
                db_name = "crud_db"
        else:
            db_name = "crud_db"
        cls.database = cls.client[db_name]

    @classmethod
    async def disconnect(cls):
        if cls.client:
            cls.client.close()

    @classmethod
    def get_collection(cls, collection_name: str):
        if cls.database is None:
            raise RuntimeError("Database not connected. Call MongoDB.connect() first.")
        return cls.database[collection_name]

