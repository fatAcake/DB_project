from datetime import datetime
import random
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.sql.models import Users
from db.sql.schemas.users_schemas import UserCreate, UserUpdate
from services.binders_methods.binders_users import send_confirmation_email
from core.data import users_data


async def create_user(session: AsyncSession, data: UserCreate) -> Optional[Users]:
    """Создание пользователя"""
    try:
        user = Users(
            first_name=data.first_name,
            last_name=data.last_name,
            father_name=data.father_name or "",
            email=data.email,
            hash_password=data.hash_password,
            role_id=data.role_id,
            is_acive=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        verification_code = random.randint(100000, 999999)

        if await send_confirmation_email(user.email, 
            f"{user.first_name} {user.last_name} {user.father_name}", 
            verification_code) == True:
            users_data[user.id] = verification_code

        return user
    except Exception:
        await session.rollback()
        return None


async def get_user(session: AsyncSession, user_id: int) -> Optional[Users]:
    """Получение пользователя по ID"""
    result = await session.execute(select(Users).where(Users.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[Users]:
    """Получение пользователя по email"""
    result = await session.execute(select(Users).where(Users.email == email))
    return result.scalar_one_or_none()


async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[Users]:
    """Получение списка пользователей"""
    result = await session.execute(
        select(Users).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_users_by_role(session: AsyncSession, role_id: int) -> List[Users]:
    """Получение пользователей по роли"""
    result = await session.execute(
        select(Users).where(Users.role_id == role_id)
    )
    return list(result.scalars().all())


async def update_user(
    session: AsyncSession,
    user_id: int,
    data: UserUpdate,
) -> Optional[Users]:
    """Обновление пользователя"""
    user = await get_user(session, user_id)
    if not user:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    user.updated_at = datetime.now()
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    """Удаление пользователя"""
    user = await get_user(session, user_id)
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True

async def save_verification_code(user_id: int, code: int) -> None:
    """Сохранить код верификации в хранилище"""
    users_data[user_id] = code


async def get_verification_code(user_id: int) -> Optional[int]:
    """Получить код верификации из хранилища"""
    return users_data.get(user_id)


async def delete_verification_code(user_id: int) -> bool:
    """Удалить код верификации из хранилища"""
    if user_id in users_data:
        del users_data[user_id]
        return True
    return False


async def verify_user_code(user_id: int, code: int) -> bool:
    """Проверить код верификации"""
    stored_code = await get_verification_code(user_id)
    if stored_code is None:
        return False
    return stored_code == code


async def activate_user(session: AsyncSession, user_id: int) -> Optional[Users]:
    """Активировать пользователя"""
    user = await get_user(session, user_id)
    if not user:
        return None
    user.is_acive = True
    user.updated_at = datetime.now()
    await session.commit()
    await session.refresh(user)
    return user