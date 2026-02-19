from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from db.sql.crud.users_crud import (
    activate_user,
    create_user,
    delete_verification_code,
    get_user,
    get_users,
    get_user_by_email,
    get_users_by_role,
    update_user,
    delete_user,
    verify_user_code,
    save_password_code,
    verify_password_code,
)
from db.sql.crud.roles_crud import get_role, get_roles
from services.binders_methods.binders_users import send_password_change_code_email
from db.sql.schemas.users_schemas import UserCreate, UserUpdate, UserResponse, PasswordChangeRequest


class UsersService:
    """Сервис для работы с пользователями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate) -> UserResponse:
        """Создание пользователя"""
        user = await create_user(self.session, data)
        if not user:
            raise HTTPException(400, "Не удалось создать пользователя")
        role = await get_role(self.session, user.role_id)
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            email=user.email,
            is_acive=user.is_acive,
            role_id=user.role_id,
            role_name=role.name if role else None,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def get_by_id(self, user_id: int) -> UserResponse:
        """Получение пользователя по ID"""
        user = await get_user(self.session, user_id)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        role = await get_role(self.session, user.role_id)
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            email=user.email,
            is_acive=user.is_acive,
            role_id=user.role_id,
            role_name=role.name if role else None,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Получение списка пользователей"""
        users = await get_users(self.session, skip, limit)
        roles = await get_roles(self.session, 0, 1000)
        role_map = {r.id: r.name for r in roles}
        return [
            UserResponse(
                id=u.id,
                first_name=u.first_name,
                last_name=u.last_name,
                father_name=u.father_name,
                email=u.email,
                is_acive=u.is_acive,
                role_id=u.role_id,
                role_name=role_map.get(u.role_id),
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
        role = await get_role(self.session, user.role_id)
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            father_name=user.father_name,
            email=user.email,
            is_acive=user.is_acive,
            role_id=user.role_id,
            role_name=role.name if role else None,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def delete(self, user_id: int) -> bool:
        """Удаление пользователя"""
        success = await delete_user(self.session, user_id)
        if not success:
            raise HTTPException(404, "Пользователь не найден")
        return True

    async def verification_user(self, user_id: int, verification_code: int) -> bool:
        """Верификация пользователя по коду"""
        is_valid = await verify_user_code(user_id, verification_code)
        if not is_valid:
            return False

        user = await activate_user(self.session, user_id)
        if not user:
            return False

        await delete_verification_code(user_id)

        return True

    async def request_password_code(
        self, user_id: int, current_password: Optional[str] = None
    ) -> bool:
        """Отправить код смены пароля на email пользователя."""
        user = await get_user(self.session, user_id)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        if not user.email:
            raise HTTPException(400, "У пользователя не указан email")
        if current_password is not None and user.hash_password != current_password:
            raise HTTPException(400, "Неверный текущий пароль")

        import random
        code = random.randint(100000, 999999)
        await save_password_code(user_id, code)
        username = f"{user.first_name} {user.last_name}".strip() or user.email
        ok = await send_password_change_code_email(user.email, username, code)
        if not ok:
            raise HTTPException(503, "Не удалось отправить письмо. Попробуйте позже.")
        return True

    async def change_password(
        self, user_id: int, data: PasswordChangeRequest
    ) -> bool:
        """Сменить пароль по коду из email."""
        user = await get_user(self.session, user_id)
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        is_valid = await verify_password_code(user_id, data.code)
        if not is_valid:
            raise HTTPException(400, "Неверный код или код истёк")
        await update_user(
            self.session, user_id, UserUpdate(hash_password=data.new_password)
        )
        return True