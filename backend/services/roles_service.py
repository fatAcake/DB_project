from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from db.sql.crud.roles_crud import (
    create_role,
    get_role,
    get_roles,
    update_role,
    delete_role,
)
from db.sql.schemas.roles_schemas import RoleCreate, RoleUpdate, RoleResponse


class RolesService:
    """Сервис для работы с ролями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: RoleCreate) -> RoleResponse:
        """Создание роли"""
        role = await create_role(self.session, data)
        if not role:
            raise HTTPException(400, "Не удалось создать роль")
        return RoleResponse(
            id=role.id,
            name=role.name,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    async def get_by_id(self, role_id: int) -> RoleResponse:
        """Получение роли по ID"""
        role = await get_role(self.session, role_id)
        if not role:
            raise HTTPException(404, "Роль не найдена")
        return RoleResponse(
            id=role.id,
            name=role.name,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[RoleResponse]:
        """Получение списка ролей"""
        roles = await get_roles(self.session, skip, limit)
        return [
            RoleResponse(
                id=r.id,
                name=r.name,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in roles
        ]

    async def update(self, role_id: int, data: RoleUpdate) -> RoleResponse:
        """Обновление роли"""
        role = await update_role(self.session, role_id, data)
        if not role:
            raise HTTPException(404, "Роль не найдена")
        return RoleResponse(
            id=role.id,
            name=role.name,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    async def delete(self, role_id: int) -> bool:
        """Удаление роли"""
        success = await delete_role(self.session, role_id)
        if not success:
            raise HTTPException(404, "Роль не найдена")
        return True
