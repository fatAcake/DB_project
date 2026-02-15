from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.sql.models import Users
from db.sql.schemas.users_schemas import UserCreate, UserUpdate


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
            is_acive=data.is_acive,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
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
