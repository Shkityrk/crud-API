from typing import List, Optional

from src.domain.user import User, UserCreate, UserUpdate
from src.usecase.user_repository import UserRepository


class UserInteractor:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(
            name=user_create.name,
            email=user_create.email,
            age=user_create.age,
        )
        return await self.user_repository.create(user)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_all_users(self) -> List[User]:
        return await self.user_repository.get_all()

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        existing_user = await self.user_repository.get_by_id(user_id)
        if not existing_user:
            return None

        # Обновляем только переданные поля
        if user_update.name is not None:
            existing_user.name = user_update.name
        if user_update.email is not None:
            existing_user.email = user_update.email
        if user_update.age is not None:
            existing_user.age = user_update.age

        return await self.user_repository.update(user_id, existing_user)

    async def delete_user(self, user_id: str) -> bool:
        return await self.user_repository.delete(user_id)

