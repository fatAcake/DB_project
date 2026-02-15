from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_postgres_db
from services.roles_service import RolesService
from db.sql.schemas.roles_schemas import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleResponse)
async def create_role(
    data: RoleCreate,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Создание роли"""
    service = RolesService(session)
    return await service.create(data)


@router.get("/", response_model=List[RoleResponse])
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_postgres_db),
):
    """Получение списка ролей"""
    service = RolesService(session)
    return await service.get_all(skip, limit)


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Получение роли по ID"""
    service = RolesService(session)
    return await service.get_by_id(role_id)


@router.patch("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    data: RoleUpdate,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Обновление роли"""
    service = RolesService(session)
    return await service.update(role_id, data)


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    session: AsyncSession = Depends(get_postgres_db),
):
    """Удаление роли"""
    service = RolesService(session)
    await service.delete(role_id)
    return {"ok": True}
