from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from src.domain.user import User
from src.usecase.user_repository import UserRepository
from src.infrastructure.mongodb import MongoDB


class UserRepositoryImpl(UserRepository):
    def __init__(self):
        self.collection_name = "users"

    def _user_from_dict(self, data: dict) -> User:
        """Преобразует документ MongoDB в модель User"""
        return User(
            id=str(data["_id"]),
            name=data["name"],
            email=data["email"],
            age=data["age"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def _user_to_dict(self, user: User, exclude_id: bool = False) -> dict:
        """Преобразует модель User в словарь для MongoDB"""
        data = {
            "name": user.name,
            "email": user.email,
            "age": user.age,
        }
        if user.created_at:
            data["created_at"] = user.created_at
        if user.updated_at:
            data["updated_at"] = user.updated_at
        if not exclude_id and user.id:
            try:
                data["_id"] = ObjectId(user.id)
            except:
                pass
        return data

    async def create(self, user: User) -> User:
        collection = MongoDB.get_collection(self.collection_name)
        now = datetime.utcnow()
        user.created_at = now
        user.updated_at = now
        
        user_dict = self._user_to_dict(user, exclude_id=True)
        result = await collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        collection = MongoDB.get_collection(self.collection_name)
        try:
            user_doc = await collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return self._user_from_dict(user_doc)
        except:
            pass
        return None

    async def get_all(self) -> List[User]:
        collection = MongoDB.get_collection(self.collection_name)
        cursor = collection.find()
        users = []
        async for doc in cursor:
            users.append(self._user_from_dict(doc))
        return users

    async def update(self, user_id: str, user: User) -> Optional[User]:
        collection = MongoDB.get_collection(self.collection_name)
        user.updated_at = datetime.utcnow()
        
        # Обновляем только переданные поля, исключая created_at и _id
        update_data = {
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "updated_at": user.updated_at,
        }
        
        try:
            result = await collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            if result.modified_count > 0 or result.matched_count > 0:
                return await self.get_by_id(user_id)
        except:
            pass
        return None

    async def delete(self, user_id: str) -> bool:
        collection = MongoDB.get_collection(self.collection_name)
        try:
            result = await collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False

