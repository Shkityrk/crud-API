from typing import List
from fastapi import APIRouter, HTTPException, status

from src.domain.user import User, UserCreate, UserUpdate
from src.usecase.user_interactor import UserInteractor


def create_user_router(user_interactor: UserInteractor) -> APIRouter:
    router = APIRouter(prefix="/users", tags=["users"])

    @router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
    async def create_user(user_create: UserCreate):
        """Создать нового пользователя"""
        try:
            return await user_interactor.create_user(user_create)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка при создании пользователя: {str(e)}"
            )

    @router.get("/", response_model=List[User])
    async def get_all_users():
        """Получить всех пользователей"""
        try:
            return await user_interactor.get_all_users()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при получении пользователей: {str(e)}"
            )

    @router.get("/{user_id}", response_model=User)
    async def get_user_by_id(user_id: str):
        """Получить пользователя по ID"""
        user = await user_interactor.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user

    @router.put("/{user_id}", response_model=User)
    async def update_user(user_id: str, user_update: UserUpdate):
        """Обновить пользователя"""
        user = await user_interactor.update_user(user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user

    @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(user_id: str):
        """Удалить пользователя"""
        success = await user_interactor.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return None

    return router

