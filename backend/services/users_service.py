from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from db.sql.crud.users_crud import (
    create_user,
    get_user,
    get_users,
    get_user_by_email,
    get_users_by_role,
    update_user,
    delete_user,
)
from db.sql.schemas.users_schemas import UserCreate, UserUpdate, UserResponse


class UsersService:
    """Сервис для работы с пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate) -> UserResponse:
        """Создание пользователя"""
        user = await create_user(self.session, data)
        if not user:
            raise HTTPException(400, "Не удалось создать пользователя")
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            email=user.email,
            is_acive=user.is_acive,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def get_by_id(self, user_id: int) -> UserResponse:
        """Получение пользователя по ID"""
        user = await get_user(self.session, user_id)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            email=user.email,
            is_acive=user.is_acive,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Получение списка пользователей"""
        users = await get_users(self.session, skip, limit)
        return [
            UserResponse(
                id=u.id,
                first_name=u.first_name,
                last_name=u.last_name,
                father_name=u.father_name,
                email=u.email,
                is_acive=u.is_acive,
                role_id=u.role_id,
                created_at=u.created_at,
                updated_at=u.updated_at,
            )
            for u in users
        ]

    async def update(self, user_id: int, data: UserUpdate) -> UserResponse:
        """Обновление пользователя"""
        user = await update_user(self.session, user_id, data)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            email=user.email,
            is_acive=user.is_acive,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def delete(self, user_id: int) -> bool:
        """Удаление пользователя"""
        success = await delete_user(self.session, user_id)
        if not success:
            raise HTTPException(404, "Пользователь не найден")
        return True
