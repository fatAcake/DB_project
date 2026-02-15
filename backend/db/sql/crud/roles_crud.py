from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.sql.models import Roles
from db.sql.schemas.roles_schemas import RoleCreate, RoleUpdate


async def create_role(session: AsyncSession, data: RoleCreate) -> Optional[Roles]:
    """Создание роли"""
    try:
        role = Roles(
            name=data.name,
            description=data.description,
        )
        session.add(role)
        await session.commit()
        await session.refresh(role)
        return role
    except Exception:
        await session.rollback()
        return None


async def get_role(session: AsyncSession, role_id: int) -> Optional[Roles]:
    """Получение роли по ID"""
    result = await session.execute(select(Roles).where(Roles.id == role_id))
    return result.scalar_one_or_none()


async def get_roles(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[Roles]:
    """Получение списка ролей"""
    result = await session.execute(
        select(Roles).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_role_by_name(session: AsyncSession, name: str) -> Optional[Roles]:
    """Получение роли по имени"""
    result = await session.execute(
        select(Roles).where(Roles.name == name)
    )
    return result.scalar_one_or_none()


async def update_role(
    session: AsyncSession,
    role_id: int,
    data: RoleUpdate,
) -> Optional[Roles]:
    """Обновление роли"""
    role = await get_role(session, role_id)
    if not role:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(role, field, value)
    role.updated_at = datetime.now()
    await session.commit()
    await session.refresh(role)
    return role


async def delete_role(session: AsyncSession, role_id: int) -> bool:
    """Удаление роли"""
    role = await get_role(session, role_id)
    if not role:
        return False
    await session.delete(role)
    await session.commit()
    return True
